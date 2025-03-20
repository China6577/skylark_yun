from rest_framework.generics import ListAPIView
from .models import UserCoupon
from .serializers import UserCouponModelSerializer
from rest_framework.permissions import IsAuthenticated


class UserCouponListAPIView(ListAPIView):
    serializer_class = UserCouponModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 获取当前登录用户！ 在确定用户登录以后，可以通过视图对象本身获取 request对象
        return UserCoupon.objects.filter(is_show=True, is_deleted=False, is_use=False, user_id=self.request.user.id)
