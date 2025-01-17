# UpdateHobbies.vue
<template>
  <div class="update-hobbies">
    <h2>Update Hobbies</h2>

    <div class="selected-hobbies" v-if="selectedHobbyIds.length">
      <h3>Your Selected Hobbies:</h3>
      <div class="hobby-tags">
        <div v-for="id in selectedHobbyIds" :key="id" class="hobby-tag">
          {{ getHobbyName(id) }}
          <button class="remove-hobby" @click="removeHobby(id)">&times;</button>
        </div>
      </div>
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="hobbies">Available Hobbies:</label>
        <div class="hobby-list">
          <div 
            v-for="hobby in availableHobbies" 
            :key="hobby.id" 
            class="hobby-item"
            :class="{ selected: isSelected(hobby.id) }"
            @click="toggleHobby(hobby.id)"
          >
            <span class="hobby-name">{{ hobby.name }}</span>
            <span class="hobby-check">✓</span>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label for="new-hobby">Add New Hobby:</label>
        <div class="add-hobby-group">
          <input 
            type="text" 
            id="new-hobby" 
            v-model="newHobby"
            @keyup.enter="addNewHobby"
            placeholder="Enter hobby name"
          />
          <button 
            type="button" 
            @click="addNewHobby" 
            class="add-hobby-button" 
            :disabled="addingHobby || !newHobby.trim()"
          >
            {{ addingHobby ? 'Adding...' : 'Add' }}
          </button>
        </div>
      </div>

      <button type="submit" class="save-button" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save Hobbies' }}
      </button>
    </form>

    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from '../../stores/user';
import type { IHobby } from '../../types/user';
import { addHobby, getAllHobbies, updateUserHobbies } from '../../services/userService';

const userStore = useUserStore();
const availableHobbies = ref<IHobby[]>([]);
const selectedHobbyIds = ref<number[]>([]);
const newHobby = ref('');
const successMessage = ref('');
const errorMessage = ref('');
const saving = ref(false);
const addingHobby = ref(false);

const getHobbyName = (id: number): string => {
  const hobby = availableHobbies.value.find(h => h.id === id);
  return hobby?.name || '';
};

const isSelected = (id: number): boolean => {
  return selectedHobbyIds.value.includes(id);
};

const toggleHobby = (id: number) => {
  const index = selectedHobbyIds.value.indexOf(id);
  if (index === -1) {
    selectedHobbyIds.value.push(id);
  } else {
    selectedHobbyIds.value.splice(index, 1);
  }
};

const removeHobby = (id: number) => {
  selectedHobbyIds.value = selectedHobbyIds.value.filter(hobbyId => hobbyId !== id);
};

const initializeHobbies = async () => {
  try {
    const hobbies = await getAllHobbies();
    availableHobbies.value = hobbies;
    
    if (userStore.user?.hobbies) {
      selectedHobbyIds.value = userStore.user.hobbies.map(h => h.id);
    }
  } catch (error) {
    console.error('Error fetching hobbies:', error);
    errorMessage.value = 'Failed to load hobbies.';
  }
};

const addNewHobby = async () => {
  if (!newHobby.value.trim()) return;

  addingHobby.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const hobby = await addHobby(newHobby.value.trim());
    availableHobbies.value.push(hobby);
    selectedHobbyIds.value.push(hobby.id);
    newHobby.value = '';
    successMessage.value = 'New hobby added successfully!';
  } catch (error) {
    console.error('Error adding hobby:', error);
    errorMessage.value = 'Failed to add new hobby.';
  } finally {
    addingHobby.value = false;
  }
};

const handleSubmit = async () => {
  saving.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const updatedHobbies = await updateUserHobbies(selectedHobbyIds.value);
    
    if (userStore.user) {
      userStore.updateUser({
        ...userStore.user,
        hobbies: updatedHobbies
      });
    }
    
    successMessage.value = 'Hobbies updated successfully!';
  } catch (error) {
    console.error('Error updating hobbies:', error);
    errorMessage.value = 'Failed to update hobbies.';
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  initializeHobbies();
});
</script>

<style scoped>
.update-hobbies {
  padding: 20px;
  background-color: #333;
  color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.selected-hobbies {
  margin-bottom: 20px;
}

.hobby-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.hobby-tag {
  background-color: #3490dc;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.remove-hobby {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  opacity: 0.7;
}

.remove-hobby:hover {
  opacity: 1;
}

.hobby-list {
  background-color: #444;
  border: 1px solid #555;
  border-radius: 5px;
  max-height: 150px;
  overflow-y: auto;
}

.hobby-item {
  padding: 10px 15px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #555;
}

.hobby-item:last-child {
  border-bottom: none;
}

.hobby-item:hover {
  background-color: #4a5568;
}

.hobby-item.selected {
  background-color: #2d4a8a;
}

.hobby-item.selected:hover {
  background-color: #1a365d;
}

.hobby-check {
  opacity: 0;
  color: #38c172;
}

.hobby-item.selected .hobby-check {
  opacity: 1;
}

.add-hobby-group {
  display: flex;
  gap: 10px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #555;
  border-radius: 5px;
  background-color: #444;
  color: #fff;
}

.add-hobby-button {
  padding: 10px 20px;
  background-color: #3490dc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-button {
  padding: 12px 24px;
  background-color: #38c172;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s ease;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  transform: translateY(-1px);
}

.success-message {
  color: #38c172;
  margin-top: 15px;
}

.error-message {
  color: #e3342f;
  margin-top: 15px;
}
</style>