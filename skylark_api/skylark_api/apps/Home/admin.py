from django.contrib import admin
from .models import Banner
from .models import Nav

# 管理站点标题
admin.site.site_title = '好课优选'
# 站点头部
admin.site.site_header = '天雀云课堂后台管理系统'
admin.site.index_title = '天雀云课堂后台管理系统'


# 注册模型
class BannerInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_url', 'orders', 'is_show']  # 显示的字段
    list_filter = ['is_show']  # 过滤字段
    search_fields = ['title']  # 搜索字段

# 注册到admin中 和@admin.register(Banner)的作用一样
admin.site.register(Banner, BannerInfoAdmin)


# 导航菜单

class NavModelAdmin(admin.ModelAdmin):
    list_display = ["title", "position", "is_show", "is_site", "link"]
    search_fields = ['title']  # 搜索字段
    list_filter = ['is_show']  # 过滤字段


admin.site.register(Nav, NavModelAdmin)
