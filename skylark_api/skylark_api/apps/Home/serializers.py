from rest_framework.serializers import ModelSerializer
from .models import Banner, Nav

# 序列化器的作用是给前端传数据
class BannerSerializers(ModelSerializer):
    """轮播广告的序列化器"""
    # 模型序列化器字段声明
    class Meta:
        model = Banner
        fields = ['image_url', 'link']  # 序列化器返回 1.图片的链接 2.点击图片跳转到对应的链接

class NavModelSerializer(ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = Nav
        fields = ["title","link","is_site"]