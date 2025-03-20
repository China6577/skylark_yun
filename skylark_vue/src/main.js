import Vue from 'vue'
import App from './App.vue'
import router from './routers';
import "../public/static/css/reset.css";
Vue.config.productionTip = false

// 导入配置文件
import settings from "./settings"
Vue.prototype.$settings = settings;

// elementUI 导入
import ElementUI from 'element-ui';
// 导入element-ui
import 'element-ui/lib/theme-chalk/index.css';
// 调用插件
Vue.use(ElementUI);

import axios from 'axios'; // 从node_modules目录中导入包
// 允许ajax发送请求时附带cookie
axios.defaults.withCredentials = false;

Vue.prototype.$axios = axios; // 把对象挂载vue中

import VueVideoPlayer from 'vue-video-player';
import 'video.js/dist/video-js.css';  // 引入 video.js 的样式
import store from "@/store";  // 将store挂载上去

Vue.use(VueVideoPlayer);


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: (h) => h(App), // 使用 render 函数
});