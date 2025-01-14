<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-link">Home</router-link>
      <router-link to="/profile" class="navbar-link">Profile</router-link>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Navbar',
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
</style>
