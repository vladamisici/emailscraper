import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Lara from './assets/styles/presets/lara'
import './style.css'
import App from './App.vue'
import router from './router'
createApp(App)
    .use(router)
    .use(PrimeVue, {
        unstyled: true,
        pt: Lara
    })
    .mount('#app')
