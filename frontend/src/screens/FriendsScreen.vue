<template>
  <div class="friends-page">
    <h1>Friends</h1>

    <div class="tabs">
      <button
        class="tab-button"
        :class="{ active: activeTab === 'friends' }"
        @click="activeTab = 'friends'"
      >
        Friends
      </button>
      <button
        v-if="isOwnProfile"
        class="tab-button"
        :class="{ active: activeTab === 'requests' }"
        @click="activeTab = 'requests'"
      >
        Requests
      </button>
    </div>

    <FriendsList v-if="activeTab === 'friends'" />

    <RequestList v-else-if="activeTab === 'requests'" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import FriendsList from '../components/FriendsScreen/FriendsList.vue';
import RequestList from '../components/FriendsScreen/RequestList.vue';
import { useUserStore } from '../stores/user';

export default defineComponent({
  name: 'FriendsScreen',
  components: { FriendsList, RequestList },
  setup() {
    const route = useRoute();
    const activeTab = ref('friends');
    const userStore = useUserStore();

    const isOwnProfile = computed(() => {
      const username = route.params.username as string;
      return userStore.user?.username === username;
    });

    return {
      activeTab,
      isOwnProfile,
    };
  },
});
</script>

<style scoped>
.friends-page {
  width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #333;
  color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tabs {
  display: flex;
  justify-content: center;
  margin: 20px 0;
  gap: 8px;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #555;
  color: white;
  transition: background-color 0.3s;
}

.tab-button.active {
  background-color: #3490dc;
}

.tab-button:hover:not(.active) {
  background-color: #444;
}
</style>
