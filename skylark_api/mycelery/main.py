import os
from celery import Celery

# 设置Django的默认设置模块:不然无法找到Django模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylark_api.settings.dev')

# 创建Celery实例
app = Celery("skylark")

# 从Django的设置文件中加载Celery配置
app.config_from_object('mycelery.config')

# 自动发现任务
app.autodiscover_tasks(['mycelery.sms'])