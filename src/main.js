import Vue from 'vue'
import App from './App.vue'
import VueEasyLightbox from 'vue-easy-lightbox'
import * as VueGoogleMaps from 'vue2-google-maps'
import 'leaflet/dist/leaflet.css';
import { Icon } from 'leaflet';
import vuetify from './plugins/vuetify'

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

Vue.config.productionTip = false
Vue.component(VueEasyLightbox.name, VueEasyLightbox)

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAHb4ol8mTqPffGGxY02LCuRxdSr-jEIjU',
    libraries: 'places',
  }
});

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
