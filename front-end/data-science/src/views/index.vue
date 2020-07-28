<template>
  <div class="container">
    <div class="main-title">
      <img src="../assets/python.png" />
      <h1>Python推荐练习系统</h1>
    </div>
    <div class="card" v-for="item in caseList" :key="item[0]" @click="toTest(item[0])">
      <div class="title">{{item[0]}}</div>
      <div class="name">{{item[1]}}</div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "index",
  async created() {
    await this.allCases();
  },
  methods: {
    ...mapActions(["allCases"]),
    toTest(caseId) {
      this.$router.push({ name: "test", params: { testId: caseId } });
    },
  },
  computed: {
    ...mapGetters(["caseList"]),
  },
};
</script>
<style lang="less" scoped>
.container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  flex-grow: 3;
  .main-title {
    width: 100%;
    padding: 20px;
    margin: 0px 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    img {
      width: 70px;
      height: 70px;
      margin: 40px;
    }
    h1 {
      margin-top: 0;
      margin-bottom: 0;
      color: rgba(0, 0, 0, 0.85);
      font-weight: 500;
    }
  }
  .card {
    width: 18%;
    padding: 1%;
    margin: 10px 1%;
    height: 100px;
    border: 1px solid rgba(165, 155, 155, 0.719);
    box-shadow: 0 2px 4px rgba(134, 134, 134, 0.4);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    border-radius: 15px;
    padding: 15px;
    cursor: pointer;
    .title {
      font-size: 20px;
      font-weight: 600;
      align-self: flex-start;
    }
    .name {
      width: 50%;
      overflow: hidden;
      -webkit-line-clamp: 2;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-box-orient: vertical;
    }
  }
  .card:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }
}
</style>