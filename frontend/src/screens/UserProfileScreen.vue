<template>
  <div class="profile-container">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="user" class="content">
      <ProfileHeader
        :id="user.id"
        :name="user.name"
        :username="user.username"
        :profilePicture="'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png?20150327203541'"
        :isOwnProfile="isOwnProfile"
        :friendStatus="user.friend_status"
        @add-friend="handleAddFriend"
        @go-to-settings="handleGoToSettings"
        @accept-friend="handleAcceptFriend"
      />
      <ProfileDetails :email="user.email" :dateOfBirth="user.date_of_birth" />

      <div class="friends-section">
        <img class="friends-icon" src="/friends.png" alt="Friends" />
        <p>
          Friends: {{ user.friends_count || 0 }}
          <router-link :to="`/friends/${user.username}`" class="view-friends-link"
            >View Friends</router-link
          >
        </p>
      </div>

      <HobbiesList :hobbies="user.hobbies || ['hobby1', 'hobby2', 'hobby3']" />
    </div>
    <div v-else class="not-found">User not found.</div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getUserByUsername, sendFriendRequest } from '../services/userService';
import { useUserStore } from '../stores/user';
import type { IFindUser } from '../types/user';
import ProfileDetails from '../components/UserProfileScreen/ProfileDetails.vue';
import ProfileHeader from '../components/UserProfileScreen/ProfileHeader.vue';
import HobbiesList from '../components/UserProfileScreen/HobbiesList.vue';

export default defineComponent({
  name: 'UserProfile',
  components: {
    ProfileHeader,
    ProfileDetails,
    HobbiesList,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    const userStore = useUserStore();
    const user = ref<IFindUser | null>(null);
    const loading = ref(true);
    const error = ref('');

    const isOwnProfile = computed(() => {
      return userStore.user?.username === user.value?.username;
    });

    const loadUser = async () => {
      const username = route.params.username as string;
      if (!username) {
        error.value = 'No username provided.';
        loading.value = false;
        return;
      }
      loading.value = true;
      error.value = '';
      user.value = null;

      try {
        user.value = await getUserByUsername(username);
      } catch (err: any) {
        error.value = err.message || 'Failed to load user data.';
      } finally {
        loading.value = false;
      }
    };

    const handleAddFriend = async () => {
      if (!user.value) return;

      const success = await sendFriendRequest(user.value.id);
      if (success) {
        user.value.friend_status = 'request_sent';
      } else {
      }
    };

    const handleGoToSettings = () => {
      router.push('/settings');
    };

    const handleAcceptFriend = () => {
      alert('Accepting friend request... (functionality pending)');
    };

    onMounted(loadUser);
    watch(() => route.params.username, loadUser);

    return {
      user,
      loading,
      error,
      isOwnProfile,
      handleAddFriend,
      handleGoToSettings,
      handleAcceptFriend,
    };
  },
});
</script>

<style scoped>
.profile-container {
  width: 800px;
  margin: 50px auto;
  padding: 30px;
  background-color: #333;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  text-align: center;
}

.loading,
.error,
.not-found {
  font-size: 1.2em;
  color: #555555;
}

.error {
  color: #ff4d4f;
}

.content {
  display: flex;
  align-items: start;
  flex-direction: column;
}

.friends-section {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.friends-icon {
  width: 32px;
  height: 32px;
}
</style>
