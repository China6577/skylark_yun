<template>
  <div class="footer">
    <ul>
      <li v-for="nav in nav_list" :key="nav.id">
        <span v-if="nav.is_site"><a :href="nav.link">{{ nav.title }}</a></span>
        <span v-else><router-link :to="nav.link">{{ nav.title }}</router-link></span>
      </li>
    </ul>
    <p class="copyright">Copyright © skylarkyun.com版权所有 | 湘ICP备2022015350号-4</p>
  </div>
</template>

<script>
export default {
  name: "FooterComponent",
  data() {
    return {
      nav_list: [],
    }
  },
  created() {
    this.get_nav();
  },
  methods: {
    get_nav() {
      this.$axios.get(`${this.$settings.HOST}/home/nav/footer/`, {}).then(response => {
        this.nav_list = response.data;
      }).catch(error => {
        console.log(error.response);
      })
    }
  }
}
</script>

<style scoped>
.footer {
  width: 100%;
  height: 128px;
  background: #25292e;
  color: #fff;
}

.footer ul {
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 810px;
}

.footer ul li {
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}

.footer ul::after {
  content: "";
  display: block;
  clear: both;
}

.footer p {
  text-align: center;
  font-size: 12px;
}

.footer ul li a,
.footer ul li a:visited,
.footer ul li a:hover,
.footer ul li a:active,
.footer ul li router-link {
  color: #fff; /* 设置链接文字为白色 */
}
</style>
