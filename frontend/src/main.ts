import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import 'nes.css/css/nes.min.css' // 引入核心样式库
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.mount('#app')