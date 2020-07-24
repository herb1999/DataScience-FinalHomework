import Vue from 'vue'
import VueRouter from 'vue-router'
import test from '../views/test.vue'
import index from '../views/index.vue'
Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'index',
    component: index
  },
  {
    path: '/test/:testId', //动态路由参数，用$route.params.hotelId使用
    name: 'test',
    component: test
  }
]

const router = new VueRouter({
  routes
})

export default router