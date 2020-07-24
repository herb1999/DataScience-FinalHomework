import Vue from 'vue'
import Vuex from 'vuex'
import {
  testAPI,
  allCasesAPI,
  caseMdAPI,
  commitCodeAPI,
  recommendLabelAPI,
  recommendCodeAPI
} from '@/api/api'
import {
  message
} from 'ant-design-vue'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    caseList: [],
    caseDescrtption: '',
    recommendLabels: {},
    recommendCodes:[]
  },
  mutations: {
    set_caseList: function (state, data) {
      state.caseList = data
    },
    set_caseDescrtption: function (state, data) {
      state.caseDescrtption = data
    },
    set_recommendLabel: function (state, data) {
      state.recommendLabels = data
    },
    set_recommendCodes: function (state, data) {
      state.recommendCodes = data
    },
  },
  actions: {
    // 测试
    test: async () => {
      const res = await testAPI().catch(err => {
        console.log('失败')
        console.log(err)
      })
      if (res) {
        console.log('成功' + res)
      }
    },
    //获取所有caseId和caseName
    allCases: async ({
      commit
    }) => {
      const res = await allCasesAPI().catch(err => {
        console.log('失败')
        console.log(err)
      })
      if (res) {
        console.log('成功' + res)
        commit('set_caseList', res)
      }
    },
    //获取对应case的md
    getCaseDescription: async ({
      commit
    }, caseId) => {
      const res = await caseMdAPI(caseId).catch(err => {
        console.log('失败')
        console.log(err)
      })
      if (res) {
        console.log('成功' + res)
        commit('set_caseDescrtption', res)
      }
    },

    commitCode: async ({
      commit
    }, data) => {
      const res = await commitCodeAPI(data).catch(err => {
        console.log('代码提交失败')
        console.log(err)
      })

      message.success('代码提交成功')
      console.log('代码提交成功' + res)

    },

    getRecommendLabel: async ({
      commit
    }, data) => {
      const res = await recommendLabelAPI(data).catch(err => {
        console.log('获取推荐标签失败')
        console.log(err)
      })

      if (res) {
        message.success('获取推荐标签成功')
        console.log('获取推荐标签成功' )
        console.log(res)
        commit('set_recommendLabel', res)
      }
    },

    getRecommendCodes:async ({
      commit
    }, data) => {
      const res = await recommendCodeAPI(data).catch(err => {
        console.log('获取推荐代码失败')
        console.log(err)
      })

      if (res) {
        message.success('获取推荐代码成功')
        console.log('获取推荐代码成功' )
        console.log(res)
        commit('set_recommendCodes', res)
      }
    },

  },
  getters: {
    caseList: state => state.caseList,
    curCase: (state) => (id) => {
      return state.caseList.find(i => i[0] === id)
    },
    caseDescrtption: state => state.caseDescrtption,
    recommendLabels: state => Object.entries(state.recommendLabels).sort((i,j) => j[1]-i[1]),
    recommendCodes: state => state.recommendCodes,
  }
})