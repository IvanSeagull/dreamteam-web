# HobbiesList.vue
<template>
  <div class="hobbies-list">
    <h2 class="hobbies-title">{{ title || 'Hobbies' }}</h2>
    <div v-if="hobbies.length === 0" class="no-hobbies">
      No hobbies selected
    </div>
    <ul v-else class="hobbies-items">
      <li 
        v-for="hobby in hobbies" 
        :key="hobby.id" 
        class="hobby-item"
        :title="hobby.description || hobby.name"
      >
        {{ hobby.name }}
        <span 
          v-if="showRemove" 
          class="remove-hobby"
          @click="$emit('remove', hobby.id)"
        >
          ×
        </span>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import type { IHobby } from '../../types/user';

export default defineComponent({
  name: 'HobbiesList',
  props: {
    hobbies: {
      type: Array as PropType<IHobby[]>,
      required: true,
    },
    title: {
      type: String,
      required: false,
    },
    showRemove: {
      type: Boolean,
      default: false,
    }
  },
  emits: ['remove'],
});
</script>

<style scoped>
.hobbies-list {
  margin-top: 20px;
  text-align: left;
  color: #fff;
}

.hobbies-title {
  font-size: 1.8em;
  font-weight: bold;
  margin-bottom: 10px;
}

.hobbies-items {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hobby-item {
  background-color: #3490dc;
  color: #fff;
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 5px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: default;
}

.hobby-item:hover {
  background-color: #2779bd;
}

.remove-hobby {
  cursor: pointer;
  font-size: 1.2em;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  transition: background-color 0.2s;
}

.remove-hobby:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.no-hobbies {
  color: #666;
  font-style: italic;
  padding: 10px 0;
}
</style>