import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import '@fortawesome/fontawesome-free/css/all.css'; // Import the Font Awesome CSS



Vue.config.productionTip = false
Vue.component('font-awesome-icon', FontAwesomeIcon)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
