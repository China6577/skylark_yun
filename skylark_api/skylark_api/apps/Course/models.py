from datetime import datetime

from django.db import models
from django.utils.timezone import now

from skylark_api.utils.utils import BaseModel
from django_ckeditor_5.fields import CKEditor5Field
from skylark_api.settings import constants


# Create your models here.
class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "sk_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """
    专题课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    brief = CKEditor5Field(max_length=2048, verbose_name="课程概述", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    # "CourseCvategory"延迟引用(字段用""包裹) 不加的话就是直接引用:当我们需要引用的模型名字不存在时会报错,延迟引用则不会
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "sk_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    def __str__(self):
        return "%s" % self.name

    # 封面视频字段
    course_video = models.FileField(upload_to="video", null=True, blank=True, verbose_name="封面视频")

    # 直接创建可用字段level_name添加到Course模型字段中 序列化器可直接使用该字段
    @property
    def level_name(self):
        # 将数据库的数字转化为具体的难度
        return self.level_choices[self.level][1]

    @property
    def brief_html(self):
        """把详情介绍中的图片地址拼上域名"""
        html = self.brief.replace('src="/media', 'src="%s/media' % constants.SERVER_IMAGE_DOMAIN)
        return html

    def lesson_list(self):
        """获取当前课程的前4个课时展示到列表中"""

        # 获取所有章节
        # self.coursechapters.filter可以筛选查询到与Course相关联的coursechapter(章节)列表 反向关联的用法
        chapters_list = self.coursechapters.filter(is_deleted=False, is_show=True)
        lesson_list = []
        if chapters_list:
            for chapter in chapters_list:
                # lessons是chapter(章节)关联的coursesections(课程)的列表 是chapter表反向关联的应用
                lessons = chapter.coursesections.filter(is_deleted=False, is_show=True)[:4]
                if lessons:
                    for lesson in lessons:
                        lesson_list.append({
                            "id": lesson.id,
                            "name": lesson.name,
                            "free_trail": lesson.free_trail
                        })

        return lesson_list

    def active_list(self):
        """
        获取当前课程参与的所有有效活动
        是不是应该开始时间大于当前时间，
        结束时间小于当前时间才生效

        参与的时间 1.13 7:30
        开始时间 1.13 9:30
        活动的开始时间 <= 当前时间
        """

        # activeprices是反向关联名
        return self.activeprices.filter(is_show=True, is_deleted=False, active__start_time__lte=now(),
                                        active__end_time__gte=now()).order_by("-orders", "-id")

    @property
    def discount_name(self):
        """课程参与活动的折扣类型名称"""
        name = ""
        # 获取到当前课程参与的所有活动
        active_list = self.active_list()

        if len(active_list) > 0:
            """当前课程如果有参与一个以上活动时才有优惠类型"""
            active = active_list[0]
            name = active.discount.discount_type.name
        return name

    def real_price(self, expire_id=None):
        """
        计算课程的真实价格(经过活动折扣后的价格)
        :return:
        """
        # 默认的真实价格为原价
        if expire_id:
            price = self.course_expire.filter(id=expire_id).first().price
        else:
            price = self.price
        # 获取当前课程参与的活动
        active_list = self.active_list()

        # 检查是否有活动
        if len(active_list) > 0:
            # 如果active_list 不为空，表示课程参与了活动
            # 获取优先级最高的活动
            active = active_list[0]

            condition = active.discount.condition
            sale = active.discount.sale
            self.price = float(self.price)
            """只有原价满足价格门槛才进行优惠计算"""
            if self.price >= condition:
                if sale == "":

                    """限时免费"""
                    price = 0
                elif sale[0] == "*":
                    """限时折扣"""
                    price = self.price * float(sale[1:])

                elif sale[0] == '-':
                    """限时减免"""
                    price = self.price - float(sale[1:])

                elif sale[0] == '满':
                    """满减"""
                    sale_list = sale.split("\r\n")
                    # 设置一个列表，把当前课程原价满足的满减条件全部保存进去
                    price_list = []
                    # 把满减的每一个选项在循环中，提取条件价格和课程原价进行判断
                    for sale_item in sale_list:
                        item = sale_item[1:]
                        condition_price, condition_sale = item.split('-')
                        if self.price >= float(condition_price):
                            price_list.append(float(condition_price))

                    price = self.price - max(price_list)  # 课程原价-最大优惠
        return "%.2f" % price

    @property
    def activity_time(self):
        """计算活动剩余时间"""
        time = 0
        active_list = self.active_list()
        if len(active_list) > 0:
            active = active_list[0]
            # 当前服务器时间戳(从格林威治时间1970年1月1日00:00:00（北京时间1970年1月1日08:00:00）起至当前时间的总秒数)
            now_time = datetime.now().timestamp()
            # 活动结束时间戳
            end_time = active.active.end_time.timestamp()
            time = end_time - now_time
        return int(time)

    @property
    def expire_list(self):
        """当前课程的有效期列表"""
        data_list = []
        expire_list = self.course_expire.filter(is_show=True, is_deleted=False).order_by('-id')

        for item in expire_list:
            data_list.append({
                "id": item.id,
                "expire_text": item.expire_text,
                "price": item.price
            })
        if self.price > 0:
            # 追加永久有效，永久有效的id默认为0
            data_list.append({"id": 0,
                              "expire_text": "永久有效",
                              "price": self.price})

        return data_list


class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "sk_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    # 第一个参数是关联的模型类 related_name='coursechapters'则可以通过Course模型类的对象访问与之相关的所有Chapter模型的对象
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE,
                               verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "sk_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    class Meta:
        db_table = "sk_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


"""价格相关的模型"""


class CourseDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="优惠类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "sk_course_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = "课程优惠类型"

    def __str__(self):
        return "%s" % self.name


class CourseDiscount(BaseModel):
    """课程优惠模型"""
    discount_type = models.ForeignKey("CourseDiscountType", on_delete=models.CASCADE, related_name='coursediscount',
                                      verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件",
                                    help_text="设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛")
    sale = models.TextField(verbose_name="优惠公式", blank=True, null=True, help_text="""
     不填表示免费；<br>
     *号开头表示折扣价，例如*0.82表示八二折；<br>
     -号开头则表示减免，例如-20表示原价-20；<br>
     如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>
     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-25<br>
     """)

    class Meta:
        db_table = "sk_course_discount"
        verbose_name = "价格优惠策略"
        verbose_name_plural = "价格优惠策略"

    def __str__(self):
        return "价格优惠:%s,优惠条件:%s,优惠值:%s" % (self.discount_type.name, self.condition, self.sale)


class Activity(BaseModel):
    """优惠活动"""
    name = models.CharField(max_length=150, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "sk_activity"
        verbose_name = "商品活动"
        verbose_name_plural = "商品活动"

    def __str__(self):
        return self.name


class CoursePriceDiscount(BaseModel):
    """课程与优惠策略的关系表"""
    # related_name 是 Django 模型中用于定义反向关系名称(自己取的一搬要有意义)的一个参数
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="activeprices", verbose_name="课程")
    active = models.ForeignKey("Activity", on_delete=models.DO_NOTHING, related_name="activecourses",
                               verbose_name="活动")
    discount = models.ForeignKey("CourseDiscount", on_delete=models.CASCADE, related_name="discountcourse",
                                 verbose_name="优惠折扣")

    class Meta:
        db_table = "sk_course_price_discount"
        verbose_name = "课程与优惠策略的关系表"
        verbose_name_plural = "课程与优惠策略的关系表"

    def __str__(self):
        return "课程：%s，优惠活动: %s,开始时间:%s,结束时间:%s" % (
            self.course.name, self.active.name, self.active.start_time, self.active.end_time)


class CourseExpire(BaseModel):
    """课程有效期的勾选"""
    # 后面必须在数据库中把course和expire_time字段设置为联合索引
    course = models.ForeignKey("Course", related_name="course_expire", on_delete=models.CASCADE,
                               verbose_name="课程名称")
    expire_time = models.IntegerField(verbose_name="有效期数值", null=True, blank=True)
    expire_text = models.CharField(max_length=150, verbose_name="有效期提示文本", null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程价格", default=0)

    class Meta:
        db_table = "sk_course_expire"
        verbose_name = "课程有效期选项"
        verbose_name_plural = "课程有效期选项"

    def __str__(self):
        return "课程:%s, 有效期: %s, 价格:%s" % (self.course, self.expire_text, self.price)
