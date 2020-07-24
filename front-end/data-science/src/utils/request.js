
import axios from 'axios'
import {
  VueAxios
} from './axios'
import {
  notification,
  message
} from 'ant-design-vue'

// 创建 axios 实例
const service = axios.create({
  // baseURL: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8080',
  //e2e测试用
  baseURL: 'http://localhost:5000'
})
console.log('NODE_ENV: ' + process.env.NODE_ENV)

const err = (error) => {
  if (error.response) {
    const data = error.response.data
    if (error.response.status === 500) {
      notification.error({
        message: '后端错误',
        description: data.message
      })
      console.log(error.response.data.trace)
    }
    if (error.response.status === 403) {
      notification.error({
        message: 'Forbidden',
        description: data.message
      })
    }
    if (error.response.status === 401 && !(data.result && data.result.isLogin)) {
      notification.error({
        message: 'Unauthorized',
        description: 'Authorization verification failed'
      })
    }
  }
  return Promise.reject(error.response)
}

//request incerceptor
service.interceptors.request.use((config) => {

  const requestConfig = {
    ...config,
    url: `${config.url}`,
  }
  console.log('requestConfig:')
  console.log(requestConfig)
  return requestConfig
}, err)
//response incerceptor
service.interceptors.response.use((response) => {
  console.log('response')
  console.log(response)
  switch (response.status) {
    case 200:
      if (response.data.code === 0) {
        console.log(response.config.url,'获取成功，data： ')
        console.log(response.data.data)
        return response.data.data;//返回数据部分
      } else {
        console.log('错误： ' + response)
      }
      break
    case 404:
      return false
    case 500:
      console.log('500d=后端错误： ' + response)
      break;
    default:
      message.error(response.data.message)
  }
},err)

const installer = {
  vm: {},
  install(Vue) {
    Vue.use(VueAxios, service)
  }
}

export {
  installer as VueAxios,
  service as axios
}