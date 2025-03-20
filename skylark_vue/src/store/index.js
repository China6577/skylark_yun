import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import settings from "../settings";

Vue.use(Vuex);


export default new Vuex.Store({
    // 存储应用程序的全局状态
    state: {
        cart: {
            cart_length: 0,
        }
    },
    // 从state中派生出一些状态，类似计算属性
    getters: {},
    // 用于同步修改state的唯一方式
    mutations: {
        // 更新购物车数量
        set_cart_length(state, cart_length) {
            state.cart.cart_length = cart_length;
        },
    },
    // 用于处理异步操作(如api请求),并通过提交给mutation修改state
    // commit是用于触发mutations的方法
    actions: {
        async fetchCartLength({commit}) {
            try {
                const token = localStorage.token || sessionStorage.token;
                // 未登陆用户不获取购物车数量
                if (!token) return;

                // 异步请求
                const response = await axios.get(`${settings.HOST}/cart/`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                });

                commit('set_cart_length', response.data.cart_length)
            } catch (error) {
                console.error("获取购物车数量失败:", error)
            }
        }
    },
    // 将store分割成模块，每个看模块拥有自己的
    modules: {}
})