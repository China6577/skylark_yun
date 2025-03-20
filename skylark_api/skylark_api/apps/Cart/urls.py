from django.urls import path
from . import views

# ViewSet书写路由方法
urlpatterns = [
    path("", views.CartAPIView.as_view({"post": "add", "get": "list",'put': 'change_expire', 'delete': 'del_cart'})), # patch和put功能一样 但 是局部作用的请求 只会接受局部资源并更新
    path("changeselected/", views.CartAPIView.as_view({'patch': 'change_selected','put': 'change_all_selected'})),
    path(r"order/",views.CartAPIView.as_view({"get":"get_selected_course"}))
]
