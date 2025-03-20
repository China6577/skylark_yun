<template>
  <div class="login box">
    <video autoplay src="../../public/static/video/background.mp4" loop></video>
    <div class="login">
      <div class="login-title">
        <img src="../../public/static/image/Logotitle.png" alt="">
        <p>一朵云推动另一朵云,一个灵魂唤醒另一个灵魂.</p>
      </div>
      <div class="login_box">
        <div class="title">
          <span @click="login_type=0">密码登录</span>
          <span @click="login_type=1">短信登录</span>
        </div>
        <div class="inp" v-if="login_type===0">
          <input v-model="username" type="text" placeholder="用户名 / 手机号码" class="user">
          <input v-model="password" type="password" name="" class="pwd" placeholder="密码" @keyup.enter="loginHandler">
          <div id="geetest1"></div>
          <div class="rember">
            <p>
              <input type="checkbox" class="no" name="a" v-model="remember"/>
              <span>7天内免登录</span>
            </p>
            <p>忘记密码</p>
          </div>
          <button class="login_btn" @click="loginHandler">登录</button>
          <p class="go_login" >没有账号 <router-link to="/user/reg"><span>立即注册</span></router-link></p>
        </div>
        <div class="inp" v-show="login_type===1">
          <input v-model="username" type="text" placeholder="手机号码" class="user">
          <input v-model="password" type="text" class="pwd" placeholder="短信验证码">
          <button id="get_code">获取验证码</button>
          <button class="login_btn">登录</button>
          <p class="go_login" >没有账号 <router-link to="/user/reg"><span>立即注册</span></router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginComponent',
  data() {
    return {
      login_type: 0,
      remember: false, // 记住密码
      username: "",
      password: "",
    }
  },
  methods: {
    // 登录
    loginHandler() {
      // 获得token：用于登录校验 将token保留到本地 就可以长期保持登录状态
      this.$axios.post(`${this.$settings.HOST}/user/token/`,
          {"username": this.username, "password": this.password}
      ).then(response => {
        // 使用浏览器本地存储保存token
        if (this.remember) {
          // 记住登录
          sessionStorage.clear();
          localStorage.token = response.data.access;  // 长期有效 (本地存储)
          localStorage.refresh = response.data.refresh;
          localStorage.id = response.data.id;
        } else {
          // 未记住登录
          localStorage.clear();
          sessionStorage.token = response.data.access;  // 关闭浏览器token失效
          sessionStorage.refresh = response.data.refresh;
          sessionStorage.id = response.data.id;
        }
        // 登录成功弹窗
        this.$message.success('登录成功！')
        // 页面跳转回到上一个页面 也可以使用 this.$router.push("/") 回到首页
        this.$router.go(-1)
      }).catch(error => {
        this.$message.error('用户名或密码错误，请重新输入！');
        console.log(error)
      })
    }
  },
};
</script>

<style scoped>
/* 全局样式 */
.box {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景视频 */
.box video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

/* 遮罩层 */
.box::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 半透明黑色遮罩 */
  z-index: 2;
}

/* 登录框 */
.box .login {
  position: absolute;
  width: 400px;
  height: auto;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 3;
}

/* 登录标题 */
.login .login-title {
  width: 100%;
  text-align: center;
  margin-bottom: 20px;
}

.login-title img {
  width: 150px;
  height: auto;
}

.login-title p {
  font-family: PingFangSC-Regular;
  font-size: 16px;
  color: #333;
  letter-spacing: 0.29px;
  padding-top: 10px;
}

/* 选项卡 */
.login_box .title {
  font-size: 18px;
  color: #9b9b9b;
  letter-spacing: 0.32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  margin-bottom: 20px;
  cursor: pointer;
}

.login_box .title span {
  padding: 10px 0;
  transition: all 0.3s ease;
}

.login_box .title span.active {
  color: #84cc39;
  border-bottom: 2px solid #84cc39;
}

.login_box .title span:hover {
  color: #84cc39;
}

/* 输入框 */
.inp {
  width: 100%;
}

.inp input {
  border: 0;
  outline: 0;
  width: 100%;
  height: 40px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
  margin-bottom: 15px;
  transition: border-color 0.3s ease;
}

.inp input:focus {
  border-color: #84cc39;
}

/* 记住密码和忘记密码 */
.inp .rember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  font-size: 14px;
  color: #4a4a4a;
}

.inp .rember p:first-of-type {
  display: flex;
  align-items: center;
}

.inp .rember input {
  width: 16px;
  height: 16px;
  margin-right: 5px;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  background: #fff;
  transition: all 0.3s ease;
}

.inp .rember input:hover {
  border-color: #84cc39;
}

.inp .rember span {
  font-size: 14px;
  color: #4a4a4a;
  transition: color 0.3s ease;
}

.inp .rember span:hover {
  color: #84cc39;
}

.inp .rember p:nth-of-type(2) {
  color: #9b9b9b;
  font-size: 14px;
  cursor: pointer;
  margin-left: auto;
}

.inp .rember p:nth-of-type(2):hover {
  color: #4a4a4a;
}

/* 登录按钮 */
.login_btn {
  width: 100%;
  height: 40px;
  background: #84cc39;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  margin-top: 20px;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

.login_btn:hover {
  background: #73b331;
}

/* 注册链接 */
.inp .go_login {
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  margin-top: 15px;
}

.inp .go_login span {
  color: #84cc39;
  cursor: pointer;
  transition: color 0.3s ease;
}

.inp .go_login span:hover {
  color: #73b331;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .box .login {
    width: 90%;
    padding: 20px;
  }

  .login-title img {
    width: 120px;
  }

  .login-title p {
    font-size: 14px;
  }

  .login_box .title {
    font-size: 16px;
  }

  .inp input {
    height: 36px;
    font-size: 13px;
  }

  .login_btn {
    height: 36px;
    font-size: 14px;
  }
}
</style>