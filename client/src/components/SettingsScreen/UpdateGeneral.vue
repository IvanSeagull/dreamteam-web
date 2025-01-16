<template>
  <div class="update-general">
    <h2>Update General Information</h2>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>

      <button type="submit" class="save-button">Save</button>
    </form>

    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { updateGeneralInfo } from '../../services/userService';
import { useUserStore } from '../../stores/user';

export default defineComponent({
  name: 'UpdateGeneral',
  setup() {
    const userStore = useUserStore();
    const name = ref(userStore.user?.name || '');
    const email = ref(userStore.user?.email || '');
    const successMessage = ref('');
    const errorMessage = ref('');

    const handleSubmit = async () => {
      try {
        successMessage.value = '';
        errorMessage.value = '';
        const user = await updateGeneralInfo(name.value, email.value);
        userStore.updateUser(user);
        successMessage.value = 'General information updated successfully!';
      } catch (error: any) {
        console.error('Error updating general info:', error);
        errorMessage.value = error.message || 'Failed to update general info.';
      }
    };

    return {
      name,
      email,
      successMessage,
      errorMessage,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.update-general {
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

input {
  width: 100%;
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
