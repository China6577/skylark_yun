from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from Course.models import Course, CourseExpire
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
import logging
from skylark_api.settings.constants import SERVER_IMAGE_DOMAIN

log = logging.getLogger("django")


class CartAPIView(ViewSet):
    """
    购物车:
        1.获取请求数据
        2.验证课程是否存在
        3.连接redis
        4.检查课程是否已经在购物车中
        5.操作redis存储购物车数据
    """

    # 认证模块：IsAuthenticated必须是登录状态才能使用下面的功能
    permission_classes = [IsAuthenticated]

    # 保存商品到redis
    def add(self, request):
        """添加商品到购物车中"""
        # request是HttpRequest对象，它包含了客户端请求的各类信息
        # request.method request.get_full_path()完整路径
        # request.data是请求体的载荷 通过get(键)的形式获取数据 request.user代表当前用户的对象User应用中的user模型类
        course_id = request.data.get("course_id")
        user_id = request.user.id

        try:
            course = Course.objects.get(is_show=True, is_deleted=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误！课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection("cart")

        try:
            if redis_conn.hexists(f"cart_{user_id}", course_id):
                return Response({"message": "商品已存在于购物车中！", "cart_length": redis_conn.hlen(f"cart_{user_id}")})

            # 使用hash存储商品id和有效期
            # 使用set 存储被选中的商品id
            # hash：
            # 键[用户ID]: {
            #     域[商品ID]: 值[课程有效期],
            # }
            # set:
            #     键[用户ID]:{商品ID1,商品ID2....}
            pipe = redis_conn.pipeline()
            pipe.multi()
            # cart_1: {
            #     "30":"30"  # 商品id， 课程有效期为30天
            #     }
            # 课程，多门课程
            # selecetd_1: {"30", "29}   商品30和商品29，被选中
            pipe.hset(f"cart_{user_id}", course_id, 0)  # 默认有效期 0
            pipe.sadd(f"selected_{user_id}", course_id)  # 默认勾选
            pipe.execute()

            course_len = redis_conn.hlen(f"cart_{user_id}")
            log.info(f"用户 {user_id} 添加课程 {course_id} 到购物车，当前购物车商品总数：{course_len}")

        except Exception as e:
            log.error(f"购物车数据存储错误：{str(e)}")
            return Response({"message": "服务器错误，购物车添加商品失败！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {"message": "购物车商品添加成功！", "cart_length": course_len}

        return Response(data)

    # 获取商品
    def list(self, request):
        """获取购物车商品列表"""
        # 获取用户ID
        user_id = request.user.id
        # 获取redis链接对象cart
        redis_conn = get_redis_connection("cart")
        # 获取用户购物车
        cart_course_list = redis_conn.hgetall(f"cart_{user_id}")
        # 获取用户的选项
        cart_selected_list = redis_conn.smembers(f"selected_{user_id}")

        if len(cart_course_list) < 1:
            return Response({"cart_length": 0, "data": []})  # 返回空列表和购物车数量

        data = []

        # course_bytes，expire_bytes 是从redis获取的数据，redis返回的数据是字节类型(bytes)
        # 需要解码才能转换为字符串
        for course_bytes, expire_bytes in cart_course_list.items():
            # 因为后端返回的数据格式问题，导致有效期显示为 0 而int可以将他们转为相同类型
            course_id = int(course_bytes.decode())
            expire_id = int(expire_bytes.decode())

            try:
                course = Course.objects.get(pk=course_id)

            except Course.DoesNotExist:
                continue

            data.append({
                "id": course_id,
                "expire_id": expire_id,
                "name": course.name,
                "course_img": f"{SERVER_IMAGE_DOMAIN}{course.course_img.url}",
                "price": course.real_price(expire_id),
                "expire_list": course.expire_list,
                # 判断当前商品是否被选中
                # cart_selected_list是一个哈希字典
                # 课程id是否存在于cart_selected_list中
                "is_selected": True if course_bytes in cart_selected_list else False
            })

        cart_length = len(data)  # 计算购物车商品总数
        return Response({"cart_length": cart_length, "data": data})  # 返回购物车数量和商品列表

    def change_selected(self, request):
        """修改选中状态"""
        """
        1.获取selected
        2.获取到用户
        3.查询redis数据
        4.修改勾选状态
        5.返回结果
        """
        user_id = request.user.id
        # 前端axios请求带的data数据集 传过来的勾选状态
        selected = request.data.get('selected')

        course_id = request.data.get('course_id')
        try:
            Course.objects.get(is_deleted=False, is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数有误！当前课程数据不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection("cart")
        if selected:
            # sadd 是 Redis 的一个命令，用于往集合（set）中添加一个或多个元素
            redis_conn.sadd("selected_%s" % user_id, course_id)
        else:
            # srem 是 Redis 的一个命令，全称为 "Set Remove"，用于从集合中移除一个或多个指定的元素
            redis_conn.srem("selected_%s" % user_id, course_id)

        return Response({'message': '选中状态修改成功！'}, status=status.HTTP_200_OK)

    def change_all_selected(self, request):
        user_id = request.user.id
        # 前端axios请求带的data数据集 传过来的勾选状态
        selected = request.data.get('is_all_selected')
        cartList = request.data.get('cartList')

        redis_conn = get_redis_connection("cart")
        for cart in cartList:
            if selected:
                # sadd 是 Redis 的一个命令，用于往集合（set）中添加一个或多个元素
                redis_conn.sadd("selected_%s" % user_id, cart["id"])
            else:
                # srem 是 Redis 的一个命令，全称为 "Set Remove"，用于从集合中移除一个或多个指定的元素
                redis_conn.srem("selected_%s" % user_id, cart["id"])

        return Response({'message': '全选状态修改成功！'}, status=status.HTTP_200_OK)

    def change_expire(self, request):
        user_id = request.user.id
        selected = request.data.get('selected')
        expire_id = request.data.get('expire_id')

        course_id = request.data.get('course_id')

        try:
            # 判断课程是否存在
            course = Course.objects.get(is_deleted=False, is_show=True, id=course_id)
            # 判断课程有效期选项是0还是其他选项，如果是其他数值，还要判断是否存在于有效期选项表中
            if expire_id > 0:
                expire_item = CourseExpire.objects.filter(is_show=True, is_deleted=False, id=expire_id)
                if not expire_item:
                    raise Course.DoesNotExist()

        except Course.DoesNotExist:
            return Response({'message': '参数有误！当前课程数据不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection("cart")
        redis_conn.hset('cart_%s' % user_id, course_id, expire_id)

        # 重新计算课程价格
        price = course.real_price(expire_id)

        return Response({'message': '切换有效期成功！', 'price': price})

    def del_cart(self, request):
        """删除购物车中商品信息"""
        user_id = request.user.id
        course_id = request.query_params.get('course_id')

        try:
            Course.objects.get(is_deleted=False, is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数有误！当前课程数据不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection("cart")

        pipe = redis_conn.pipeline()
        pipe.multi()
        pipe.hdel('cart_%s' % user_id, course_id)
        pipe.srem('selected_%s' % user_id, course_id)
        pipe.execute()

        return Response({"message": "删除商品成功！"})

    # 获取购物车中勾选的商品列表
    def get_selected_course(self, request):
        """获取购物车中勾选的商品列表"""
        # 获取用户ID
        user_id = request.user.id
        # 获取redis连接
        redis_conn = get_redis_connection("cart")

        # 获取购物车中所有的商品
        cart_bytes_dict = redis_conn.hgetall("cart_%s" % user_id)
        selected_bytes_list = redis_conn.smembers("selected_%s" % user_id)

        # 获取勾选的商品
        data = []  # 商品列表
        total_price = 0  # 勾选商品总价格
        for course_id_bytes, expire_id_bytes in cart_bytes_dict.items():
            course_id = int(course_id_bytes.decode())
            expire_id = int(expire_id_bytes.decode())
            # 判断商品课程ID是否在勾选集合中
            if course_id_bytes in selected_bytes_list:
                try:
                    course = Course.objects.get(is_show=True, is_deleted=False, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # 判断课程有效期，获取课程原价
                original_price = course.price
                expire_text = "永久有效"
                try:
                    if expire_id > 0:
                        coruseexpire = CourseExpire.objects.get(id=expire_id)
                        original_price = coruseexpire.price
                        expire_text = coruseexpire.expire_text
                except CourseExpire.DoesNotExist:
                    pass

                real_price = course.real_price(expire_id)

                data.append({
                    "course_img": SERVER_IMAGE_DOMAIN + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_text": expire_text,
                    "discount_name": course.discount_name,
                    "real_price": real_price,
                    "original_price": "%.2f" % original_price
                })

                total_price += float(real_price)

        return Response({"course_list": data, "total_price": total_price})