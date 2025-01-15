import { createRouter, createWebHistory } from 'vue-router';
import MainScreen from '../screens/MainScreen.vue';

import UserProfileScreen from '../screens/UserProfileScreen.vue';

const routes = [
  { path: '/', name: 'Home', component: MainScreen },
  { path: '/profile/:username', name: 'Profile', component: UserProfileScreen, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
