import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue'
import Logs from '@/pages/Logs.vue';
import NoVNC from '@/pages/NoVNC.vue';
import FAQ from '@/pages/FAQ.vue';
import SunshineConfig from '@/pages/SunshineConfig.vue';
import Settings from '@/pages/Settings.vue'

const routes = [
  { path: '/home', component: Home },
  { path: '/logs', component: Logs },
  { path: '/novnc', component: NoVNC },
  { path: '/faq', component: FAQ },
  { path: '/sunshineconfig', component: SunshineConfig },
  { path: '/settings', component: Settings}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkExactActiveClass: "is-active", // makes active nav link light up
});

export default router;
