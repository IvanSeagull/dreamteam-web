<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-link">Home</router-link>

      <template v-if="isLoggedIn">
        <router-link to="/profile" class="navbar-link">Profile</router-link>
        <button @click="logout" class="navbar-button">Logout</button>
      </template>

      <template v-else>
        <button @click="goToLogin" class="navbar-button">Login</button>
      </template>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'Navbar',
  setup() {
    const isLoggedIn = ref(false);
    const router = useRouter();

    onMounted(async () => {
      try {
        const resp = await fetch('http://localhost:8000/api/profile-data', {
          credentials: 'include',
        });

        console.log(resp.status);
        if (resp.status === 200) {
          isLoggedIn.value = true;
        } else {
          isLoggedIn.value = false;
        }
      } catch (error) {
        isLoggedIn.value = false;
      }
    });

    const goToLogin = () => {
      window.location.href = 'http://localhost:8000/api/login?next=http://localhost:5173/profile';
    };

    const logout = async () => {
      try {
        const resp = await fetch('http://localhost:8000/api/logout', {
          method: 'POST',
          credentials: 'include',
        });
        if (resp.ok) {
          isLoggedIn.value = false;
          router.push('/');
        } else {
          console.error('Failed to logout. Status:', resp.status);
        }
      } catch (err) {
        console.error('Logout error:', err);
      }
    };

    return {
      isLoggedIn,
      goToLogin,
      logout,
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
