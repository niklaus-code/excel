import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import modisdownload from '@/components/modisdownload'
import head from '@/components/head'
import user from '@/components/user'
import task from '@/components/task'
import machine from '@/components/machine'


Vue.use(Router)

export default new Router({
	//mode: 'history',
  routes: [
    {
      path: '/',
      component: machine
    },
    {
      path: '/machine',
      name: 'machine',
      component: machine
    },
    {
      path: '/user',
      component: user
    },
    {
      path: '/list',
      component: HelloWorld
    },
    {
      path: '/modisdownload',
      component: modisdownload
    }
  ]
})
