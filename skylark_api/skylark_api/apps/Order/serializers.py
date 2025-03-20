from rest_framework import serializers
from .models import Order, OrderDetail
from datetime import datetime
import random
from django_redis import get_redis_connection
from Course.models import Course, CourseExpire
from django.db import transaction
from Coupon.models import UserCoupon


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "order_title", "total_price",
            "real_price", "order_number", "order_status",
            "pay_type", "credit",
            "coupon", "pay_time",
        ]
        extra_kwargs = {
            "id": {"read_only": True, },
            "order_title": {"read_only": True, },
            "total_price": {"read_only": True, },
            "real_price": {"read_only": True, },
            "order_number": {"read_only": True, },
            "order_status": {"read_only": True, },
            "pay_time": {"read_only": True, },
            "pay_type": {"required": True, },
            "credit": {"required": True, "min_value": 0},
            "coupon": {"required": True, },
        }

    def create(self, validated_data):
        """生成订单"""
        """1. 先生成订单记录"""
        # 接受客户端提交的数据
        pay_type = validated_data.get("pay_type")
        credit = validated_data.get("credit", 0)
        coupon = validated_data.get("coupon", 0)
        # 生成必要参数
        user_id = self.context["request"].user.pk  # 在序列化器中获取视图中的数据，通过self.context
        order_title = "好课优选"
        # order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%06d" % user_id) + ("%04d" % random.randint(0, 9999))
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(user_id) + ("%04d" % random.randint(0, 9999))
        order_status = 0  # 未支付

        # 从redis中提取勾选商品
        redis = get_redis_connection("cart")

        # 从购物车中一区订单信息 返回二进制的数据
        course_set = redis.smembers("selected_%s" % user_id)
        cart_list = redis.hgetall("cart_%s" % user_id)

        # 如果没有任何勾选的商品，则不能继续下单
        if len(course_set) < 1:
            raise serializers.ValidationError("对不起，当前没有选中任何课程！")

        # 生成订单记录
        with transaction.atomic():
            # 设置SQL语句的回滚位置
            save_id = transaction.savepoint()

            order = super().create({
                "order_title": order_title,
                "total_price": 0,  # 等后面生成订单详情的时候，需要循环购物车中商品时，再计算总价格，再填进来
                "real_price": 0,
                "order_number": order_number,
                "order_status": order_status,
                "pay_type": pay_type,
                "credit": credit,
                "coupon": coupon,
                "order_desc": "",
                "user_id": user_id,
                "orders": 0,  # 排序字段
            })

            """2. 再生成订单详情"""
            # 声明订单总价格和订单实价
            total_price = 0

            for course_id_bytes in course_set:
                """在循环中把每一件商品添加订单详情"""
                course_expire_bytes = cart_list[course_id_bytes]
                expire_time = int(course_expire_bytes.decode())
                course_id = int(course_id_bytes.decode())
                print(expire_time)
                try:
                    course = Course.objects.get(pk=course_id)
                except:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError("对不起，商品课程不存在！")

                # 提取课程的有效期选项
                try:
                    """有效期选项"""
                    course_expire = CourseExpire.objects.get(expire_time=expire_time, course=course)
                    price = course_expire.price
                except CourseExpire.DoesNotExist:
                    """永久有效"""
                    price = course.price

                # 生成订单详情记录
                try:
                    order_detail = OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_time,
                        price=price,
                        real_price=course.real_price(price),
                        discount_name=course.discount_name,
                        orders=0,  # 排序字段
                    )
                except:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError("对不起，订单生成失败！请联系客服工作人员！")

                total_price += float(order_detail.real_price)

            # 保存订单的总价格
            order.total_price = total_price
            order.real_price = total_price  # 先默认当前商品总价是实付金额

            # 如果用户使用了优惠券，则计算加入优惠券以后的实付金额
            if coupon > 0:
                # 1. 查找优惠券
                user_coupon = UserCoupon.objects.get(is_show=True, is_delete=False, pk=coupon)
                # 2. 判断优惠券是否已经过期
                start_time = user_coupon.start_time.timestamp()
                now_time = datetime.now().timestamp()
                end_time = start_time + user_coupon.coupon.timer * 24 * 3600

                if start_time > now_time or now_time > end_time:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError("对不起，当前优惠券无法使用！请重新确认使用的优惠券")

                # 3. 判断优惠券是否满足使用条件
                if user_coupon.coupon.condition > total_price:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError("对不起，当前优惠券无法使用！请重新确认使用的优惠券")

                # 3. 根据优惠券的不同类型，采用不同的公式计算实付金额
                sale_num = float(user_coupon.coupon.sale[1:])
                if user_coupon.coupon.sale[0] == "-":
                    # 3.1 抵扣优惠券，实付总金额 = 商品总价 - 优惠券的金额
                    order.real_price = total_price - sale_num
                elif user_coupon.coupon.sale[0] == "*":
                    # 3.2 折扣优惠券，实付总金额 = 商品总价 * 优惠券的金额
                    order.real_price = total_price * sale_num

                # 防止出现无条件使用的优惠券产生负数的实付金额
                if order.real_price < 0:
                    order.real_price = 0

            order.save()

        """3. 清除掉购物车中勾选的商品"""
        pip = redis.pipeline()
        pip.multi()
        for course_id_bytes in cart_list:
            if course_id_bytes in course_set:
                pip.hdel("cart_%s" % user_id, course_id_bytes)
                pip.srem("selected_%s" % user_id, course_id_bytes)
        pip.execute()

        return order
