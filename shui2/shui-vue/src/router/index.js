import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue'
import Logs from '@/pages/Logs.vue';
import NoVNC from '@/pages/NoVNC.vue';
import FAQ from '@/pages/FAQ.vue';
import SunshineConfig from '@/pages/SunshineConfig.vue';
import Settings from '@/pages/Settings.vue'
import AppManager from "@/pages/AppManager.vue";

const routes = [
  { path: '/', component: Home },
  { path: '/logs', component: Logs },
  { path: '/vnc', component: NoVNC },
  { path: '/faq', component: FAQ },
  { path: '/appmanager', component: AppManager },
  { path: '/sunshineconfig', component: SunshineConfig },
  { path: '/settings', component: Settings}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkExactActiveClass: "is-active", // makes active nav link light up
});

export default router;
