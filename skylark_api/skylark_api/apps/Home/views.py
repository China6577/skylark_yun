from rest_framework.generics import ListAPIView
from .models import Banner, Nav
from .serializers import BannerSerializers, NavModelSerializer
from skylark_api.settings import constants


# Create your views here.
# 因为轮播图只用获取数据 所以使用ListAPIView只有get方法的实现
class BannerListApiView(ListAPIView):
    # 限制返回的图片 必须满足is_show=True, is_deleted=False才返回 降序排序(因为最后导入的最新先显示)
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by('-orders', '-id')[
               :constants.BANNER_LENGTH]
    serializer_class = BannerSerializers


class NavListApiView(ListAPIView):
    """
    导航菜单视图
    """
    queryset = Nav.objects.filter(is_show=True, is_deleted=False).order_by('-orders', '-id')[
               :constants.HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer


class HeaderNavListApiView(ListAPIView):
    """
    顶部导航菜单视图
    """
    queryset = Nav.objects.filter(is_show=True, is_deleted=False, position=1).order_by('-orders', '-id')[
               :constants.HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer


class FooterNavListApiView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_deleted=False, position=2).order_by('-orders', '-id')[
               :constants.FOOTER_NAV_LENGTH]
    serializer_class = NavModelSerializer
