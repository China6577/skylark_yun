from django.urls import path
from . import views

urlpatterns = [
    path("banner/", views.BannerListApiView.as_view()),
    path('nav/', views.NavListApiView.as_view()),
    path("nav/header/", views.HeaderNavListApiView.as_view()),
    path("nav/footer/", views.FooterNavListApiView.as_view()),
]
