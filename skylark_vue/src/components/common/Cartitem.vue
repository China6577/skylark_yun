<template>
  <div class="cart_item">
    <div class="cart_column column_1">
      <el-checkbox class="my_el_checkbox" v-model="checked" @change="onCheckboxChange"></el-checkbox>
    </div>
    <div class="cart_column column_2">
      <img :src="cart.course_img" alt="">
      <span><router-link :to="`/course/detail/${cart.id}`">{{ cart.name }}</router-link></span>
    </div>

    <div class="cart_column column_3">
      <el-select v-model="expireId" size="mini" placeholder="请选择购买有效期" class="my_el_select">
        <el-option v-for="item in cart.expire_list" :label="item.expire_text" :value="item.id"
                   :key="item.id">
        </el-option>
      </el-select>
    </div>

    <div class="cart_column column_4">
      ¥{{ cart.price }}
    </div>

    <div class="cart_column column_5">
      <el-button type="danger" @click="handle_delete_course(cart.id)">
        删除
      </el-button>
    </div>
  </div>
</template>


<script>


export default {
  name: "CartItem",
  // props(properties) 是父组件向子组件传递数据
  props: ['cart','is_all_selected'],
  data() {
    return {
      checked: this.cart.is_selected,
      expireId: this.cart.expire_id,
    }
  },
  watch: {
    "cart.is_selected": function () {
      this.checked = this.cart.is_selected;
    },
    expireId: function () {
      this.change_expire();
    }
  },
  methods: {
    onCheckboxChange() {
      this.change_selected();
    },

    change_selected() {
      let token = localStorage.token || sessionStorage.token;
      this.$axios.patch(`${this.$settings.HOST}/cart/changeselected/`, {
        selected: this.checked,
        course_id: this.cart.id
      }, {
        headers: {
          "Authorization": "Bearer " + token,
        }
      }).then(res => {
        this.$message.success(res.data.message);
        // 更改完值的时候要重新获取cart更新后的数据
        this.$emit("changeSelected")
        // 当子组件中，切换了商品课程的勾选状态，则通知父组件重新计算购物商品总价
        this.$emit('calc_total')
        this.$emit('is_all_selected', this.checked, this.cart.id)
      }).catch(error => {
        console.log(error);
      });
    },

    change_expire() {
      let token = localStorage.token || sessionStorage.token;
      this.$axios.put(`${this.$settings.HOST}/cart/`, {
        expire_id: this.expireId,
        course_id: this.cart.id
      }, {
        headers: {
          "Authorization": "Bearer " + token,
        }
      }).then(res => {
        this.$message.success(res.data.message)
        // 更改完值的时候要重新获取cart更新后的数据
        this.$emit("changeExpireId")
        // 当子组件中，切换了商品课程的有效期，则通知父组件重新计算购物商品总价
        this.$emit('calc_total')
      }).catch(error => {
        console.log(error)
      })
    },

    handle_delete_course(cart_id){
      let token = localStorage.token || sessionStorage.token;
      this.$axios
          .delete(`${this.$settings.HOST}/cart/`, {
            params: {
              course_id: cart_id,
            },
            headers: {
              Authorization: "Bearer " + token,
            },
          })
          .then((res) => {
            this.$message.success(res.data.message);
          })
          .catch((error) => {
            console.log(error);
            this.$message.error("删除失败，请重试");
          });
      this.$emit("delete_cart", cart_id);
    }

  }
}
</script>

<style scoped>
.cart_item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.cart_column {
  padding: 0 10px;
  flex: 1;
}

.column_1 {
  width: 50px;
  flex: 0 0 50px;
}

.column_2 {
  flex: 2;
  display: flex;
  align-items: center;
}

.column_2 img {
  width: 80px;
  height: 60px;
  margin-right: 20px;
}

.column_3 {
  width: 200px;
  flex: 0 0 200px;
}

.column_4 {
  width: 100px;
  flex: 0 0 100px;
  text-align: right;
}

.column_5 {
  width: 80px;
  flex: 0 0 80px;
  text-align: right;
}
</style>
