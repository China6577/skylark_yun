<template>
  <div class="course">
    <Header></Header>
    <div class="main">

      <!-- 筛选条件 -->
      <div class="condition">

        <ul class="cate-list">
          <li class="title">课程分类:</li>
          <!-- 将全部的id默认为0 当点击全部时id=0高亮 -->
          <li
              @click="changeCategory(0)"
              :class="{ this: category === 0 }">
            全部
          </li>
          <!-- 点击高亮处理 从后端传来每一个选项的id值 作为高亮的定位 -->
          <li
              v-for="cat in category_list"
              :key="cat.id"
              @click="changeCategory(cat.id)"
              :class="{ this: category === cat.id }">
            {{ cat.name }}
          </li>
        </ul>

        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选:</li>
            <!-- 点击一下类型则修改一下排序顺序 type从上到下 从0到1 -->
            <!-- :class满足条件则在原class后面加上表达式返回的class值 -->
            <li @click="change_order_type(0)" class="default" :class="change_order_class(0)">默认</li>
            <li @click="change_order_type(1)" class="hot" :class="change_order_class(1)">人气</li>
            <li @click="change_order_type(2)" class="price" :class="change_order_class(2)">价格</li>
          </ul>
          <p class="condition-result">共{{ course_list.length }}个课程</p>
        </div>

      </div>

      <!-- 课程列表 -->
      <div class="course-list">
        <div class="course-item" v-for="course in course_list" :key="course.id">
          <div class="course-image">
            <img :src="course.course_img" :alt="course.name">
          </div>
          <div class="course-info">
            <h3>
              <router-link :to="`/course/detail/${course.id}`">{{ course.name }}</router-link>
              <span>
                <img src="../../public/static/image/avatar1.svg" alt="">{{ course.students }}人已加入学习
              </span>
            </h3>

            <!-- course.lessons是课程总数 course.pub_lessons是已更新课程数量 -->
            <p class="teather-info">{{ course.teacher.name }} {{ course.teacher.signature }} {{ course.teacher.title }}
              <span>
                共{{ course.lessons }}课时/{{ course.lessons === course.pub_lessons ? '更新完成' : `已更新${course.pub_lessons}课时`}}
              </span>
            </p>

            <!-- 每个章节的小课显示 -->
            <ul class="lesson-list">
              <li v-for="(lesson, key) in course.lesson_list" :key="lesson.id">
                <p class="lesson-title">0{{key+1}} | {{lesson.name}}</p>
                <span v-if="lesson.free_trail" class="free">免费</span>
              </li>
            </ul>

            <div class="pay-box">
              <span class="discount-type" v-if="course.discount_name">{{course.discount_name}}</span>
              <span class="discount-price">￥{{course.real_price}}元</span>
              <span class="original-price" v-if="course.discount_name">原价：{{course.price}}元</span>
              <span class="buy-now">立即购买</span>
            </div>

          </div>
        </div>
      </div>
    </div>
    <!-- 分页功能实现 -->
    <!-- :total 左边显示一共几条的数据字段 -->
    <!-- :page-sizes 用户自己选择的分页大小的选项 -->
    <!-- @current-change当前页数发生变化时调用 如下一页上一页操作   -->
    <el-pagination
        background
        layout="total,prev, pager, next, sizes"
        :total="total"
        :page-size="filters.size"
        :page-sizes="[2, 5, 10, 15,20]"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
    >
    </el-pagination>
    <Footer></Footer>
  </div>
</template>


<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

export default {
  name: "CourseComp",
  data() {
    return {
      course_list: [],
      ordering: '-id',// 默认排序字段为id,降序排序
      category: 0,
      category_list: [],
      total: 0, // 用来保存课程总数
      filters: {
        type: 0, // 筛选类型，0表示默认，1表示人气,2表示价格
        orders: "desc",  // 排序类型，desc表示降序，asc表示升序
        page: 1, // 当前页，初始为第1页
        size: 5 //每页显示5条数据
      }
    }
  },

  created() {
    this.get_course_category();
    this.get_course();
  },

  methods: {
    // 获取排序
    get_ordering(){
      let ordering = "";
      if (this.filters.type === 1){
        //   人气排序
        ordering = this.filters.orders === "desc" ? "-students" : "students";
      }else if (this.filters.type === 2){
        // 价格排序
        ordering = this.filters.orders === "desc" ? "-price" : "price";
      }else {
        //   默认排序
        ordering = this.filters.orders === "desc" ? "-id" : "id";
      }
      return  ordering;
    },

    get_course() {
      // 构建请求参数
      let params = {
        page: this.filters.page,
        size: this.filters.size,
      };
      // 只有当分类不为0的时候才添加分类参数
      if (this.category !== 0) {
        params.course_category = this.category
      }
      // 获取排序参数
      params.ordering = this.get_ordering()
      // 发送请求 获得筛选后的课程信息
      this.$axios.get(`${this.$settings.HOST}/course/`, {params}).then(response => {
        this.course_list = response.data.data
        console.log(response.data)
        console.log(this.course_list)
        console.log(response.data)
        //  response.data.count中的count是response.data的一个值 用于记录数据的总数
        this.total = response.data.count
      }).catch(error => {
        console.log(error.response);
      })
    },

    // 当前页面变化
    handleCurrentChange(page) {
      // 更新当前页码
      this.filters.page = page;
      this.get_course();
    },

    // 如果选择的每页数据量发生变化 则重新以新的每页数据量从第一页显示
    handleSizeChange(size){
      // 更新每页条数
      this.filters.size=size;
      // 重置回第一页
      this.filters.page=1
      this.get_course();
    },

    get_course_category() {
      // 获取课程分类信息
      this.$axios.get(`${this.$settings.HOST}/course/category/`).then(response => {
        this.category_list = response.data;
      })
    },

    changeCategory(id) {
      this.category = id;
      // 切换课程时要重新请求获得更新后的数据
      this.get_course();
    },

    change_order_type(type) {
      // 更改升序或者降序
      // 有该选择的类型且此时为降序 则改为升序
      if (this.filters.type === type && this.filters.orders === "desc") {
        this.filters.orders = "asc";
        // 有该选择的类型且此时为升序 则改为降序
      } else if (this.filters.type === type && this.filters.orders === "asc") {
        this.filters.orders = "desc";
      }
      // 就算是没有排序 也让排序字段指向该点击字段
      this.filters.type = type;
      // 每次更新要重新请求 显示更新后的数据
      this.get_course();
    },

    change_order_class(type) {
      // 更改当前选中筛选条件的高亮方式
      if (this.filters.type === type && this.filters.orders === "asc") {
        return "this asc";
      } else if (this.filters.type === type && this.filters.orders === "desc") {
        return "this desc";
      } else {
        return "";
      }
    }

  },
  components: {
    Header,
    Footer,
  }
}
</script>


<style scoped>
.course {
  background: #f6f6f6;
}

.course .main {
  width: 1100px;
  margin: 35px auto 0;
}

.course .condition {
  margin-bottom: 35px;
  padding: 25px 30px 25px 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.course .cate-list {
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
  padding-bottom: 18px;
  margin-bottom: 17px;
}

.course .cate-list::after {
  content: "";
  display: block;
  clear: both;
}

.course .cate-list li {
  float: left;
  font-size: 16px;
  padding: 6px 15px;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  transition: all .3s ease;
  cursor: pointer;
  color: #4a4a4a;
  border: 1px solid transparent; /* transparent 透明 */
}

.course .cate-list .title {
  color: #888;
  margin-left: 0;
  letter-spacing: .36px;
  padding: 0;
  line-height: 28px;
}

.course .cate-list .this {
  color: #ffc210;
  border: 1px solid #ffc210 !important;
  border-radius: 30px;
}

.course .ordering::after {
  content: "";
  display: block;
  clear: both;
}

.course .ordering ul {
  float: left;
}

.course .ordering ul::after {
  content: "";
  display: block;
  clear: both;
}

.course .ordering .condition-result {
  float: right;
  font-size: 14px;
  color: #9b9b9b;
  line-height: 28px;
}

.course .ordering ul li {
  float: left;
  padding: 6px 15px;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  transition: all .3s ease;
  cursor: pointer;
  color: #4a4a4a;
}

.course .ordering .title {
  font-size: 16px;
  color: #888;
  letter-spacing: .36px;
  margin-left: 0;
  padding: 0;
  line-height: 28px;
}

.course .ordering .this {
  color: #ffc210;
}

.course .ordering .price {
  position: relative;
}

.course .ordering .price::before,
.course .ordering .price::after {
  cursor: pointer;
  content: "";
  display: block;
  width: 0px;
  height: 0px;
  border: 5px solid transparent;
  position: absolute;
  right: 0;
}

.course .ordering .price::before {
  border-bottom: 5px solid #aaa;
  margin-bottom: 2px;
  top: 2px;
}

.course .ordering .price::after {
  border-top: 5px solid #aaa;
  bottom: 2px;
}

.course .course-item:hover {
  box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
}

.course .course-item {
  width: 1050px;
  background: #fff;
  padding: 20px 30px 20px 20px;
  margin-bottom: 35px;
  border-radius: 2px;
  cursor: pointer;
  box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
  /* css3.0 过渡动画 hover 事件操作 */
  transition: all .2s ease;
}

.course .course-item::after {
  content: "";
  display: block;
  clear: both;
}

/* 顶级元素 父级元素  当前元素{} */
.course .course-item .course-image {
  float: left;
  width: 423px;
  height: 210px;
  margin-right: 30px;
}

.course .course-item .course-image img {
  width: 100%;
}

.course .course-item .course-info {
  float: left;
  width: 596px;
}

.course-item .course-info h3 {
  font-size: 26px;
  color: #333;
  font-weight: normal;
  margin-bottom: 8px;
}

.course-item .course-info h3 span {
  font-size: 14px;
  color: #9b9b9b;
  float: right;
  margin-top: 14px;
}

.course-item .course-info h3 span img {
  width: 11px;
  height: auto;
  margin-right: 7px;
}

.course-item .course-info .teather-info {
  font-size: 14px;
  color: #9b9b9b;
  margin-bottom: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
}

.course-item .course-info .teather-info span {
  float: right;
}

.course-item .lesson-list::after {
  content: "";
  display: block;
  clear: both;
}

.course-item .lesson-list li {
  float: left;
  width: 44%;
  font-size: 14px;
  color: #666;
  padding-left: 22px;
  /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
  background: url("../../public/static/image/play-icon-gray.svg") no-repeat left 4px;
  margin-bottom: 15px;
}

.course-item .lesson-list li .lesson-title {
  /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  display: inline-block;
  max-width: 200px;
}

.course-item .lesson-list li:hover {
  background-image: url("../../public/static/image/play-icon-yellow.svg");
  color: #ffc210;
}

.course-item .lesson-list li .free {
  width: 34px;
  height: 20px;
  color: #fd7b4d;
  vertical-align: super;
  margin-left: 10px;
  border: 1px solid #fd7b4d;
  border-radius: 2px;
  text-align: center;
  font-size: 13px;
  white-space: nowrap;
}

.course-item .lesson-list li:hover .free {
  color: #ffc210;
  border-color: #ffc210;
}

.course-item .pay-box::after {
  content: "";
  display: block;
  clear: both;
}

.course-item .pay-box .discount-type {
  padding: 6px 10px;
  font-size: 16px;
  color: #fff;
  text-align: center;
  margin-right: 8px;
  background: #fa6240;
  border: 1px solid #fa6240;
  border-radius: 10px 0 10px 0;
  float: left;
}

.course-item .pay-box .discount-price {
  font-size: 24px;
  color: #fa6240;
  float: left;
}

.course-item .pay-box .original-price {
  text-decoration: line-through;
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  float: left;
  margin-top: 10px;
}

.course-item .pay-box .buy-now {
  width: 120px;
  height: 38px;
  background: transparent;
  color: #fa6240;
  font-size: 16px;
  border: 1px solid #fd7b4d;
  border-radius: 3px;
  transition: all .2s ease-in-out;
  float: right;
  text-align: center;
  line-height: 38px;
}

.course-item .pay-box .buy-now:hover {
  color: #fff;
  background: #ffc210;
  border: 1px solid #ffc210;
}

.cate-list li {
  float: left;
  font-size: 16px;
  padding: 6px 15px;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  cursor: pointer;
  color: #4a4a4a;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.cate-list li.this {
  color: #ffc210;
  border: 1px solid #ffc210;
  border-radius: 30px;
}
</style>