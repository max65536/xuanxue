// app.js
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

// 导入组件
import Home from './components/Home.vue';
import About from './components/About.vue';

// 创建 Vue Router 实例
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/about', component: About }
  ]
});

// 创建 Vue 应用程序实例
const app = createApp({
  // 组件选项
});

// 使用 Vue Router
app.use(router);

// 挂载应用程序
app.mount('#app');
