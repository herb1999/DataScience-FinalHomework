<template>
  <div class="container">
    <div class="text">
      <div class="title">
        <div v-if="curCase">{{curCase[0]}} - {{curCase[1]}}</div>
      </div>
      <div class="description">
        <div class="label-div">
          <div class="label" v-for="label in recommendLabels" :key="label[0]">{{label[0]}}:{{label[1].toFixed(2)}}</div>
        </div>
        <mavon-editor
          class="md"
          :value="caseDescrtption"
          :subfield="false"
          :defaultOpen="'preview'"
          :toolbarsFlag="false"
          :editable="false"
          :scrollStyle="true"
          :ishljs="true"
        ></mavon-editor>
      </div>
    </div>
    <div class="code">
      <div class="button-div">
        <a-button type="primary" @click="onCommitCode">提交代码</a-button>
        <a-divider type="vertical" />
        <a-button type="primary" @click="onGetRecommendCode">推荐代码</a-button>
      </div>

      <div class="code-div">
        <a-textarea placeholder="在这里填入代码" :rows="30" :allowClear="true" v-model="code" />
      </div>
    </div>
    <recommendCode :visible="modalVisible" @hide="onHideModal"/>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import recommendCode from '../components/recommendCode'
export default {
  data() {
    return {
      code: "",
      modalVisible:false,
    };
  },
  name: "test",
  components:{
recommendCode
  },
  async created() {
    // this.test();
    await this.allCases();
    await this.getCaseDescription(this.caseId);
    await this.getRecommendLabel(this.caseId);
    console.log(this.caseId);
  },
  methods: {
    ...mapActions([
      "test",
      "getCaseDescription",
      "allCases",
      "commitCode",
      "getRecommendLabel"
    ]),
    onCommitCode() {
      this.commitCode({
        caseId: this.caseId,
        code: this.code,
      });
    },
    onGetRecommendLabel() {},
    onGetRecommendCode() {
      
      this.modalVisible=true
    },
    onHideModal(){
      this.modalVisible=false
    }
  },
  computed: {
    ...mapGetters(["caseDescrtption", "recommendLabels","recommendCodes"]),
    caseId() {
      return this.$route.params.testId;
    },
    curCase() {
      let res = this.$store.getters.curCase(this.caseId);
      return res;
    },
  },
};
</script>

<style lang="less" scoped>
.container {
  width: 100%;
  height: 100%;
  display: flex;
  .text {
    width: 50%;
    max-height: 100%;
    padding: 5px 5px 5px 10px;
    display: flex;
    justify-content: space-around;
    flex-direction: column;
    .title {
      width: 100%;
      padding-left: 20px;
      border-left: 5px solid rgba(80, 158, 223, 0.836);
      display: flex;
      text-align: center;
      font-size: 20px;
    }
    .description {
      height: 90%;
      overflow: auto;
      .label-div{
        display: flex;
        flex-wrap: wrap;
        .label{
          background: rgb(169, 221, 228);
          margin-left: 20px;
          margin-bottom: 20px;
          border-radius: 20px;
          padding: 6px 10px;
        }
      }
      .md {
        border-radius: 4px;
        padding: 10px 20px;
        background-color: #f1f1f1ba;
      }
    }
  }
  .code {
    width: 50%;
    height: 100%;
    padding: 5px 5px 5px 10px;
    border-left: 0.5px solid rgba(135, 135, 136, 0.836);
    display: flex;
    justify-content: space-around;
    flex-direction: column;
    .button-div {
      width: 100%;
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>
<style lang="less">
.button-div {
  .ant-divider,
  .ant-divider-vertical {
    height: 100%;
  }
  padding-right: 20px;
}
.ant-modal-wrap{
  z-index: 2000 !important;
}
.ant-modal-mask{
  z-index: 1999 !important;
}
</style>
