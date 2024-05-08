import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Lara from './assets/styles/presets/lara'
import './style.css'
import App from './App.vue'
import ToastService from 'primevue/toastservice';
import router from './router'

createApp(App)
    .use(router)
    .use(ToastService)
    .use(PrimeVue, {
        unstyled: true,
        pt: Lara
    })
    .mount('#app')
