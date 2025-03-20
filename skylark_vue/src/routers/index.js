import Vue from "vue"
import Router from "vue-router"


// 这里导入可以让让用户访问的组件
import Home from "../components/Home"
import Login from "../components/Login"
import Register from "../components/Register"
import Course from "../components/Course"
import Detail from "../components/Detail"
import Cart from "@/components/Cart.vue";
// import AliPlayer from "../components/AliPlayer.vue";

Vue.use(Router);

export default new Router({
    // 设置路由模式为‘history’，去掉默认的#
    mode: "history",
    routes: [
        // 路由列表
        {
            name: "Home",
            path: "/",
            component: Home,
        }, {
            name: "HomePage",
            path: "/home",
            component: Home,
        },{
            name: "Login",
            path: "/user/login",
            component: Login,
        },{
            name: "Register",
            path: "/user/reg",
            component: Register,
        }, {
            path: '/course',
            name: 'Course',
            component: Course,
        }, {
            path: '/course/detail/:id',
            name: 'Detail',
            component: Detail,
        }, {
            path: '/cart',
            name: 'Cart',
            component: Cart,
        },
    ]
})
