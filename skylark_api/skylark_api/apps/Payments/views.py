from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Order.models import Order
from Coupon.models import UserCoupon
from alipay import AliPay
from django.conf import settings
import os
from django.db import transaction
from decimal import Decimal
import logging
log = logging.getLogger("django")
from datetime import datetime
from User.models import UserCourse

class AlipayAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        """生成支付宝支付地址"""
        # 接受参数[优惠券,订单号]
        coupon_id = request.query_params.get("coupon_id")
        order_number  = request.query_params.get("order_number")
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"message":"对不起,当前订单信息不存在!无法进行支付"},status=status.HTTP_400_BAD_REQUEST)

        if coupon_id != None and coupon_id != "0":
            with transaction.atomic():
                save_id = transaction.savepoint()
                # 重新计算订单实际支付价格
                try:
                    user_coupon = UserCoupon.objects.get(pk=coupon_id)
                except UserCoupon.DoesNotExist:
                    return Response({"message": "对不起,当前订单使用的优惠券不存在!无法进行支付"}, status=status.HTTP_400_BAD_REQUEST)

                if user_coupon.coupon.coupon_type == 0:
                    """折扣优惠"""
                    order.real_price = order.total_price * Decimal(user_coupon.coupon.sale[1:])
                elif user_coupon.coupon.coupon_type == 1:
                    order.real_price = order.total_price - Decimal(user_coupon.coupon.sale[1:])
                else:
                    return Response({"message": "当前优惠券无法使用!无法进行支付"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    # 经过上面的计算,保存实付价格和使用的优惠券
                    order.use_coupon = True
                    order.coupon = user_coupon.id
                    order.save()

                    # 上面的优惠券已经被使用了,所以我们需要修改优惠券的状态
                    user_coupon.is_use = True
                    user_coupon.save()

                except:
                    transaction.savepoint_rollback(save_id)
                    return Response({"message": "系统异常,无法进行支付"}, status=status.HTTP_400_BAD_REQUEST)

        # 构造支付宝支付链接地址
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=settings.APP_NOTIFY_URL,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount= "%.2f" % order.real_price,
            subject=order.order_title,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL,
        )

        url = settings.APIPAY_GATEWAY + "?" + order_string

        return Response({"message":"发起支付成功","url":url})


class AlipayResult(APIView):

    def post(self,request):

        data = request.data.dict()
        # 在字典中移除sign签名
        signature = data.pop("sign")

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=settings.APP_NOTIFY_URL,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG
        )

        success = alipay.verify(data, signature)
        if success:
            # 支付成功!
            # 更新订单
            order_number = data.get("out_trade_no")
            try:
                order = Order.objects.get( order_number=order_number )
            except Order.DoesNotExist:
                log.error("订单号:%s不存在!" % order_number )
                return Response({"message": "无效的订单号"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with transaction.atomic():
                save_id = transaction.savepoint()
                try:
                    order.order_status = 1
                    order.pay_time = datetime.now()
                    # order.pay_time = data.get("timestamp")
                    order.save()

                    # 课程与用户之间添加一条购买记录
                    detail_list = order.order_courses.all()
                    course_list = []
                    for detail in detail_list:

                        if detail.expire=='-1':
                            out_time = "2099-01-01 00:00:00"
                        else:
                            out_time = datetime.now().timestamp() + detail.expire * 86400
                            # 日期时间对象 = fromtimestamp(数值时间戳)
                            out_time = datetime.fromtimestamp(out_time)
                            out_time = out_time.strftime("%Y-%m-%d %H:%M:%S")

                        UserCourse.objects.create(
                            user=order.user,
                            course=detail.course,
                            buy_number=data.get("trade_no"),
                            buy_type=0,
                            pay_time=data.get("timestamp"),
                            out_time=out_time
                        )

                        course_list.append(detail.course.name)

                    return Response("success", content_type="text/html")

                except:
                    log.error("修改订单和购买记录发生异常!")
                    transaction.savepoint_rollback(save_id)
                    return Response({"message":"系统异常!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)