<template>
  <div class="header-box">
    <div class="header">
      <div class="content">
        <!-- Logo -->
        <div class="logo full-left">
          <router-link to="/"><img src="../../../public/static/image/logo.png" alt="Logo"></router-link>
        </div>

        <!-- 导航栏 -->
        <ul class="nav full-left">
          <li v-for="nav in nav_list" :key="nav.id">
            <span v-if="nav.is_site">
              <a :href="nav.link">{{ nav.title }}</a>
            </span>
            <span v-else>
              <router-link :to="nav.link">{{ nav.title }}</router-link>
            </span>
          </li>
        </ul>

        <!-- 登录状态判断 -->
        <div v-if="token" class="login-bar full-right">
          <!-- 购物车 -->
          <div class="shop-cart full-left">
            <span class="shop-cart-total">{{ cartLength }}</span>
            <img src="/static/image/cart.svg" alt="购物车">
            <span><router-link to="/cart">购物车</router-link></span>
          </div>

          <!-- 用户菜单 -->
          <div class="login-box login-box1 full-left">
            <router-link to="">学习中心</router-link>
            <el-menu width="200" class="member el-menu-demo" mode="horizontal">
              <el-submenu index="2">
                <template slot="title">
                  <img src="/static/image/logo@2x.png" alt="用户头像">
                </template>
                <el-menu-item index="2-1">我的账户</el-menu-item>
                <router-link to="/order"><el-menu-item index="2-2">我的订单</el-menu-item></router-link>

                <el-menu-item index="2-3">我的优惠卷</el-menu-item>
                <el-menu-item index="2-4" @click="logout">退出登录</el-menu-item>
              </el-submenu>
            </el-menu>
          </div>
        </div>

        <!-- 未登录状态 -->
        <div v-else class="login-bar full-right">
          <!-- 购物车 -->
          <div class="shop-cart full-left">
            <img src="../../../public/static/image/cart.svg" alt="购物车">
            <span><router-link to="/cart">购物车</router-link></span>
          </div>

          <!-- 登录和注册 -->
          <div class="login-box full-left">
            <router-link to="/user/login">登录</router-link>
            &nbsp;|&nbsp;
            <span class="header-register"><router-link to="/user/reg">注册</router-link></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "HeaderComp",
  data() {
    return {
      token: null, // 登录状态标识
      nav_list: []
    };
  },
  computed: {
    cartLength(){
      return this.$store.state.cart.cart_length;  // 访问vuex中购物车的数量
    }
  },
  created() {
    this.get_nav(); //获取导航数据
    this.checkLoginStatus(); // 检查登陆状态
    this.fetchCartLength();
  },
  methods: {
    // 获取导航数据
    get_nav() {
      this.$axios.get(`${this.$settings.HOST}/home/nav/header`, {}).then(res => {
        this.nav_list = res.data;
      }).catch(error => {
        console.error("获取导航数据失败:", error);
      });
    },

    //  检查登陆状态
    checkLoginStatus(){
      this.token = localStorage.token || sessionStorage.token
    },

    // 获取购物车数量
    fetchCartLength() {
      this.$store.dispatch('fetchCartLength');
    },

    //  退出登陆
    logout(){
      // 清除本地/会话存储
      localStorage.removeItem('token');
      localStorage.removeItem('refresh');
      localStorage.removeItem('id');

      sessionStorage.removeItem('token');
      sessionStorage.removeItem('refresh');
      sessionStorage.removeItem('id');
      // 更新登陆状态
      this.token = null;

      // 退出登录时清空购物车数量
      this.$store.commit('set_cart_length', 0);
    }
  }
};
</script>
<style scoped>
.header-box {
  height: 60px;
}

.header {
  width: 100%;
  height: 60px;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  margin: auto;
  z-index: 99;
  background: #fff;
}

.header .content {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 100%; /* 确保内容区域高度与 header 一致 */
}

.header .content .logo {
  height: 60px;
  line-height: 60px;
  margin-right: 50px;
  cursor: pointer;
}

.header .content .logo img {
  vertical-align: middle;
  height: 40px;
  transition: transform 0.3s ease;
}

.header .content .logo img:hover {
  transform: scale(1.1); /* 悬停时放大 Logo */
}

/* 导航栏样式 */
.nav {
  display: flex;
  align-items: center;
  justify-content: center; /* 导航栏内容居中 */
  flex-grow: 1; /* 让导航栏占据剩余空间 */
  margin: 0 auto; /* 水平居中 */
}

.nav li {
  margin-right: 20px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
  transition: color 0.3s ease;
}

.nav li:hover {
  color: #6a11cb;
}

.nav li .this {
  color: #6a11cb;
  border-bottom: 2px solid #6a11cb;
}

/* 登录状态判断 */
.login-bar {
  display: flex;
  align-items: center;
  height: 100%; /* 确保高度与 header 一致 */
}

/* 购物车部分样式 */
.shop-cart {
  margin-right: 20px;
  border-radius: 20px; /* 缩小圆角 */
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); /* 渐变背景 */
  cursor: pointer;
  font-size: 12px; /* 缩小字体大小 */
  height: 32px; /* 缩小高度 */
  width: 100px; /* 缩小宽度 */
  line-height: 32px; /* 调整行高 */
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.shop-cart:hover {
  background: linear-gradient(135deg, #2575fc 0%, #6a11cb 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.shop-cart img {
  width: 16px; /* 缩小图标大小 */
  height: 16px; /* 缩小图标大小 */
  vertical-align: middle;
  margin-right: 6px; /* 调整图标与文字的间距 */
  filter: brightness(0) invert(1); /* 使图标变为白色 */
}

.shop-cart span {
  color: #fff;
  font-weight: 500;
}

.shop-cart-total {
  position: absolute;
  top: -6px; /* 调整位置 */
  right: -6px; /* 调整位置 */
  background: #ff4757;
  color: #fff;
  font-size: 10px; /* 缩小字体大小 */
  font-weight: bold;
  padding: 3px 6px; /* 缩小内边距 */
  border-radius: 50%;
  min-width: 18px; /* 缩小最小宽度 */
  text-align: center;
  line-height: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 登录和注册按钮样式 */
.login-box {
  margin-left: 20px; /* 与购物车保持间距 */
}

.login-box a {
  color: #4a4a4a;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.3s ease;
  padding: 8px 12px;
  border-radius: 20px;
}

.login-box a:hover {
  color: #6a11cb;
  background: rgba(106, 17, 203, 0.1); /* 悬停时添加背景色 */
}

/* 用户菜单样式 */
.member {
  display: inline-block;
  height: 40px;
  margin-left: 20px;
}

.member img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: inline-block;
  transition: transform 0.3s ease;
}

.member img:hover {
  transform: scale(1.1);
  border: 2px solid #6a11cb;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header .content {
    padding: 0 10px;
  }

  .nav {
    display: none; /* 在小屏幕上隐藏导航栏 */
  }

  .shop-cart {
    width: auto;
    padding: 0 15px;
  }

  .shop-cart img {
    margin-right: 5px;
  }

  .shop-cart span {
    display: none; /* 在小屏幕上隐藏“购物车”文字 */
  }

  .login-box {
    margin-top: 15px;
  }

  .login-box a {
    padding: 6px 10px;
    font-size: 14px;
  }
}
</style>