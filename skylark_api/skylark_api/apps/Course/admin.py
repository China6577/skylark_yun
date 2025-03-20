from django.contrib import admin
from .models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson, CourseDiscountType, CourseDiscount, \
    Activity, CoursePriceDiscount, CourseExpire


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 在列表中显示的字段
    search_fields = ('name',)  # 搜索框能够搜索的字段


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_type', 'level', 'status', 'pub_date', 'students')
    list_filter = ('course_type', 'level', 'status')  # 右侧过滤栏
    search_fields = ('name', 'brief')  # 搜索框能够搜索的字段
    date_hierarchy = 'pub_date'  # 详细时间分层筛选
    raw_id_fields = ('teacher', 'course_category')  # ForeignKey 和 ManyToMany 字段使用原始ID选择器


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'title')
    search_fields = ('name', 'title')


@admin.register(CourseChapter)
class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'name', 'course')
    list_filter = ('course',)
    search_fields = ('name',)


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'orders', 'section_type', 'chapter')
    list_filter = ('chapter__course', 'section_type')
    search_fields = ('name',)


@admin.register(CourseDiscountType)
class CourseDiscountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'remark')  # 列表页显示的字段
    search_fields = ('name',)  # 搜索字段
    list_per_page = 20  # 每页显示的数量


@admin.register(CourseDiscount)
class CourseDiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_type', 'condition', 'sale')  # 列表页显示的字段
    list_filter = ('discount_type',)  # 过滤器
    search_fields = ('discount_type__name', 'sale')  # 搜索字段
    list_per_page = 20


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'remark')  # 列表页显示的字段
    list_filter = ('start_time', 'end_time')  # 过滤器
    search_fields = ('name', 'remark')  # 搜索字段
    list_per_page = 20


@admin.register(CoursePriceDiscount)
class CoursePriceDiscountAdmin(admin.ModelAdmin):
    list_display = ('course', 'active', 'discount')  # 列表页显示的字段
    list_filter = ('active', 'discount__discount_type')  # 过滤器
    search_fields = ('course__name', 'active__name', 'discount__sale')  # 搜索字段
    list_per_page = 20


@admin.register(CourseExpire)
class CourseExpireAdmin(admin.ModelAdmin):
    list_display = ('course', 'expire_time', 'expire_text', 'price')
    list_filter = ('course', 'expire_time')
    search_fields = ('course__name', 'expire_time')
    list_per_page = 20
