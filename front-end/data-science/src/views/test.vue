<template>
  <div class="container">
  
    <div class="text">
      <div class="title">
        <div v-if="curCase">{{curCase[0]}} - {{curCase[1]}}</div>
      </div>
      <div class="description">
        <div class="label-title">推荐标签</div>
        <div class="label-div">
          <div
            :class="{label:label[1]===0,label_1:0<label[1]&&label[1]<1,label_2:label[1]>=1}"
            v-for="label in recommendLabels"
            :key="label[0]"
          >{{label[0]}}</div>
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
      <div class="score-and-button">
        <div class="score">
          <div class="current">得分：<span style="font-size:25px;font-weight:600">{{score}}</span></div>
          <div class="total">/100</div>
        </div>
      <div class="button-div">
        
        <a-button type="primary" @click="onCommitCode">提交代码</a-button>
        <a-divider type="vertical" />
        <a-button type="primary" @click="onGetRecommendCode" :disabled="!canGetCode">推荐代码</a-button>
      </div>
      </div>

      <div class="code-div">
        <a-textarea placeholder="在这里填入代码" :rows="30" :allowClear="true" v-model="code" />
      </div>
    </div>
    <recommendCode :visible="modalVisible" @hide="onHideModal" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import recommendCode from "../components/recommendCode";
export default {
  data() {
    return {
      code: "",
      modalVisible: false,
      score:0
    };
  },
  name: "test",
  components: {
    recommendCode,
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
      "getRecommendLabel",
      "getRecommendCodes",
    ]),
    async onCommitCode() {
      this.score=await this.commitCode({
        caseId: this.caseId,
        code: this.code,
      });
    },
    onGetRecommendLabel() {},
    async onGetRecommendCode() {
      await this.getRecommendCodes(this.caseId);
      this.modalVisible = true;
    },
    onHideModal() {
      this.modalVisible = false;
    },
  },
  computed: {
    ...mapGetters([
      "caseDescrtption",
      "recommendLabels",
      "recommendCodes",
      "canGetCode",
    ]),
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
      border-top: solid 0.5px rgba(198, 198, 202, 0.836);
      .label-title {
        padding-left: 20px;
        width: 100%;
        text-align: start;
        font-size: 20px;
        font-weight: 600;
        margin: 20px 0px;
      }
      .label-div {
        display: flex;
        flex-wrap: wrap;
        .label {
          background: rgb(169, 211, 228);
          margin-left: 20px;
          margin-bottom: 20px;
          border-radius: 20px;
          padding: 6px 10px;
        }
        .label_1 {
          background: rgb(92, 160, 228);
          margin-left: 20px;
          margin-bottom: 20px;
          border-radius: 20px;
          padding: 6px 10px;
        }
        .label_2 {
          background: rgb(95, 119, 228);
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
    .description::-webkit-scrollbar {
      /*滚动条整体样式*/
      width: 8px; /*高宽分别对应横竖滚动条的尺寸*/
      height: 1px;
    }
    .description::-webkit-scrollbar-thumb {
      /*滚动条里面小方块*/
      border-radius: 10px;
      background-color: rgb(92, 185, 221);
      background-image: -webkit-linear-gradient(
        45deg,
        rgba(255, 255, 255, 0.2) 25%,
        transparent 25%,
        transparent 50%,
        rgba(255, 255, 255, 0.2) 50%,
        rgba(255, 255, 255, 0.2) 75%,
        transparent 75%,
        transparent
      );
    }
    .description::-webkit-scrollbar-track {
      /*滚动条里面轨道*/
      box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
      background: #ededed;
    }
  }
  .code {
    width: 50%;
    height: 100%;
    padding: 5px 5px 5px 10px;
    border-left: 0.5px solid rgba(208, 208, 209, 0.466);
    display: flex;
    justify-content: space-around;
    flex-direction: column;
    .score-and-button{
      width: 100%;
      display: flex;
      justify-content: space-around;
      .button-div {
      width: 40%;
      display: flex;
      justify-content: flex-end;
      
    }
    .score{
        font-size: 20px;
        font-weight: 400;
        display: flex;
        .current{

        }
        .total{
          margin-top:10px;
        }
      }
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
.ant-modal-wrap {
  z-index: 2000 !important;
}
.ant-modal-mask {
  z-index: 1999 !important;
}
</style>
