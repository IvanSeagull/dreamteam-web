<template>
  <div>
    <h2>Profile Screen</h2>
    <p v-if="error">{{ error }}</p>

    <div v-else-if="user">
      <p>Username: {{ user.username }}</p>
      <p>Email: {{ user.email }}</p>
      <p>Name: {{ user.name }}</p>
      <p>Date of Birth: {{ user.date_of_birth }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

interface UserData {
  id: number;
  username: string;
  email: string;
  name: string;
  date_of_birth: string;
}

export default defineComponent({
  name: 'ProfileScreen',
  setup() {
    const user = ref<UserData | null>(null);
    const error = ref<string | null>(null);

    onMounted(async () => {
      try {
        const resp = await fetch('http://localhost:8000/api/profile-data', {
          credentials: 'include',
        });
        if (!resp.ok) {
          throw new Error(`Failed to fetch user data: ${resp.status}`);
        }
        user.value = await resp.json();
      } catch (err: any) {
        error.value = err.message;
      }
    });

    return { user, error };
  },
});
</script>
