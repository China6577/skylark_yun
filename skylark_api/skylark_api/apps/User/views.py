from .serializers import CustomTokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义token视图"""
    serializer_class = CustomTokenObtainSerializer


from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserModelSerializer


class UserAPIView(CreateAPIView):
    """用户信息视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework import status
import random
from skylark_api.settings import constants
import logging
from mycelery.sms.task import send_sms

logger = logging.getLogger("django")

class SMSAPIView(APIView):
    def get(self, request, phone):
        """短信发送"""
        # 1. 判断手机号码是否在60秒内曾经发送过短信
        redis_conn = get_redis_connection("sms_code")
        ret = redis_conn.get(f"phone_{phone}")
        if ret is not None:
            return Response({"message": "对不起，60秒内已经发送过短信，请耐心等待"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 生成短信验证码
        sms_code = "%06d" % random.randint(1, 999999)  # 生成 6 位验证码

        # 3. 保存短信验证码到redis
        # 使用事务确保操作的原子性: 可以多个客户端一起发送验证码验证
        pipe = redis_conn.pipeline()

        # 开启事务模式：解决高并发问题,多任务执行
        pipe.multi()
        # 存储验证码
        pipe.setex(f"sms_{phone}", constants.SMS_EXPIRE_TIME, sms_code)  # 验证码有效期 5 分钟
        # 间隔时间
        pipe.setex(f"phone_{phone}", constants.SMS_INTERVAL_TIME, "_")  # 发送间隔 60 秒

        # 执行所有的事务
        pipe.execute()

        # redis_conn.setex(f"sms_{phone}", constants.SMS_EXPIRE_TIME, sms_code)  # redis_conn.setex用于设置一个带有过期时间的键值对
        # redis_conn.setex(f"phone_{phone}", constants.SMS_INTERVAL_TIME, "_")  # redis_conn.setex(键,过期时间,值)

        # 4. 调用 Celery 任务异步发送短信
        """
        "Code": "LimitExceeded.PhoneNumberDailyLimit" 则说明该手机号码今天收到验证码已经达到上线
        "Code": "Ok" 则是手机成功收到验证码
        """
        try:
            # 调用 Celery 异步任务
            send_sms.delay(phone, sms_code)
            logger.info(f"短信发送任务已提交！手机号：{phone}，验证码：{sms_code}")
            return Response({"message": "发送短信成功！"})
        except Exception as e:
            logger.error(f"短信发送任务异常！手机号：{phone}，异常信息：{str(e)}")
            return Response({"message": "发送短信失败！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
