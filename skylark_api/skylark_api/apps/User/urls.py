from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .utils import PhoneApiView

urlpatterns = [
    # 生成token
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('', views.UserAPIView.as_view(), name='user'),
    re_path(r"phone/(?P<phone>1[3-9]\d{9})/", PhoneApiView.as_view(), name='phone'),
    re_path(r"sms/(?P<phone>1[3-9]\d{9})/", views.SMSAPIView.as_view()),
]
