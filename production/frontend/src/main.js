import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'
import VueApexCharts from "vue3-apexcharts";
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import "./assets/custom.css";
const vuetify = createVuetify({
  components,
  directives
})


createApp(App).use(vuetify).use(VueApexCharts).use(store).use(i18n).use(router).mount('#app')
