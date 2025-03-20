# skylark_yun
### 前后端不分离项目

skylark_yun/  
   ├── docs/          # 项目相关资料保存目录  
   ├── skylark_vue/     # 前端项目目录  
   ├── skylark_api/      # 后端项目目录  
        ├── logs/          # 项目运行时/开发时日志目录  
        ├── manage.py  
        ├── skylark_api/      # 项目主应用，开发时的代码保存  
        │    ├── apps/      # 开发者的代码保存目录，以模块[子应用]为目录保存  
        │    ├── libs/      # 第三方类库的保存目录[第三方组件、模块]  
        │    ├── settings/  
        │         ├── dev.py   # 项目开发时的本地配置  
        │         ├── prod.py  # 项目上线时的运行配置  
        │    ├── urls.py    # 总路由  
        │    ├── utils/     # 多个模块[子应用]的公共函数类库[自己开发的组件]  
        └── scripts/       # 保存项目运行时的脚本文件  
