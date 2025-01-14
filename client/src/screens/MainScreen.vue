<template>
  <div>
    <h2>Hobbies app</h2>
    <button @click="goToAuth">Go to Django Login</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
  setup() {
    const goToAuth = () => {
      const djangoLoginURL = 'http://localhost:8000/api/login';
      const nextParam = '?next=http://localhost:5173';
      window.location.href = djangoLoginURL + nextParam;
    };

    return { goToAuth };
  },
});
</script>

<style scoped>
button {
  cursor: pointer;
  padding: 8px 16px;
  font-size: 16px;
}
</style>
