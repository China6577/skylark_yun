from django.contrib import admin
from .models import Order, OrderDetail

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_title', 'total_price', 'real_price', 'order_number', 'order_status',
                   'pay_type', 'pay_time', 'user')
    list_filter = ('order_status', 'pay_type', 'pay_time')  # 添加更多筛选选项
    search_fields = ('order_number', 'order_title', 'user__username')  # 添加用户名搜索
    date_hierarchy = 'pay_time'  # 添加日期层级导航
    readonly_fields = ('order_number', 'pay_time')  # 设置只读字段
    list_per_page = 20  # 每页显示数量

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'course', 'expire', 'price', 'real_price', 'discount_name')
    list_filter = ('expire', 'discount_name')  # 优化筛选选项
    search_fields = ('order__order_number', 'course__name', 'discount_name')  # 添加关联字段搜索
    list_per_page = 20
