from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    """优惠券模型管理类"""
    list_display = ["name", "coupon_type", "timer"]

from .models import UserCoupon

@admin.register(UserCoupon)
class UserCouponModelAdmin(admin.ModelAdmin):
    """我的优惠券模型管理类"""
    list_display = ["user", "coupon", "start_time", "is_use"]
