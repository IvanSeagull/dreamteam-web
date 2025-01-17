<template>
  <div class="profile-details">
    <div class="profile-details-item">
      <img class="profile-details-item-icon" />
      <p class="profile-info">{{ email }}</p>
    </div>
    <div class="profile-details-item">
      <img class="profile-details-item-icon" />
      <p class="profile-info">{{ formattedDateOfBirth }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { formatDateOfBirth } from '../../utils/dateUtils';

export default defineComponent({
  name: 'ProfileDetails',
  props: {
    email: {
      type: String,
      required: true,
    },
    dateOfBirth: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const formattedDateOfBirth = computed(() => formatDateOfBirth(props.dateOfBirth));

    return {
      formattedDateOfBirth,
    };
  },
});
</script>

<style scoped>
.profile-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.profile-details-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}

.profile-details-item-icon {
  width: 20px;
  height: 20px;
  background-color: #3490dc;
  border-radius: 50%;
}

.profile-info {
  color: #fff;
  font-size: 1.2em;
}
</style>
