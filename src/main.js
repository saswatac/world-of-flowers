import Vue from 'vue'
import App from './App.vue'
import VueEasyLightbox from 'vue-easy-lightbox'
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false
Vue.component(VueEasyLightbox.name, VueEasyLightbox)

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAHb4ol8mTqPffGGxY02LCuRxdSr-jEIjU',
    libraries: 'places',
  }
});

new Vue({
  render: h => h(App),
}).$mount('#app')
