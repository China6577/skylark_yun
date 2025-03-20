from django.urls import path
from . import views
urlpatterns = [
    path("alipay/url/",views.AlipayAPIView.as_view() ),
    path("alipay/result/",views.AlipayResult.as_view() ),
]