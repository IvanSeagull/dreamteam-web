import { createRouter, createWebHistory } from 'vue-router';
import MainScreen from '../screens/MainScreen.vue';
import UserProfileScreen from '../screens/UserProfileScreen.vue';
import FriendsScreen from '../screens/FriendsScreen.vue';
import SettingsScreen from '../screens/SettingsScreen.vue';

const routes = [
  { path: '/', name: 'Home', component: MainScreen },
  { path: '/profile/:username', name: 'Profile', component: UserProfileScreen, props: true },
  { path: '/friends/:username', name: 'Friends', component: FriendsScreen, props: true },
  { path: '/settings', name: 'Settings', component: SettingsScreen },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
