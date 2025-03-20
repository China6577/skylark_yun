<template>
  <div class="detail">
    <Header></Header>
    <div class="main">
      <div class="course-info">
        <div class="wrap-left">
          <!-- 播放器配置 -->
          <video-player
              class="video-player vjs-custom-skin"
              ref="videoPlayer"
              :playsinline="true"
              :options="playerOptions"
              @play="onPlayerPlay($event)"
              @pause="onPlayerPause($event)"
          ></video-player>
        </div>
        <div class="wrap-right">
          <h3 class="course-name">{{ course.name }}</h3>
          <p class="data">{{ course.students }}人在学&nbsp;&nbsp;&nbsp;&nbsp;课程总时长：{{ course.lessons }}
            课时/{{ course.pub_lessons === course.lessons ? '更新完成' : `已更新${course.pub_lessons}课时` }}
            &nbsp;&nbsp;&nbsp;&nbsp;难度：{{ course.level_name }}</p>
          <div class="sale-time">
            <p class="sale-type">{{course.discount_name}}</p>
            <p class="expire">
              <!-- 过滤器的使用 -->
              距离结束：仅剩 {{ course.activity_time | format_countdown }}
            </p>
          </div>
          <p class="course-price">
            <span>活动价</span>
            <span class="discount">{{ course.real_price }}</span>
            <span class="original">{{ course.price }}</span>
          </p>
          <div class="buy">
            <div class="buy-btn">
              <button class="buy-now">立即购买</button>
              <button class="free">免费试学</button>
            </div>
            <div class="add-cart" @click="addCart"><img src="../../public/static/image/cart-yellow.svg" alt="">加入购物车</div>
          </div>
        </div>
      </div>
      <div class="course-tab">
        <ul class="tab-list">
          <li :class="tabIndex===1?'active':''" @click="tabIndex=1">详情介绍</li>
          <li :class="tabIndex===2?'active':''" @click="tabIndex=2">课程章节<span
              :class="tabIndex!==2?'free':''">(试学)</span></li>
          <li :class="tabIndex===3?'active':''" @click="tabIndex=3">用户评论 (42)</li>
          <li :class="tabIndex===4?'active':''" @click="tabIndex=4">常见问题</li>
        </ul>
      </div>
      <div class="course-content">
        <div class="course-tab-list">

          <!-- 详情页数据 -->
          <div class="tab-item" v-if="tabIndex===1">
            <div v-html="course.brief_html"></div>
          </div>

          <div class="tab-item" v-if="tabIndex===2">

            <div class="tab-item-title">
              <p class="chapter">课程章节</p>
              <p class="chapter-length">共{{ chapter_list.length }}章 {{ course.lessons }}个课时</p>
            </div>

            <div class="chapter-item" v-for="chapter in chapter_list" :key="chapter.id">
              <p class="chapter-title"><img src="../../public/static/image/1.png"
                                            alt="">第{{ chapter.chapter }}章·{{ chapter.name }}</p>
              <ul class="lesson-list">
                <li class="lesson-item" v-for="(lesson, index) in chapter.coursesections" :key="lesson.id">
                  <p class="name"><span class="index">{{ chapter.chapter }}-{{ index + 1 }}</span> {{ lesson.name }}
                    <span class="free" v-if="lesson.free_trail">免费</span>
                  </p>
                  <p class="time">07:30 <img src="../../public/static/image/chapter-player.svg" alt=""></p>
                  <button class="try" v-if="lesson.free_trail">立即试学</button>
                  <button class="try" v-else>立即购买</button>
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

export default {
  name: "DetailComp",
  data() {
    return {
      tabIndex: 2,
      course_id: 0,
      course: {
        teacher: {} //存储教师信息
      },
      chapter_list: [],//章节数据
      // 播放器配置
      playerOptions: {
        playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
        autoplay: false, // 自动播放
        muted: false, // 静音
        loop: false, // 循环播放
        preload: 'auto', // 预加载
        language: 'zh-CN', // 语言
        aspectRatio: '16:9', // 视频比例
        fluid: true, // 自适应容器大小
        sources: [
          {
            type: 'video/mp4', // 视频格式
            src: 'https://video.hkaiyun.com/EXCEL/%E5%9B%BE%E8%A1%A8%E7%BE%8E%E5%8C%96.mp4', // 视频地址
          },
        ],
        poster: 'https://video.hkaiyun.com/EXCEL/excel.jpg', // 封面图
        notSupportedMessage: '此视频暂无法播放，请稍后再试', // 不支持播放时的提示
      },
    }
  },
  created() {
    // 课程ID
    this.get_course_id();
    this.get_course_info();
    this.get_course_chapter();
  },

  filters: {
    format_countdown(seconds) {
      // 辅助函数 将时间转换为二位数
      const time_format = (time) => {
        time = parseInt(time, 10);
        return time < 10 ? "0" + time : time;
      };
      // 将时间戳转换为小时分钟秒的二位数格式
      seconds = Math.floor(seconds);
      const days = Math.floor(seconds / (24 * 3600));
      const hours = Math.floor((seconds % (24 * 3600)) / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      return `${days}天 ${time_format(hours)}小时 ${time_format(minutes)}分 ${time_format(secs)}秒`;
    },
  },

  methods: {
    get_course_id() {
      // 从路径参数(url)中获得课程id 如http://localhost:8080/course/detail/29 则course_id为29
      let course_id = this.$route.params.id;
      if (course_id > 0) {
        this.course_id = parseInt(course_id);
      } else {
        let self = this;
        this.$alert("对不起，访问页面参数有误！", "错误", {
          callback() {
            self.$router.go(-1);
          }
        });
        return false;
      }
      return course_id;
    },

    // 获取课程详情页
    get_course_info() {
      this.$axios
          .get(`${this.$settings.HOST}/course/${this.course_id}/`)
          .then((response) => {
            this.course = response.data;
            // 替换视频源
            this.playerOptions.sources[0].src = response.data.course_video;
            this.playerOptions.poster = response.data.course_img;
            // 设置活动进行时，课程优惠的倒计时
            // 倒计时的每一秒刷新显示
            if(this.course.activity_time > 0){
              let timer = setInterval(()=>{
                if( this.course.activity_time > 1 ){
                  this.course.activity_time-=1;
                }else{
                  clearInterval(timer);
                }
              },1000)}
          })
    },

    // 获取章节课时内容
    get_course_chapter() {
      //   获取当前课程的章节信息
      this.$axios.get(`${this.$settings.HOST}/course/chapter/`, {
        params: {
          course: this.course_id
        }
      }).then(response => {
        this.chapter_list = response.data
        console.log(response.data)
      })
    },

    // 判断用户是否登陆
    check_user_login() {
      let token = localStorage.token || sessionStorage.token;
      if (!token) {
        let self = this;
        self.$confirm("您尚未登陆！请登陆后再添加购物车", "好课优选", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$router.push('/user/login');
        }).catch(() => {
          // 代码不再继续往下执行
          return false;
        })
      }
      return token;
    },

    // 添加到购物车
    addCart() {
      //   添加商品必须用户已经登陆了
      let token = this.check_user_login();
      // 如果未登陆，直接返回，不再执行后续的代码
      if (!token) {
        return;
      }
      //   添加商品到购物车
      this.$axios.post(`${this.$settings.HOST}/cart/`, {
            course_id: this.course_id,
          }, {
            headers: {
              //   提交token的时候，当前token类型是Bearer生成的，所以中间必须要有一个空格
              "Authorization": `Bearer ${token}`
            }
          }
      ).then(response => {
        this.$message.success(response.data.message);
        // 更新到购物车总数
        this.$store.state.cart.cart_length=response.data.cart_length
      })
    },

    onPlayerPlay(event) {
      console.log('视频开始播放', event);
      // 可以在这里添加播放时的逻辑，比如关闭广告
    },

    onPlayerPause(event) {
      console.log('视频暂停', event);
      // 可以在这里添加暂停时的逻辑，比如显示广告
    },
  },
  components: {
    Header,
    Footer,
  }
}
</script>

<style scoped>
.main {
  background: #fff;
  padding-top: 30px;
}

.course-info {
  width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}

.wrap-left {
  float: left;
  width: 690px;
  height: 388px;
  background-color: #000;
}

.wrap-right {
  float: left;
  position: relative;
  height: 388px;
}

.course-name {
  font-size: 20px;
  color: #333;
  padding: 10px 23px;
  letter-spacing: .45px;
}

.data {
  padding-left: 23px;
  padding-right: 23px;
  padding-bottom: 16px;
  font-size: 14px;
  color: #9b9b9b;
}

.sale-time {
  width: 464px;
  background: #fa6240;
  font-size: 14px;
  color: #4a4a4a;
  padding: 10px 23px;
  overflow: hidden;
}

.sale-type {
  font-size: 16px;
  color: #fff;
  letter-spacing: .36px;
  float: left;
}

.sale-time .expire {
  font-size: 14px;
  color: #fff;
  float: right;
}

.sale-time .expire .second {
  width: 24px;
  display: inline-block;
  background: #fafafa;
  color: #5e5e5e;
  padding: 6px 0;
  text-align: center;
}

.course-price {
  background: #fff;
  font-size: 14px;
  color: #4a4a4a;
  padding: 5px 23px;
}

.discount {
  font-size: 26px;
  color: #fa6240;
  margin-left: 10px;
  display: inline-block;
  margin-bottom: -5px;
}

.original {
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  text-decoration: line-through;
}

.buy {
  width: 464px;
  padding: 0px 23px;
  position: absolute;
  left: 0;
  bottom: 20px;
  overflow: hidden;
}

.buy .buy-btn {
  float: left;
}

.buy .buy-now {
  width: 125px;
  height: 40px;
  border: 0;
  background: #ffc210;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-right: 15px;
  outline: none;
}

.buy .free {
  width: 125px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  background: #fff;
  color: #ffc210;
  border: 1px solid #ffc210;
}

.add-cart {
  float: right;
  font-size: 14px;
  color: #ffc210;
  text-align: center;
  cursor: pointer;
  margin-top: 10px;
}

.add-cart img {
  width: 20px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.course-tab {
  width: 100%;
  background: #fff;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px 0 #f0f0f0;

}

.course-tab .tab-list {
  width: 1200px;
  margin: auto;
  color: #4a4a4a;
  overflow: hidden;
}

.tab-list li {
  float: left;
  margin-right: 15px;
  padding: 26px 20px 16px;
  font-size: 17px;
  cursor: pointer;
}

.tab-list .active {
  color: #ffc210;
  border-bottom: 2px solid #ffc210;
}

.tab-list .free {
  color: #fb7c55;
}

.course-content {
  width: 1200px;
  margin: 0 auto;
  background: #FAFAFA;
  overflow: hidden;
  padding-bottom: 40px;
}

.course-tab-list {
  width: 880px;
  height: auto;
  padding: 20px;
  background: #fff;
  float: left;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.tab-item {
  width: 880px;
  background: #fff;
  padding-bottom: 20px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.tab-item-title {
  justify-content: space-between;
  padding: 25px 20px 11px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
  overflow: hidden;
}

.chapter {
  font-size: 17px;
  color: #4a4a4a;
  float: left;
}

.chapter-length {
  float: right;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
}

.chapter-title {
  font-size: 16px;
  color: #4a4a4a;
  letter-spacing: .26px;
  padding: 12px;
  background: #eee;
  border-radius: 2px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}

.chapter-title img {
  width: 18px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.lesson-list {
  padding: 0 20px;
}

.lesson-list .lesson-item {
  padding: 15px 20px 15px 36px;
  cursor: pointer;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.lesson-item .name {
  font-size: 14px;
  color: #666;
  float: left;
}

.lesson-item .index {
  margin-right: 5px;
}

.lesson-item .free {
  font-size: 12px;
  color: #fff;
  letter-spacing: .19px;
  background: #ffc210;
  border-radius: 100px;
  padding: 1px 9px;
  margin-left: 10px;
}

.lesson-item .time {
  font-size: 14px;
  color: #666;
  letter-spacing: .23px;
  opacity: 1;
  transition: all .15s ease-in-out;
  float: right;
}

.lesson-item .time img {
  width: 18px;
  height: 18px;
  margin-left: 15px;
  vertical-align: text-bottom;
}

.lesson-item .try {
  width: 86px;
  height: 28px;
  background: #ffc210;
  border-radius: 4px;
  font-size: 14px;
  color: #fff;
  position: absolute;
  right: 20px;
  top: 10px;
  opacity: 0;
  transition: all .2s ease-in-out;
  cursor: pointer;
  outline: none;
  border: none;
}

.lesson-item:hover {
  background: #fcf7ef;
  box-shadow: 0 0 0 0 #f3f3f3;
}

.lesson-item:hover .name {
  color: #333;
}

.lesson-item:hover .try {
  opacity: 1;
}

.course-side {
  width: 300px;
  height: auto;
  margin-left: 20px;
  float: right;
}

.teacher-info {
  background: #fff;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.side-title {
  font-weight: normal;
  font-size: 17px;
  color: #4a4a4a;
  padding: 18px 14px;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
}

.side-title span {
  display: inline-block;
  border-left: 2px solid #ffc210;
  padding-left: 12px;
}

.teacher-content {
  padding: 30px 20px;
  box-sizing: border-box;
}

.teacher-content .cont1 {
  margin-bottom: 12px;
  overflow: hidden;
}

.teacher-content .cont1 img {
  width: 54px;
  height: 54px;
  margin-right: 12px;
  float: left;
}

.teacher-content .cont1 .name {
  float: right;
}

.teacher-content .cont1 .teacher-name {
  width: 188px;
  font-size: 16px;
  color: #4a4a4a;
  padding-bottom: 4px;
}

.teacher-content .cont1 .teacher-title {
  width: 188px;
  font-size: 13px;
  color: #9b9b9b;
  white-space: nowrap;
}

.teacher-content .narrative {
  font-size: 14px;
  color: #666;
  line-height: 24px;
}
</style>