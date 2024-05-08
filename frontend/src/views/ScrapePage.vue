<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">fetchy.cc</h1>
    <div class="mb-4">
      <p class="text-gray-600">Logged in as {{ username }}</p>
    </div>
    <div class="flex justify-center space-x-4">
      <button @click="category = 'sent'; currentPage = 1" :class="{ 'bg-orange-500 text-white': category === 'sent', 'bg-gray-200': category !== 'sent' }" class="px-6 py-3 rounded-md focus:outline-none">Sent</button>
      <button @click="category = 'inbox'; currentPage = 1" :class="{ 'bg-orange-500 text-white': category === 'inbox', 'bg-gray-200': category !== 'inbox' }" class="px-6 py-3 rounded-md focus:outline-none">Inbox</button>
    </div>
    <div class="mt-8">
      <div v-if="category === 'sent'" class="bg-white shadow-lg rounded-lg p-6 overflow-y-auto max-h-96">
        <h2 class="text-xl font-semibold mb-4">Sent Emails</h2>
        <!-- Your existing code for displaying sent emails -->
      </div>
      <div v-else class="bg-white shadow-lg rounded-lg p-6 overflow-y-auto max-h-96">
        <h2 class="text-xl font-semibold mb-4">Inbox Emails</h2>
        <!-- Your existing code for displaying inbox emails -->
      </div>
    </div>
    <div class="flex justify-center mt-4">
      <!-- Refresh button -->
      <button @click="refreshEmails" class="flex items-center justify-center bg-gray-200 border border-gray-300 rounded-md py-2 px-4 text-gray-700 hover:bg-gray-300 focus:outline-none focus:border-blue-500 focus:ring focus:ring-blue-200">
        <img src="/src/assets/styles/Icons/refresh_icon.png" alt="Refresh Logo" class="w-6 h-6 mr-2">
        Refresh
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect, computed } from 'vue';

// Sample data for sent and inbox emails
const sentEmails = [
  // Sample sent emails data
];

const inboxEmails = [
  // Sample inbox emails data
];

const category = ref('sent');
const username = ref('John Doe'); // Sample username, replace it with actual logged-in user's name

// Method to refresh emails
const refreshEmails = async () => {
  try {
    // Fetch emails from the server
    const response = await fetch('https://127.0.0.1:5000/mail/inbox');
    const data = await response.json();

    // Update inboxEmails with new data
    inboxEmails.splice(0, inboxEmails.length, ...data);
  } catch (error) {
    console.error('Error fetching emails:', error);
    // Show error message or handle error
  }
};
</script>

<style scoped>
button {
  cursor: pointer;
}
</style>
