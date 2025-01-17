<template>
  <div class="update-hobbies">
    <h2>Update Hobbies</h2>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="hobbies">Select Hobbies:</label>
        <select id="hobbies" v-model="selectedHobbies" multiple>
          <option v-for="hobby in availableHobbies" :key="hobby.id" :value="hobby.name">
            {{ hobby.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="new-hobby">Add New Hobby:</label>
        <input type="text" id="new-hobby" v-model="newHobby" />
        <button type="button" @click="addNewHobby" class="add-hobby-button">Add</button>
      </div>

      <button type="submit" class="save-button">Save Hobbies</button>
    </form>

    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'UpdateHobbies',
  setup() {
    const availableHobbies = ref<{ id: number; name: string }[]>([]);
    const selectedHobbies = ref<string[]>([]);
    const newHobby = ref('');
    const successMessage = ref('');
    const errorMessage = ref('');

    const addNewHobby = () => {
      if (!newHobby.value.trim()) {
        alert('Hobby name cannot be empty.');
        return;
      }

      availableHobbies.value.push({ id: Date.now(), name: newHobby.value.trim() });
      selectedHobbies.value.push(newHobby.value.trim());
      newHobby.value = '';
    };

    const handleSubmit = async () => {
      alert('Save hobbies clicked');
    };

    return {
      availableHobbies,
      selectedHobbies,
      newHobby,
      successMessage,
      errorMessage,
      handleSubmit,
      addNewHobby,
    };
  },
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

h2 {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

select {
  width: 100%;
  padding: 10px;
  border: 1px solid #555;
  border-radius: 5px;
  background-color: #444;
  color: #fff;
}

input {
  width: calc(100% - 110px);
  padding: 10px;
  border: 1px solid #555;
  border-radius: 5px;
  background-color: #444;
  color: #fff;
}

input:focus {
  border-color: #3490dc;
  outline: none;
}

.add-hobby-button {
  padding: 10px;
  margin-left: 10px;
  background-color: #3490dc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-hobby-button:hover {
  background-color: #2779bd;
}

.save-button {
  padding: 10px 20px;
  background-color: #38c172;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #2fa360;
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
