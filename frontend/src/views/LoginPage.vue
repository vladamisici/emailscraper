<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-10 bg-white rounded-lg shadow-xl transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-105">
      <h2 class="mb-6 text-3xl font-bold text-center text-gray-800">Login</h2>
      <form @submit.prevent="login" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input id="username" v-model="username" class="mt-1 w-full rounded-md border-gray-300 focus:border-orange-500 focus:ring focus:ring-orange-500 focus:ring-opacity-50 placeholder-gray-400" placeholder="Enter your username">
          <p v-if="usernameError" class="mt-2 text-sm text-orange-600">{{ usernameError }}</p>
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <div class="mt-1 relative">
            <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'" class="w-full rounded-md border-gray-300 focus:border-orange-500 focus:ring focus:ring-orange-500 focus:ring-opacity-50 placeholder-gray-400" placeholder="Enter your password">
            <button type="button" @click="toggleShowPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5">
              <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'" class="text-gray-700 hover:text-orange-500"></i>
            </button>
          </div>
          <p v-if="passwordError" class="mt-2 text-sm text-orange-600">{{ passwordError }}</p>
        </div>
        <a href="#" class="text-sm text-orange-500 hover:text-orange-700 hover:underline">Forgot Password?</a>
        <button type="submit" class="w-full bg-orange-500 text-white py-2 rounded-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-opacity-50">Log in</button>
        <button @click="openGmailLogin" class="flex items-center justify-center bg-white border border-gray-300 rounded-md w-full py-2 text-gray-800 hover:bg-gray-50 focus:outline-none focus:border-blue-500 focus:ring focus:ring-blue-200">
          <img src="/src/assets/styles/images//gmail_logo.png" alt="Gmail Logo" class="w-6 h-6 mr-2">
          Login with Gmail
        </button>
      </form>
      <Toast ref="toast"></Toast>
    </div>
  </div>
</template>

<script>
import Toast from 'primevue/toast';
import 'primeicons/primeicons.css';
2
export default {
  components: {
    Toast
  },
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      usernameError: '',
      passwordError: ''
    };
  },
  methods: {
    async login() {
    this.usernameError = '';
    this.passwordError = '';
    
    if (!this.username) {
      this.usernameError = 'Username is required.';
      this.$refs.toast.add({severity: 'warn', summary: 'Validation Error', detail: 'Username is required.', life: 3000});
      return;
    }
    
    if (!this.password) {
      this.passwordError = 'Password is required.';
      this.$refs.toast.add({severity: 'warn', summary: 'Validation Error', detail: 'Password is required.', life: 3000});
      return;
    }

    try {
      const response = await fetch('/login/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: this.username, password: this.password })
      });
      
      if (response.ok) {
        const data = await response.json();
        this.$refs.toast.add({severity: 'info', summary: 'Login Successful', detail: data.message, life: 3000});
        this.$router.push('/scrape');
      } else {
        const errorData = await response.json();
        this.$refs.toast.add({severity: 'error', summary: 'Login Failed', detail: errorData.error, life: 3000});
      }
    } catch (error) {
      this.$refs.toast.add({severity: 'error', summary: 'Login Error', detail: error.message, life: 3000});
    }
  },
  openGmailLogin() {
    window.location.href = 'https://127.0.0.1:5000/login/login_oauth';
  },
    toggleShowPassword() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>
<style scoped>
input:focus {
  outline: none;
}
</style>