<template>
  <div class="profile-header">
    <div class="profile-top">
      <img :src="profilePicture" alt="Profile Picture" class="profile-picture" />
      <div class="profile-username-content">
        <h1 class="profile-name">{{ name }}</h1>
        <p class="profile-username">@{{ username }}</p>
      </div>
    </div>

    <div class="buttons">
      <button v-if="isOwnProfile" @click="onGoToSettings" class="button settings-button">
        Settings
      </button>
      <button v-else @click="onAddFriend" class="button add-friend-button">Add Friend</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProfileHeader',
  props: {
    name: {
      type: String,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    profilePicture: {
      type: String,
      required: true,
      default:
        'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png?20150327203541',
    },
    isOwnProfile: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['add-friend', 'go-to-settings'],
  methods: {
    onAddFriend() {
      this.$emit('add-friend');
    },
    onGoToSettings() {
      this.$emit('go-to-settings');
    },
  },
});
</script>

<style scoped>
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  width: 100%;
  margin-bottom: 32px;
}

.profile-top {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #3490dc;
}

.profile-username-content {
  text-align: left;
  display: flex;
  flex-direction: column;
}

.profile-name {
  font-size: 2.1em;
  font-weight: bold;
  color: #fff;
}

.profile-username {
  font-size: 1.5em;
  color: #fff;
  font-weight: bold;
}

.buttons {
  padding: 20px 0;
}

.button {
  padding: 10px 20px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin: 0 10px;
}

.settings-button {
  background-color: #3490dc;
  color: #ffffff;
}

.settings-button:hover {
  background-color: #2779bd;
}

.add-friend-button {
  background-color: #38c172;
  color: #ffffff;
}

.add-friend-button:hover {
  background-color: #2fa360;
}

@media (max-width: 600px) {
  .profile-container {
    padding: 20px;
    margin: 20px;
  }

  .profile-name {
    font-size: 1.5em;
  }

  .button {
    width: 100%;
    margin: 10px 0;
  }

  .buttons {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .profile-info {
    font-size: 0.9em;
  }
}
</style>
