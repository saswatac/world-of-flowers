import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '../App.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'App',
    component: App
  },
  {
    path: '/upload',
    name: 'Upload',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../Upload.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
