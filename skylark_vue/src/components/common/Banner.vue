<template>
  <el-carousel height="720px" :interval="3000" arrow="always" class="el-carousel">
    <el-carousel-item v-for="item in banner_list" :key="item.id" class="el-carousel__item">
      <a :href="item.link"><img :src="item.image_url" alt="" class="carousel-img"></a>
    </el-carousel-item>
  </el-carousel>

</template>

<script>

export default {
  name: "BannerComp",
  data() {
    return {
      banner_list: []
    }
  },
  created() {
    this.get_banner_list();
  },
  methods: {
    get_banner_list() {
      //   获取轮播图广告列表
      this.$axios.get(`${this.$settings.HOST}/home/banner/`, {}).then(res => {
        this.banner_list = res.data;
      })
    }
  },
}
</script>


<style scoped>
.el-carousel,
.el-carousel__item {
  height: 756px; /* 高度固定为视口高度 */
}

.carousel-img {
  width: 100%;
  height: auto;
  object-fit: cover;
  margin: 0;
  padding: 0;
}
</style>


