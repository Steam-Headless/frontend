import '@/assets/main.css'

import {createApp} from 'vue'
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import {createPinia} from "pinia";
import App from '@/App.vue'
import router from '@/router'

const app = createApp(App)

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            // “dark” tokens live in :root (no class needed), overriding the light ones
            darkModeSelector: ':root'
        }
    }
});

app.use(createPinia())
app.use(router)
app.mount('#app')
