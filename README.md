# skylark_yun
### 前后端不分离网页项目:

**前端使用WebStorm IDE -> Vue框架**

**后端使用Pycharm IDE -> Django框架**

**数据库使用MySQL和Redis**



### 启动指令：

1. 要先启动mysql数据库服务
2. 还需启动redis服务
3. 注册时后端需要启动celery服务:celery -A mycelery.main worker -l info -P eventlet
   后端运行指令: python manage.py runserver
   前端运行指令: npm run serve

### 注意:
  skylark_yun\skylark_api\skylark_api\apps需要设置成源目录

### 依赖包安装：

**后端：**

pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple/

pip install PymySQL  -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install Pillow  -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install django-redis  -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install django-cors-headers  -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install django-simpleui  -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install djangorestframework-simplejwt -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip3 install --upgrade tencentcloud-sdk-python  -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip3 install -U "celery[redis]" -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install eventlet -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install django-filter -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

pip install django-ckeditor-5 -i https://pypi.tuna.tsinghua.edu.cn/simple/ 



**前端：**

npm install vue-router@3 -S

npm i element-ui -S

npm i axios -S

npm install vuex@3

### 感受和体验：
只是简单的运用Vue和Django框架进行网页的学习，还有很多功能尚未完善，如支付功能等。本项目仅供参考，大家可以借鉴学习。在使用的过程中，skylark_yun\skylark_api\skylark_api\settings\dev.py文件是本地运行配置文件，大家需要根据自己的情况进行配置。如果有什么问题，请随时交流学习，大家共同进步。
