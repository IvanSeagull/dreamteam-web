# screens/MainScreen.vue
<template>
  <div class="main-screen">
    <!-- Login Prompt -->
    <div v-if="!userStore.isAuthenticated" class="auth-prompt">
      <h1>Welcome to Hobbies App</h1>
      <p>Please log in to see users with similar hobbies</p>
      <button @click="goToAuth" class="auth-button">Go to Login</button>
    </div>

    <!-- Main Content -->
    <div v-else class="content">
      <h1>Users with Similar Hobbies</h1>

      <!-- Filters -->
      <div class="filters">
        <div class="filter-group">
          <label>Min Age: <input type="number" v-model="minAge" @change="handleFilter" /></label>
          <label>Max Age: <input type="number" v-model="maxAge" @change="handleFilter" /></label>
          <button @click="clearFilters">Clear</button>
        </div>
      </div>

      <!-- Users List -->
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else-if="!users.length">No users found with similar hobbies</div>
      <div v-else class="users-grid">
        <div v-for="user in users" :key="user.id" class="user-card">
          <RouterLink :to="{ name: 'Profile', params: { username: user.username } }">
            <h3>{{ user.name }}</h3>
            <p>@{{ user.username }}</p>
            <p>Age: {{ user.age }}</p>
            <p>Common Hobbies ({{ user.common_hobbies_count }}):</p>
            <div class="hobby-tags">
              <span v-for="hobby in user.common_hobbies" :key="hobby.name">{{ hobby.name }}</span>
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="users.length" class="pagination">
        <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from '../stores/user';
import { getSimilarUsers } from '../services/userService';
import type { ISimilarUser } from '../types/user';

const userStore = useUserStore();
const users = ref<ISimilarUser[]>([]);
const currentPage = ref(1);
const totalPages = ref(0);
const loading = ref(false);
const error = ref<string | null>(null);
const minAge = ref<number | null>(null);
const maxAge = ref<number | null>(null);

const fetchUsers = async (page: number) => {
  loading.value = true;
  try {
    const response = await getSimilarUsers(
      page,
      minAge.value ?? undefined,
      maxAge.value ?? undefined,
    );
    users.value = response.users;
    totalPages.value = response.total_pages;
    currentPage.value = response.current_page;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch users';
  } finally {
    loading.value = false;
  }
};

const handleFilter = () => {
  currentPage.value = 1;
  fetchUsers(1);
};

const clearFilters = () => {
  minAge.value = null;
  maxAge.value = null;
  handleFilter();
};

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) fetchUsers(page);
};

const goToAuth = () => {
  window.location.href = 'http://localhost:8000/api/login/?next=http://localhost:5173/profile';
};

onMounted(() => {
  if (userStore.isAuthenticated) fetchUsers(1);
});
</script>

<style scoped>
.main-screen {
  min-height: 100vh;
  color: white;
  padding: 20px;
}

.auth-prompt {
  text-align: center;
  padding: 40px;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-button {
  margin-top: 20px;
}

.filters {
  margin: 20px 0;
  padding: 15px;
  background: #2d3748;
  border-radius: 8px;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.user-card {
  background: #2d3748;
  padding: 20px;
  border-radius: 8px;
}

.content {
  margin-top: 5rem;
}
.hobby-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 10px 0;
}

.hobby-tags span {
  background: #4299e1;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.friend-button {
  width: 100%;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.friend-button.not_friends {
  background: #48bb78;
  color: white;
}

.friend-button.friends {
  background: #4299e1;
  color: white;
  cursor: default;
}

.friend-button.request_sent {
  background: #718096;
  color: white;
  cursor: default;
}

.friend-button.request_received {
  background: #ed8936;
  color: white;
}

.friend-button.sending {
  opacity: 0.7;
  cursor: wait;
}

.friend-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.pagination button {
  color: white;
  border-color: white;
}

a {
  color: white;
  text-decoration: none;
}

input {
  background: #1a1a1a;
  border: 1px solid #4a5568;
  color: white;
  padding: 5px;
  border-radius: 4px;
  margin: 0 10px;
}

.filters .filter-group button {
  color: white;
}
</style>
