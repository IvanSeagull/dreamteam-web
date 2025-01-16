<template>
  <div class="friends-list">
    <h2>Your Friends</h2>
    <ul>
      <li
        v-for="friend in friends"
        :key="friend.id"
        class="friend-item"
        @click="navigateToProfile(friend.username)"
      >
        <div>
          <strong>{{ friend.name }}</strong> (@{{ friend.username }})
        </div>
      </li>
    </ul>
    <p v-if="!friends.length">No friends found for this user.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getFriends } from '../../services/userService';

export default defineComponent({
  name: 'FriendsList',
  setup() {
    const friends = ref<any[]>([]);
    const loading = ref(true);
    const error = ref('');
    const route = useRoute();
    const router = useRouter();

    const loadFriends = async () => {
      const username = route.params.username as string;
      if (!username) {
        error.value = 'No username provided in the route.';
        loading.value = false;
        return;
      }

      try {
        friends.value = await getFriends(username);
      } catch (err) {
        console.error('Error loading friends:', err);
        error.value = 'Failed to load friends.';
      } finally {
        loading.value = false;
      }
    };

    const navigateToProfile = (username: string) => {
      router.push(`/profile/${username}`);
    };

    onMounted(loadFriends);

    return {
      friends,
      loading,
      error,
      navigateToProfile,
    };
  },
});
</script>

<style scoped>
.friends-list {
  margin-top: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #444;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

li:hover {
  background-color: #555;
}

.friend-item {
  color: white;
}

.loading {
  color: #f6ad55;
}

.error {
  color: #e3342f;
}
</style>
