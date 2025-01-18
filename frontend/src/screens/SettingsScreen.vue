<template>
  <div class="settings-page">
    <div class="settings-sidebar">
      <button
        class="tab-button"
        :class="{ active: activeTab === 'general' }"
        @click="activeTab = 'general'"
      >
        General
      </button>
      <button
        class="tab-button"
        :class="{ active: activeTab === 'security' }"
        @click="activeTab = 'security'"
      >
        Security
      </button>
      <button
        class="tab-button"
        :class="{ active: activeTab === 'hobbies' }"
        @click="activeTab = 'hobbies'"
      >
        Hobbies
      </button>
    </div>

    <div class="settings-content">
      <UpdateGeneral v-if="activeTab === 'general'" />
      <UpdatePassword v-if="activeTab === 'security'" />
      <UpdateHobbies v-if="activeTab === 'hobbies'" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import UpdateGeneral from '../components/SettingsScreen/UpdateGeneral.vue';
import UpdatePassword from '../components/SettingsScreen/UpdatePassword.vue';
import UpdateHobbies from '../components/SettingsScreen/UpdateHobbies.vue';

export default defineComponent({
  name: 'SettingsScreen',
  components: {
    UpdateGeneral,
    UpdatePassword,
    UpdateHobbies,
  },
  setup() {
    const activeTab = ref('general');

    return {
      activeTab,
    };
  },
});
</script>

<style scoped>
.settings-page {
  display: flex;
  gap: 30px;
  width: 800px;
  min-height: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #333;
  color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.settings-sidebar {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tab-button {
  padding: 10px;
  background-color: #444;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.3s;
}

.tab-button.active {
  background-color: #3490dc;
}

.tab-button:hover:not(.active) {
  background-color: #555;
}

.settings-content {
  flex: 1;
}
</style>
