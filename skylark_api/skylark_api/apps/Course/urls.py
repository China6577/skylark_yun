from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CourseCategoryListAPIView.as_view() ),
    path('', views.CourseListAPIView.as_view() ),
    path("<int:pk>/", views.CourseRetrieveAPIView.as_view()),
    # 章节路由
    path("chapter/", views.CourseChapterListAPIView.as_view()),
]
