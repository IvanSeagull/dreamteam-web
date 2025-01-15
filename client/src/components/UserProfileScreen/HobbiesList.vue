<template>
  <div class="hobbies-list">
    <h2 class="hobbies-title">Hobbies</h2>
    <ul class="hobbies-items">
      <li v-for="(hobby, index) in hobbies" :key="index" class="hobby-item">
        {{ hobby }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HobbiesList',
  props: {
    hobbies: {
      type: Array as () => string[],
      required: true,
    },
  },
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
  display: inline-block;
}
</style>
