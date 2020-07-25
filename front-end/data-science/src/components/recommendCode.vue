<template>
  <div>
    <a-modal v-model="visible" title="推荐代码" @cancel="onHideModal" :footer="null" :width="700">
      <pre class="code" v-for="code in recommendCodes" :key="code">
        <code>{{code}}</code>
      </pre>

      <a-divider/>
    </a-modal>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
    };
  },
  props:['visible'],
  async created(){
    
  },
  computed:{
    ...mapGetters(["recommendCodes"]),
    caseId() {
      return this.$route.params.testId;
    },
  },
  methods: {
    ...mapActions([
      "getRecommendCodes"
    ]),
    onHideModal(e) {
      console.log(e);
      this.$emit('hide')
    },
  },
};
</script>
<style lang="less" scoped>
  pre{
    margin: 20px 0px;
    background: rgb(245, 241, 241);
  }
</style>
