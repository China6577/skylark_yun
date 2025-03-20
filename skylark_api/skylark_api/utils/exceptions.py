from rest_framework.views import exception_handler
from django.db import DatabaseError
from rest_framework.response import Response
import logging

logger = logging.getLogger("django")

from rest_framework import status
from redis import RedisError


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc:  本次请求发生的异常信息
    :param context:  本清请求发送异常的执行上下文[ 本次请求的request对象，异常发送的时间，行号等... ]
    :return:
    """
    response = exception_handler(exc, context)

    if response is None:
        """来到这里只有2种情况：要么程序没出错，要么就是出错了而django或者restframework不识别"""
        view = context["view"]
        # mysql和redis的异常捕获
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误，请联系客服工作人员！'},
                                status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
