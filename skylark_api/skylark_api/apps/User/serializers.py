# 自定义序列化器
# 添加自定义字段到token
import re

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from User.utils import get_user_by_account
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django_redis import get_redis_connection


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 继承了原方法：生成refresh和access字段
        token = super().get_token(user)

        # 添加自定义生成字段
        token['id'] = user.id

        return token

    def validate(self, attrs):
        # 继承了原方法：验证原用户登录信息 用户名或手机号登录 验证密码是否正确
        data = super().validate(attrs)

        # 将自定义的字段添加到返回数据中
        data['id'] = self.user.id
        return data


class UserModelSerializer(serializers.ModelSerializer):
    """
    添加短信验证码和token字段
    """
    # 临时字段，不用存储到数据库中 需要post请求上传
    # 验证码不需要存储到数据库，用于验证过程
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, label="验证码")
    # token 也不需要保存到数据库
    token = serializers.CharField(max_length=1024, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "mobile", "password", "sms_code", 'token']
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
            # 为了用户的密码安全，只写入不读取
            "password": {"write_only": True},
            "mobile": {"write_only": True}
        }

    def validate(self, attrs):
        """
        验证方法：
            对手机号、短信验证码进行校验
        """

        phone = attrs.get("mobile")
        sms_code = attrs.get('sms_code')
        password = attrs.get('password')

        # 验证手机号码的格式(国内)
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError({'phone': '手机号码格式有误！'})  # raise抛出异常

        # 验证手机号码是否已被注册
        if get_user_by_account(phone):
            raise serializers.ValidationError({'phone': '手机号码已被注册'})

        # 验证验证码是否正确
        redis_conn = get_redis_connection('sms_code')
        real_sms_code = redis_conn.get(f'sms_{phone}')
        if real_sms_code is None:
            raise serializers.ValidationError({'sms_code': '短信验证码已经失效,请重新发送'})

        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError({'sms_code': '短信验证码有误,请核对后重试！'})

        # 本次验证成功后，直接删除当前本次验证码，防止恶意暴力破解
        redis_conn.delete(f"sms_{phone}")

        return attrs

    def create(self, validated_data):
        """
        创建用户并返回token

        :param validated_data: validate方法验证通过的数据
        :return:
        """
        # 移除不需要的数据 不会保存在数据库中
        validated_data.pop("sms_code")

        # 密码加密
        raw_password = validated_data.get('password')  # 获取明文密码
        validated_data["password"] = make_password(raw_password)  # 加密密码

        # 设置默认用户名为手机号
        validated_data['username'] = validated_data.get('mobile')

        # 创建用户
        user = User.objects.create(**validated_data)  # **是Python中的解包操作符 用于将字典解包为关键字参数

        # 生成refresh token值
        # for_user作用：为指定用户创建JWT令牌
        refresh = RefreshToken.for_user(user)
        user.token = str(refresh.access_token)

        return user
