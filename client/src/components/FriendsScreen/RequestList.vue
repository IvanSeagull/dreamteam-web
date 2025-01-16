<template>
  <div class="requests-list">
    <h2>Friend Requests</h2>
    <ul>
      <li v-for="request in requests" :key="request.id" class="request-item">
        <div>
          <strong>{{ request.sender_name }}</strong> (@{{ request.sender_username }})
        </div>
        <div class="actions">
          <button @click="acceptRequest(request.id)" class="accept-button">Accept</button>
          <button @click="rejectRequest(request.id)" class="reject-button">Reject</button>
        </div>
      </li>
    </ul>
    <p v-if="!requests.length">No pending friend requests.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import {
  acceptFriendRequest,
  getFriendRequests,
  rejectFriendRequest,
} from '../../services/userService';

export default defineComponent({
  name: 'RequestsList',
  setup() {
    const requests = ref<any[]>([]);
    const loading = ref(true);
    const error = ref('');

    const loadRequests = async () => {
      try {
        const res = await getFriendRequests();
        console.log(res);
        requests.value = res;
      } catch (err) {
        console.error('Error loading requests:', err);
        error.value = 'Failed to load friend requests.';
      } finally {
        loading.value = false;
      }
    };

    const acceptRequest = async (requestId: number) => {
      //   alert(`Accept request ${requestId}`);
      try {
        const success = await acceptFriendRequest(requestId);
        if (success) {
          requests.value = requests.value.filter((req) => req.id !== requestId);
        } else {
          alert('Failed to accept friend request.');
        }
      } catch (err) {
        console.error('Error accepting request:', err);
        alert('Error accepting friend request.');
      }
    };

    const rejectRequest = async (requestId: number) => {
      //   alert(`Reject request ${requestId}`);
      try {
        const success = await rejectFriendRequest(requestId);
        if (success) {
          requests.value = requests.value.filter((req) => req.id !== requestId);
        } else {
          alert('Failed to reject friend request.');
        }
      } catch (err) {
        console.error('Error rejecting request:', err);
        alert('Error rejecting friend request.');
      }
    };

    onMounted(loadRequests);

    return {
      requests,
      loading,
      error,
      acceptRequest,
      rejectRequest,
    };
  },
});
</script>

<style scoped>
.requests-list {
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
}

.actions button {
  margin-left: 10px;
}

.accept-button {
  background-color: #38c172;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.accept-button:hover {
  background-color: #2fa360;
}

.reject-button {
  background-color: #e3342f;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reject-button:hover {
  background-color: #cc1f1a;
}
</style>
