// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import { ElDatePicker } from 'element-plus';
import 'element-plus/theme-chalk/index.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)
app.component(ElDatePicker.name, ElDatePicker);
app.mount('#app')
