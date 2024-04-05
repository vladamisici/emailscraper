<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <InputText id="email" type="email" v-model="email" aria-required="true"/>
      </div>
      <div>
        <label for="password">Password:</label>
        <input id="password" type="password" v-model="password" required>
      </div>
      <button type="submit">Log In</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import InputText from 'primevue/inputtext';


const email = ref('');
const password = ref('');

function handleLogin() {
  // Implement your login logic here
  console.log('Login attempt with:', email.value, password.value);
}
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  margin-bottom: 20px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b883;
  border: none;
  color: white;
  cursor: pointer;
}
button:hover {
  background-color: #369b76;
}
</style>
