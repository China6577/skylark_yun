from rest_framework.generics import ListAPIView
from .models import CourseCategory
from .serializers import CourseCategoryModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders")
    serializer_class = CourseCategoryModelSerializer


from .models import Course
from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CustomPageNumberPagination


# 课程查询
class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_deleted=False, is_show=True).order_by("orders")
    serializer_class = CourseModelSerializer

    # 设置过滤器和排序后端
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # 导入自定义分页器
    # 如/course/?page=2&size=2
    pagination_class = CustomPageNumberPagination

    # 设置允许过滤的字段: 按照课程分类过滤
    # 如/course/?course_category=1
    filterset_fields = ('course_category',)

    # 允许排序的字段：按照id\学生人数\价格排序
    # 如/course/?course_category=3&ordering=-id
    ordering_fields = ('id', 'students', 'price')


from rest_framework.generics import RetrieveAPIView
from .serializers import CourseRetrieveSerializer


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_deleted=False, is_show=True)
    serializer_class = CourseRetrieveSerializer


from .models import CourseChapter
from .serializers import CourseChapterSerializer


# 课程章节返回
class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_deleted=False, is_show=True).order_by("chapter")
    serializer_class = CourseChapterSerializer

    filter_backends = [DjangoFilterBackend]

    # course是course_id关联到Course模型的id /course/chapter/?course=3
    filterset_fields = ['course', ]
