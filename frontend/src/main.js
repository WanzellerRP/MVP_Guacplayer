/**
 * Ponto de entrada da aplicação Vue.js
 * Autor: GuacPlayer Team
 * Data: 2025
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Criar aplicação
const app = createApp(App)

// Usar plugins
app.use(createPinia())
app.use(router)

// Montar aplicação
app.mount('#app')
