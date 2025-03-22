<template>
  <div class="cart">
    <Header></Header>
    <div class="cart_info">
      <!-- 购物车标题 -->
      <div class="cart_title">
        <span class="text">我的购物车</span>
        <span class="total">共 {{ cart_length }} 门课程</span>
      </div>

      <!-- 购物车内容 -->
      <div class="cart_table">
        <!-- 顶部全选和操作栏 -->
        <div class="cart_head_row">
          <span class="select_all">
            <el-checkbox v-model="is_all_selected" @change="handle_select_all" :disabled="selected_items.length === 0">
              全选
            </el-checkbox>
          </span>
        </div>

        <!-- 商品列表 -->
        <div class="cart_course_list">
          <!-- 给子组件传参 -->
          <CartItem
              v-for="cart in cart_list"
              :cart="cart"
              :key="cart.id"
              @changeSelected="handleSelected"
              @changeExpireId="handleExpireId"
              @calc_total="calc_total"
              @is_all_selected="handle_all_selected"
              @delete_cart="handle_delete_cart"
          ></CartItem>
        </div>

        <div class="discount">
          <div id="accordion">

            <div class="coupon-box">
              <div class="icon-box">
                <span class="select-coupon">使用优惠劵：</span>
                <a class="select-icon unselect" :class="use_coupon?'is_selected':''"
                   @click="changeUseCoupon"><img class="sign is_show_select"
                                                        src="../../public/static/image/12.png" alt=""></a>
                <span class="coupon-num">有{{ coupon_list.length }}张可用</span>
              </div>
            </div>

            <div id="collapseOne" v-if="use_coupon">

              <ul class="coupon-list" v-if="coupon_list.length>0">
                <li class="coupon-item" v-for="(item,index) in coupon_list" :key="index"
                    @click="changeCouponPrice(index,item.id)"
                    :class="selected_coupon(index,item.id)"
                >
                  <p class="coupon-name">{{ item.coupon.name }}</p>
                  <p class="coupon-condition" v-if="item.coupon.condition>0">满{{ item.coupon.condition }}元可以使用</p>
                  <p class="coupon-condition" v-else>没有使用条件</p>
                  <p class="coupon-time start_time">开始时间：{{ item.start_time.replace("T", " ") }}</p>
                  <p class="coupon-time end_time">过期时间：{{ item.end_time }}</p>
                </li>
              </ul>

              <div class="no-coupon" v-if="coupon_list.length<1">
                <span class="no-coupon-tips">暂无可用优惠券</span>
              </div>

            </div>
          </div>

          <p class="sun-coupon-num" v-if="use_coupon">优惠券抵扣：<span>{{ this.coupon_price }}</span></p>
        </div>

        <!-- 底部结算栏 -->
        <div class="cart_footer_row">
          <span class="select_all"></span>
          <span class="total_price">
            总计：<span class="price">¥{{ total_price }}</span>
          </span>
          <span class="goto_pay">
              <el-button type="warning" :disabled="selected_items.length === 0" @click="payHandler">
                去结算 {{ selected_items.length }}
              </el-button>
          </span>
        </div>

      </div>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
import Header from "./common/Header";
import Footer from "./common/Footer";
import CartItem from "./common/Cartitem";


export default {
  name: "CartComp",
  data() {
    return {
      cart_length: 0,
      cart_list: [],
      total_price: 0.00,
      is_all_selected: false, // 是否全选
      selected_items: [], // 选中的商品

      use_coupon: false,
      coupon: 0,          // 优惠券ID，0表示没有使用优惠券
      coupon_list: [],      // 优惠券列表
      coupon_price: 0,
      is_click_index: -1,
      coupon_sale: "",
    };
  },

  created() {
    this.token = this.check_user_login();
    this.get_cart();
    this.get_coupon();


  },

  // 要在mounted挂载完后执行calc_total因为cart_list是在挂载完获取的
  updated() {
    this.calc_total();
  },

  methods: {

    // 检查用户是否登录
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
        });
        return false;
      }
      return token;
    },

    // 获取购物车数据
    get_cart() {
      this.$axios.get(`${this.$settings.HOST}/cart/`, {
        headers: {
          Authorization: `Bearer ${this.token}`
        },
      }).then((response) => {
        this.selected_items = []
        this.cart_list = response.data.data;
        this.cart_length = response.data.cart_length;

        let flag = true;
        this.cart_list.forEach((cart) => {
          if (cart.is_selected) {
            this.selected_items.push(cart.id);
          } else {
            flag = false;
          }
        });
        this.is_all_selected = flag;
      }).catch(error => {
        console.error('获取购物车数据失败:', error);
      });
    },

    get_coupon() {
      // 获取当前用户拥有的优惠券
      this.$axios.get(`${this.$settings.HOST}/coupon/`, {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      }).then(response => {
        this.coupon_list = response.data;
      }).catch(error => {
        this.$message.error("对不起，当前购物车没有任何商品被勾选！");
        console.log(error);
      });
    },

    handleSelected() {
      if (this.use_coupon){
        location.reload();
      }else {
        this.get_cart();
      }
    },

    handleExpireId() {
      if (this.use_coupon){
        location.reload();
      }else {
        this.get_cart();
      }
    },

    handle_delete_cart(cart_id) {
      // 从本地 cart_list 中删除对应的商品
      this.cart_list = this.cart_list.filter((item) => item.id !== cart_id);
      this.cart_length -= 1
      this.coupon_price = 0
      this.calc_total(); // 重新计算总价
      this.$store.state.cart.cart_length -= 1
      // 不能用filter 因为filter是筛选 影响不了selected_items.length
      this.selected_items.splice(this.selected_items.indexOf(cart_id), 1)
    },

    calc_total() {
      // 初始化总价格为 0
      let total = 0;
      // 遍历购物车列表，计算勾选商品的总价格
      this.cart_list.forEach((course) => {
        if (course.is_selected) {
          total += parseFloat(course.price);
        }
      });
      if (this.use_coupon) {
        // 减免优惠
        this.total_price = (total - this.coupon_price).toFixed(2);
      }else {
        this.total_price = total.toFixed(2);
      }

    },

    handle_select_all() {
      this.$axios.put(`${this.$settings.HOST}/cart/changeselected/`, {
        is_all_selected: this.is_all_selected,
        cartList: this.cart_list
      }, {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      }).then(res => {
        this.get_cart();
        this.$message.success(res.data.message);
      }).catch(error => {
        console.log(error);
      });
    },

    handle_all_selected(checked, id) {
      if (!checked) {
        this.is_all_selected = false;
      } else {
        this.cart_list.forEach((cart) => {
          if (cart.id !== id && cart.is_selected === false) {
            return false;
          }
        })
        this.is_all_selected = true;
      }
    },


    selected_coupon(index, user_coupon_id) {
      // 当选中优惠券时，切换优惠券的高亮显示效果
      let user_coupon = this.coupon_list[index];
      // 判断总价格是否满足优惠券的使用
      if (this.total_price < user_coupon.coupon.condition) {
        return "disable";
      }
      // 判断优惠券是否处于使用时间范围内
      let start_timestamp = parseInt(new Date(user_coupon.start_time) / 1000);
      let end_timestamp = parseInt(new Date(user_coupon.end_time) / 1000);
      let now_timestamp = parseInt(new Date() / 1000);
      if ((now_timestamp < start_timestamp) || (now_timestamp > end_timestamp)) {
        return "disable";
      }
      if (this.coupon === user_coupon_id) {
        return "active";
      }
      return "";
    },

    payHandler() {
      // 生成订单
      this.$axios.post(`${this.$settings.HOST}/order/`, {
        pay_type: 1,
        coupon: this.coupon,      // 优惠券ID
      }, {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      }).then(response => {
        // 订单生成成功！
        this.$message.success("订单生成成功!")
        this.$store.state.cart.cart_length -= this.selected_items.length;
        this.cart_list = this.cart_list.filter(cart => !this.selected_items.some(selected_items => selected_items.id === cart.id));
        setTimeout(()=>{
          location.reload()
        }, 1000)
        console.log(response)
      }).catch(error => {
        this.$message.error("订单生成失败！");
        console.log(error)
      })
    },

    changeCouponPrice(index, id) {
      this.coupon = id
      let item = this.coupon_list[index]
      // 选出当前选中的那一张优惠券
      let start_timestamp = parseInt(new Date(item.start_time) / 1000);
      let end_timestamp = parseInt(new Date(item.end_time) / 1000);
      let now_timestamp = parseInt(new Date() / 1000);
      // 选出当前可以使用的优惠券
      if (this.is_click_index !== index && (this.total_price > item.coupon.condition) && (now_timestamp > start_timestamp) && ((now_timestamp < end_timestamp) || (isNaN(end_timestamp)))) {
        // 获取优惠公式
        let f = parseFloat(item.coupon.sale.substr(1));
        this.coupon_sale = item.coupon.sale;
        // 根据优惠公式计算最终折算后的总价格
        if (item.coupon.sale[0] === "*") {
          // 折扣优惠
          this.coupon_price = (this.total_price * (1 - f)).toFixed(2);
        } else {
          this.coupon_price = f.toFixed(2);
        }
        this.is_click_index = index;
      }
    },

    changeUseCoupon() {
      this.use_coupon = !this.use_coupon;
    }
  },
  components: {
    Header,
    Footer,
    CartItem,
  }
}
</script>

<style scoped>
.cart {
  background-color: #f8f9fa;
  padding: 20px 0;
}

.cart_info {
  width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 16px; /* 增加圆角 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 更柔和的阴影 */
}

.cart_title {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cart_title .text {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}

.cart_title .total {
  font-size: 18px;
  color: #666;
  font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}

.cart_table {
  width: 100%;
  margin-top: 20px;
}

.cart_head_row {
  background: #f8f9fa;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 12px 12px 0 0; /* 增加圆角 */
  border-bottom: 1px solid #e9ecef;
}

.cart_course_list {
  margin-top: 10px;
}

.cart_footer_row {
  background: #f8f9fa;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 0 0 12px 12px; /* 增加圆角 */
  border-top: 1px solid #e9ecef;
  margin-top: 20px;
}

.select_all {
  display: flex;
  align-items: center;
}

.total_price {
  font-size: 20px;
  color: #333;
  font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}

.total_price .price {
  color: #ff6700;
  font-weight: bold;
  font-size: 24px;
}

.goto_pay {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.goto_pay :hover {
  background-color: #e65c00;
  border-color: #e65c00;
  transform: translateY(-2px); /* 悬停时轻微上移 */
  box-shadow: 0 6px 8px rgba(255, 103, 0, 0.3); /* 悬停时阴影加深 */
}

.goto_pay :active {
  background-color: #cc5200;
  border-color: #cc5200;
  transform: translateY(0); /* 点击时恢复原位 */
  box-shadow: 0 4px 6px rgba(255, 103, 0, 0.2); /* 点击时阴影恢复 */
}

/* 响应式设计 */
@media (max-width: 768px) {
  .cart_info {
    width: 100%;
    padding: 10px;
  }

  .cart_title {
    flex-direction: column;
    align-items: flex-start;
  }

  .cart_title .text {
    font-size: 24px;
  }

  .cart_title .total {
    font-size: 16px;
    margin-top: 10px;
  }

  .cart_footer_row {
    flex-direction: column;
    align-items: flex-start;
  }

  .goto_pay {
    width: 100%;
    margin-top: 10px;
  }

  .goto_pay {
    width: 100%;
    text-align: center;
    padding: 12px 24px; /* 调整按钮宽度 */
  }
}

.coupon-box {
  text-align: left;
  padding-bottom: 22px;
  padding-left: 30px;
  border-bottom: 1px solid #e8e8e8;
}

.coupon-box::after {
  content: "";
  display: block;
  clear: both;
}

.icon-box {
  float: left;
}

.icon-box .select-coupon {
  float: left;
  color: #666;
  font-size: 16px;
}

.icon-box::after {
  content: "";
  clear: both;
  display: block;
}

.select-icon {
  width: 20px;
  height: 20px;
  float: left;
}

.select-icon img {
  max-height: 100%;
  max-width: 100%;
  margin-top: 2px;
  transform: rotate(-90deg);
  transition: transform .5s;
}

.is_show_select {
  transform: rotate(0deg) !important;
}

.coupon-num {
  height: 22px;
  line-height: 22px;
  padding: 0 5px;
  text-align: center;
  font-size: 12px;
  float: left;
  color: #fff;
  letter-spacing: .27px;
  background: #fa6240;
  border-radius: 2px;
  margin-left: 20px;
}

.no-coupon {
  text-align: center;
  width: 100%;
  padding: 50px 0px;
  align-items: center;
  justify-content: center; /* 文本两端对其 */
  border-bottom: 1px solid rgb(232, 232, 232);
}

.no-coupon-tips {
  font-size: 16px;
  color: #9b9b9b;
}

.discount {
  overflow: hidden;
}

.sun-coupon-num {
  margin-right: 45px;
  margin-bottom: 43px;
  margin-top: 40px;
  font-size: 16px;
  color: #4a4a4a;
  display: inline-block;
  float: right;
}

.sun-coupon-num span {
  font-size: 18px;
  color: #fa6240;
}

.coupon-list {
  margin: 20px 0;
}

.coupon-list::after {
  display: block;
  content: "";
  clear: both;
}

.coupon-list .active {
  background-color: #fa9000;
}

.coupon-list .disable {
  cursor: not-allowed;
  background-color: #fa6060;
}

.coupon-item {
  float: left;
  margin: 15px 8px;
  width: 180px;
  height: 100px;
  padding: 5px;
  background-color: #fa3030;
  cursor: pointer;
}

.coupon-condition {
  font-size: 12px;
  text-align: center;
  color: #fff;
}

.coupon-name {
  color: #fff;
  font-size: 24px;
  text-align: center;
}

.coupon-time {
  text-align: left;
  color: #fff;
  font-size: 12px;
}

.unselect {
  margin-left: 0px;
  transform: rotate(-90deg);
}

.is_selected {
  transform: rotate(-1turn) !important;
}
</style>