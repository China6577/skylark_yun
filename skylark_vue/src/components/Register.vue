<template>
  <div class="box">
    <img src="../../public/static/image/Loginbg.3377d0c.jpg" alt="">
    <div class="register">
      <div class="register_box">
        <div class="register-title">注册好课优选</div>
        <div class="inp">
          <input v-model="phone" type="text" @blur="checkPhone" placeholder="手机号码" class="user">
          <!-- @blur是当失去焦点时调用函数 -->
          <input v-model="password" type="password" placeholder="登录密码" class="user">
          <div class="sms-box">
            <input v-model="sms_code" maxlength="6" type="text" placeholder="短信验证码" class="user"
                   @keyup.enter="registerHandler">
            <div class="sms-btn" @click="smsHandler" disabled="is_send_sms">
              {{ sms_text }}
            </div>
            <div id="gee test"></div>
            <button class="register_btn" @click="registerHandler">注册</button>
            <p class="go_login">已有账号
              <router-link to="/user/login"><span>直接登录</span></router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterComponent',
  data() {
    return {
      sms_code: "",
      phone: "",
      password: "",
      is_send_sms: false, // 是否已发送短信
      sms_text: "点击发送短信", // 短信按钮文本
    }
  },
  created() {
  },
  methods: {
    checkPhone() {
      // 判断不符合11位数字的号码验证
      if (this.phone.length !== 11 || !/^1[3-9]\d{9}$/.test(this.phone)) {
        this.$message.error("手机号码格式不正确！")
        return false
      }

      // 检查手机号的合法性[格式和是否已经注册]
      this.$axios.get(`${this.$settings.HOST}/user/phone/${this.phone}/`).catch(error => {
        this.$message.error(error.response.data.message);
      });
    },
    registerHandler() {
      // 用户注册
      // post请求以键值对形式传入 键必须是之前定义好的字段 如mobile
      this.$axios.post(`${this.$settings.HOST}/user/`, {
        mobile: this.phone,
        sms_code: this.sms_code,
        password: this.password,
      }).then(response => {
        // 注册成功 则移除原来登录状态 并将创建好的账号登录状态存入session中
        localStorage.removeItem("user_token");
        localStorage.removeItem("user_id");
        localStorage.removeItem("user_name");
        sessionStorage.token = response.data.token;
        sessionStorage.id = response.data.id;
        sessionStorage.username = response.data.username;
        // 页面跳转
        let self = this;
        this.$alert("注册成功!", "好课优选", {
          callback() {
            self.$router.push("/");
          }
        });
      }).catch(error => {
        let data = error.response.data;
        let message = "";
        for (let key in data) {
          message = data[key][0];
        }
        this.$message.error(message);
      });
    },
    smsHandler() {
      // 发送短信
      // 1. 检查手机格式
      if (!/1[3-9]\d{9}/.test(this.phone)) {
        this.$message.error("手机号码格式不正确！");
        return false;
      }

      // 2. 判断手机号码是否60s内发送短信
      if (this.is_send_sms) {
        this.$message.error("当前手机号已经在60秒内发送过短信，请不要频繁发送！");
        return false;
      }

      // 3. 发送ajax
      this.$axios.get(`${this.$settings.HOST}/user/sms/${this.phone}/`).then(() => {

        this.is_send_sms = true; // 开始倒计时
        let interval_time = 60; // 倒计时时间（秒）

        // 提示验证码已发送
        this.$message.success("验证码已发送，请注意查收！");

        // 倒计时逻辑
        let timer = setInterval(() => {
          if (interval_time <= 1) {
            clearInterval(timer); // 停止倒计时
            this.is_send_sms = false; // 允许重新发送
            this.sms_text = "点击发送短信"; // 恢复按钮文本
          } else {
            interval_time--;
            this.sms_text = `${interval_time}秒后重新发送`; // 更新按钮文本
          }
        }, 1000);
      }).catch(error => {
        this.$message.error(error.response.data.message); // 显示错误信息
      });
    },
  },
};
</script>

<style scoped>
.box {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: 'Arial', sans-serif;
}

.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
  filter: brightness(80%);
}

.register {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  padding: 30px 25px;
}

.register-title {
  font-size: 28px;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  font-weight: 700;
  letter-spacing: 1px;
}

.inp {
  width: 100%;
}

.inp input {
  width: 100%;
  height: 50px;
  margin-bottom: 16px;
  padding: 10px 15px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  background: #f9f9f9;
}

.inp input:focus {
  border-color: #84cc39;
  box-shadow: 0 0 8px rgba(132, 204, 57, 0.5);
  background: #fff;
}

.sms-box {
  position: relative;
}

.sms-box .sms-btn {
  position: absolute;
  font-size: 14px;
  letter-spacing: 0.26px;
  top: 10px;
  right: 16px;
  border-left: 1px solid #484848;
  padding-left: 16px;
  padding-bottom: 4px;
  cursor: pointer;
  background: #ffffff;
  color: #84cc39;
  transition: color 0.3s ease;
}

.sms-box .sms-btn:hover {
  color: #5a9924;
}

.sms-box .sms-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.register_btn {
  width: 100%;
  height: 50px;
  background: linear-gradient(45deg, #84cc39, #76b335);
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(132, 204, 57, 0.4);
}

.register_btn:hover {
  background: linear-gradient(45deg, #76b335, #5a9924);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(132, 204, 57, 0.6);
}

.register_btn:active {
  transform: translateY(1px);
}

.go_login {
  text-align: center;
  font-size: 14px;
  margin-top: 20px;
  color: #7a7a7a;
}

.go_login a {
  color: #84cc39;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

.go_login a:hover {
  color: #5a9924;
  text-decoration: underline;
}

/* 响应式布局 */
@media (max-width: 600px) {
  .register {
    width: 90%;
    padding: 20px;
  }

  .register-title {
    font-size: 24px;
  }

  .register_btn {
    height: 45px;
    font-size: 16px;
  }
}
</style>