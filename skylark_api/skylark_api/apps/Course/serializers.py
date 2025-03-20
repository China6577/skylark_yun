# 开发中一个序列化器 A 中需要同时序列化其他模型 B 的数据返回给客户端,那么直接通过外键默认只会返回主键ID
# 所以我们可以通过再创建一个模型B的序列化器,对模型B的数据进行序列化
# 在序列化器A中直接把模型B的序列化器调用作为字段值来声明即可.

from rest_framework import serializers
from .models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    """课程分类的序列化器"""

    class Meta:
        model = CourseCategory
        fields = ("id", "name")


# 把原来的讲师序列化器增加几个字段
class CourseTeacherModelSerializer(serializers.ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ["id", "name", "role", "title", "signature", "brief", "image"]


class CourseRetrieveSerializer(serializers.ModelSerializer):
    """课程详情页数据的序列化器"""
    teacher = CourseTeacherModelSerializer()
    real_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "students", "lessons", "pub_lessons", "price", "course_img", "teacher", "level_name",
                  "brief_html", "course_video","discount_name","real_price","activity_time"]

    def get_real_price(self, obj):
        real_price = obj.real_price()
        return real_price


class CourseModelSerializer(serializers.ModelSerializer):
    """课程信息的序列化器"""
    teacher = CourseTeacherModelSerializer()  # 老师 1 : 多课程
    # teacher = CourseTeacherModelSerializer(many=True) # 多对1

    # 自定义字段，用于返回课时信息
    # serializers.SerializerMethodField() 允许我们在序列化中通过调用一个自定义方法来生成字段的值
    lesson_list = serializers.SerializerMethodField()
    real_price = serializers.SerializerMethodField()

    class Meta:
        # 当前正在序列化的模型实例
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons", "price",
                  "teacher", "lesson_list", "discount_name", "real_price")

    def get_lesson_list(self, obj):
        """自定义方法 用于获取课时信息"""
        # 调用模型中的lesson_list的方法
        #  obj 当前正在序列化的模型实例(在class Meta中指定的) 即Course
        lesson_data = obj.lesson_list()  # 调用Course中的lesson_list()来生成课程数据
        return lesson_data

    def get_real_price(self, obj):
        real_price = obj.real_price()
        return real_price


# 课时信息返回
class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id", "name", "duration", "free_trail"]


# 课程章节返回
class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections = CourseLessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseChapter
        fields = ["id", "name", "chapter", "summary", "pub_date", "coursesections"]
