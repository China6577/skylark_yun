<template>
  <div class="success">
    <Header/>
    <div class="main">
      <div class="title">
        <!--          <img src="../../static/images/right.svg" alt="">-->
        <div class="success-tips">
          <p class="tips1">您已成功购买 {{order_info.course_list.length}} 门课程！</p>
          <p class="tips2">你还可以加入QQ群 <span>747556033</span> 学习交流</p>
        </div>
      </div>
      <div class="order-info">
        <p class="info1"><b>付款时间：</b><span>{{order_info.pay_time}}</span></p>
        <p class="info2"><b>付款金额：</b><span >￥{{order_info.real_price}}元</span></p>
        <p class="info3"><b>课程信息：</b><span><span>{{order_info.course_list2}}</span></span></p>
      </div>
      <div class="wechat-code">
        <!--          <img src="../../static/images/server.cf99f78.png" alt="" class="er">-->
        <!--          <p><img src="../../static/images/tan.svg" alt="">重要！微信扫码关注获得学习通知&amp;课程更新提醒！否则将严重影响学习进度和课程体验！</p>-->
      </div>
      <div class="study">
        <span>立即学习</span>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"
export default{
  name:"SuccessComp",
  data(){
    return {
      order_info:{
        course_list:[]
      }
    };
  },
  created(){
    let token = localStorage.token || sessionStorage.token;

    if(!token){
      this.$alert("对不起,您尚未登录!请登录!","警告",{
        callback(){
          this.$router.push("/login");
        }
      })
    }

    // 转发支付结果到后端
    this.$axios.get(this.$settings.HOST+"/payments/alipay/result/"+location.search,{
      headers:{
        // 注意下方的空格!!!
        Authorization: `Bearer ${this.token}`
      },
    }).then(response=>{
      this.order_info = response.data.message;
      this.order_info.course_list2 = "";
      this.order_info.course_list.forEach(course=>{
        this.order_info.course_list2+=`《${course}》`;
      })
    }).catch(error=>{

      console.log(error.response);
    })
  },
  components:{
    Header,
    Footer,
  }
}
</script>

<style scoped>
.success{
  padding-top: 80px;
}
.main{
  height: 100%;
  padding-top: 25px;
  padding-bottom: 25px;
  margin: 0 auto;
  width: 1200px;
  background: #fff;
}
.main .title{
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding: 25px 40px;
  border-bottom: 1px solid #f2f2f2;
}
.main .title .success-tips{
  box-sizing: border-box;
}
.title img{
  vertical-align: middle;
  width: 60px;
  height: 60px;
  margin-right: 40px;
}
.title .success-tips{
  box-sizing: border-box;
}
.title .tips1{
  font-size: 22px;
  color: #000;
}
.title .tips2{
  font-size: 16px;
  color: #4a4a4a;
  letter-spacing: 0;
  text-align: center;
  margin-top: 10px;
}
.title .tips2 span{
  color: #ec6730;
}
.order-info{
  padding: 25px 48px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f2f2f2;
}
.order-info p{
  font-family: PingFangSC-Regular;
  display: -ms-flexbox;
  display: flex;
  margin-bottom: 10px;
  font-size: 16px;
}
.order-info p b{
  font-weight: 400;
  color: #9d9d9d;
  white-space: nowrap;
}
.wechat-code{
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding: 25px 40px;
  border-bottom: 1px solid #f2f2f2;
}
.wechat-code>img{
  width: 100px;
  height: 100px;
  margin-right: 15px;
}
.wechat-code p{
  font-family: PingFangSC-Regular;
  font-size: 14px;
  color: #d0021b;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}
.wechat-code p>img{
  width: 16px;
  height: 16px;
  margin-right: 10px;
}
.study{
  padding: 25px 40px;
}
.study span{
  display: block;
  width: 140px;
  height: 42px;
  text-align: center;
  line-height: 42px;
  cursor: pointer;
  background: #ffc210;
  border-radius: 6px;
  font-family: PingFangSC-Regular;
  font-size: 16px;
  color: #fff;
}
</style>