<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-link">Home</router-link>

      <template v-if="userStore.isAuthenticated">
        <router-link :to="`/profile/${userStore.user?.username}`" class="navbar-link"
          >Profile</router-link
        >
        <button @click="userStore.logout" class="navbar-button" :disabled="userStore.loading">
          Logout
        </button>
      </template>

      <template v-else>
        <button @click="userStore.login" class="navbar-button">Login</button>
        <button @click="userStore.signup" class="navbar-button">Sign Up</button>
      </template>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../stores/user';

export default defineComponent({
  name: 'Navbar',
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
});
</script>

<style scoped>
.navbar {
  background-color: #333;
  color: #fff;
  padding: 1rem;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.navbar-container {
  display: flex;
  gap: 1rem;
}

.navbar-link {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}

.navbar-link:hover {
  text-decoration: underline;
}

.navbar-button {
  cursor: pointer;
  padding: 0.5rem 1rem;
  font-size: 15px;
  border: none;
  background: #444;
  color: #fff;
  border-radius: 4px;
}

.navbar-button:hover {
  background-color: #555;
}
</style>
