<template>
  <div class="update-password">
    <h2>Update Password</h2>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="password1">New Password:</label>
        <input type="password" id="password1" v-model="password1" required />
      </div>

      <div class="form-group">
        <label for="password2">Confirm Password:</label>
        <input type="password" id="password2" v-model="password2" required />
      </div>

      <button type="submit" class="save-button">Change Password</button>
    </form>

    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { updatePassword } from '../../services/userService';

export default defineComponent({
  name: 'UpdatePassword',
  setup() {
    const password1 = ref('');
    const password2 = ref('');
    const successMessage = ref('');
    const errorMessage = ref('');

    const handleSubmit = async () => {
      try {
        successMessage.value = '';
        errorMessage.value = '';

        if (password1.value !== password2.value) {
          errorMessage.value = 'Passwords do not match.';
          return;
        }

        await updatePassword(password1.value, password2.value);
        successMessage.value = 'Password updated successfully!';
        password1.value = '';
        password2.value = '';
      } catch (error: any) {
        console.error('Error updating password:', error);
        errorMessage.value = error.message || 'Failed to update password.';
      }
    };

    return {
      password1,
      password2,
      successMessage,
      errorMessage,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.update-password {
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
