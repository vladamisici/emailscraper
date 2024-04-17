<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm p-8 bg-white rounded-lg shadow-md">
      <h2 class="mb-6 text-3xl font-bold text-center text-gray-700">Login</h2>
      <form @submit.prevent="login" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <InputText id="username" v-model="username" class="mt-1 w-full rounded-md border-gray-300" placeholder="Enter your username"/>
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <InputText id="password" v-model="password" type="password" class="mt-1 w-full rounded-md border-gray-300" placeholder="Enter your password"/>
        </div>
        <Button label="Log in" class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600" />
      </form>
    </div>
  </div>
</template>

<script>
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

export default {
  components: {
    InputText,
    Button
  },
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      if (this.username && this.password) {
        alert(`Login attempt with username: ${this.username}`);
      } else {
        alert('Please fill in all fields.');
      }
    }
  }
};
</script>

<style>
/* No additional styles needed unless specific adjustments are required */
</style>
