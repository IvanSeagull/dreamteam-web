import { createRouter, createWebHistory } from 'vue-router';
import MainScreen from '../screens/MainScreen.vue';
import ProfileScreen from '../screens/ProfileScreen.vue';

const routes = [
  { path: '/', name: 'Home', component: MainScreen },
  { path: '/profile', name: 'Profile', component: ProfileScreen },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
