"""
URL configuration for skylark_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页的路由
    path('home/', include('Home.urls')),
    # 捕获media/下的文件的路由 如127.0.0.1:8000/media/banner/横版课程宣传图.png
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('user/', include('User.urls')),
    path('course/', include("Course.urls")),
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # CKEditor 5 路由
    path('cart/', include("Cart.urls")),
    path('order/', include("Order.urls")),
    path('coupon/', include("Coupon.urls")),
]
