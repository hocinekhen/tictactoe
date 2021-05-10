import Vue from 'vue'

import VueRouter from "vue-router"
import Board from "./components/Board.vue"
Vue.config.productionTip = false
Vue.use(VueRouter)

const routes = [

  { name: 'Board', path: '/board', component: Board },
  {
    path: '*',
    redirect: '/board'
  },
]
export default new VueRouter({
  mode: 'history',
  routes: routes
})
