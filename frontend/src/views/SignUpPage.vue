<template>
  <div class="signup-page min-h-screen flex items-center justify-center bg-gray-100">
    <Toast ref="toast" />
    <div class="signup-container bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Sign Up</h1>
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label for="name" class="block text-gray-700 font-medium mb-2">Name</label>
          <input
            v-model="form.name"
            type="text"
            id="name"
            class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            required
          />
        </div>
        <div class="mb-4">
          <label for="email" class="block text-gray-700 font-medium mb-2">Email</label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            required
          />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
          <input
            v-model="form.password"
            type="password"
            id="password"
            class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            required
          />
        </div>
        <div class="mb-6">
          <label for="confirmPassword" class="block text-gray-700 font-medium mb-2">Confirm Password</label>
          <input
            v-model="form.confirmPassword"
            type="password"
            id="confirmPassword"
            class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full py-3 bg-orange-500 text-white rounded-lg font-semibold hover:bg-orange-600 transition-colors"
        >
          Sign Up
        </button>
      </form>
      <p class="text-center text-gray-600 mt-6">
        Already have an account?
        <router-link to="/login" class="text-orange-500 hover:underline">Log In</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const toast = useToast();
const router = useRouter();

const handleSubmit = () => {
  if (form.password !== form.confirmPassword) {
    toast.add({ severity: 'warn', summary: 'Warning', detail: 'Passwords do not match!', life: 3000 });
    return;
  }
  // Perform sign-up logic here (e.g., API call)
  // On successful sign-up, redirect to the dashboard or another page
  router.push('/dashboard');
};
</script>

<style scoped>
.signup-page {
  background: linear-gradient(to bottom, #e9e9e9, #f7f7f7);
}

.signup-container {
  max-width: 500px;
  background: #fff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.signup-container h1 {
  margin-bottom: 20px;
}

.signup-container form {
  display: flex;
  flex-direction: column;
}

.signup-container form input {
  margin-bottom: 10px;
}

.signup-container form button {
  margin-top: 20px;
}
</style>
