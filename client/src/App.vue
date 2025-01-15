<template>
  <div>
    <Navbar />
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import { useUserStore } from './stores/user';

export default defineComponent({
  name: 'App',
  components: {
    Navbar,
  },
  setup() {
    const userStore = useUserStore();

    onMounted(() => {
      userStore.initializeUser();
    });

    return {};
  },
});
</script>

<style scoped></style>
