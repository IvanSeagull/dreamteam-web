<template>
  <div v-if="userStore.isAuthenticated">
    <ul class = "friends">
      <li v-for="friend in friends" :key="friend.username" class="friend">
        <div>
          <p>{{ friend.username }} </p> <br />
          <p>{{ friend.name }} </p> <br />
          <p>{{ friend.age }} </p> <br />
          <strong>Hobbies:</strong>
          <ul class="hobbies"> 
            <li v-for="hobby in friend.hobbies">{{ hobby }}</li>
          </ul>
        </div>
      </li>
    </ul>
  </div>  
  
  <div v-else>
    <h2>Hobbies app</h2>
      <button @click="goToAuth">Go to Django Login</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../stores/user';


export default defineComponent({
  name: 'HomeView',
  setup() {
    const goToAuth = () => {
      const djangoLoginURL = 'http://localhost:8000/api/login';
      const nextParam = '?next=http://localhost:5173';
      window.location.href = djangoLoginURL + nextParam;
    };

    const userStore = useUserStore();

    const friends = [{name: "Cunix", username: "user1", age: "21", hobbies: ["karate", "wrestling", "kickboxing", "grappling"]}, 
    {name: "Popusk", username: "user3", age: "23", hobbies: ["sambo", "grappling", "karate"]},
    {name: "Propeller", username: "user3", age: "20", hobbies: ["sambo", "grappling", "karate"]},
    {name: "Kloun", username: "user3", age: "22", hobbies: ["sambo", "grappling", "karate"]},
    {name: "Popeta", username: "user3", age: "19", hobbies: ["sambo", "grappling", "karate"]},
    {name: "Popuskatel", username: "user3", age: "21", hobbies: ["sambo", "grappling", "karate"]},
    {name: "Popuskatel", username: "user3", age: "21", hobbies: ["sambo", "grappling", "karate"]},
  ];


    return { goToAuth, userStore, friends };
  },
});
</script>

<style scoped>
button {
  cursor: pointer;
  padding: 8px 16px;
  font-size: 16px;
}

.friends{
  display: flex;
  justify-content: space-between;

  position: absolute;
  left: 370px;
  top: 155px;
  width: 1000px;
  flex-wrap: wrap;
  
}

.friends .friend{
  border: 1px solid white;
  list-style-type: none;
  column-gap: 20px;
  width: 400px;
  margin-bottom: 35px;
  
  border-radius: 20px;
  padding-top: 25px;
  padding-bottom: 25px;
  transition-duration: 0.8s;

  box-shadow: 4px 4px 
}

.friends .friend:hover{
  transform: scale(1.05);
  
}



.hobbies{
  display: flex;
  margin-left: 15px;
  flex-wrap: wrap;
 

}

.hobbies li{
  list-style-type: none;
  margin-left: 50px

}


</style>
