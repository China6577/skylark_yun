"""重写认证添加手机号认证"""

import re
from .models import User
from django.contrib.auth.backends import ModelBackend


def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # 账号为手机号
            user = User.objects.get(mobile=account)
        else:
            # 账号为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        # 验证用户名存在 且密码正确
        if user is not None and user.check_password(password):
            return user

"""验证手机号是否被注册过"""
from rest_framework.views import APIView
from rest_framework.response import Response

class PhoneApiView(APIView):
    def get(self, request, phone):
        ret = get_user_by_account(phone)
        if ret is not None:
            # 判断用户是否已经存在
                return Response({"message": "手机号码已经被注册过了！"}, status=400)

        return Response({'message': 'ok'})
