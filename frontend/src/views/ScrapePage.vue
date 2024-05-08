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
        <ul>
          <li v-for="(email, index) in paginatedEmails" :key="index" class="mb-4">
            <div class="bg-gray-100 p-4 rounded-lg">
              <h3 class="text-lg font-semibold">{{ email.title }}</h3>
              <p class="text-gray-600 mb-1">From: {{ email.sender }}</p>
              <p class="text-gray-600 mb-1">Date: {{ email.date }}</p>
              <p class="text-gray-600 mb-2">Time: {{ email.time }}</p>
              <p class="text-gray-700">{{ email.content.substring(0, 100) }}{{ email.content.length > 100 ? '...' : '' }}</p>
            </div>
          </li>
        </ul>
        <div class="flex justify-end mt-4">
          <button @click="currentPage--" :disabled="currentPage === 1" class="px-4 py-2 rounded-md bg-gray-200 text-gray-700 mr-2">Previous</button>
          <button @click="currentPage++" :disabled="currentPage === totalPages" class="px-4 py-2 rounded-md bg-gray-200 text-gray-700">Next</button>
        </div>
      </div>
      <div v-else class="bg-white shadow-lg rounded-lg p-6 overflow-y-auto max-h-96">
        <h2 class="text-xl font-semibold mb-4">Inbox Emails</h2>
        <ul>
          <li v-for="(email, index) in paginatedEmails" :key="index" class="mb-4">
            <div class="bg-gray-100 p-4 rounded-lg">
              <h3 class="text-lg font-semibold">{{ email.title }}</h3>
              <p class="text-gray-600 mb-1">From: {{ email.sender }}</p>
              <p class="text-gray-600 mb-1">Date: {{ email.date }}</p>
              <p class="text-gray-600 mb-2">Time: {{ email.time }}</p>
              <p class="text-gray-700">{{ email.content.substring(0, 100) }}{{ email.content.length > 100 ? '...' : '' }}</p>
            </div>
          </li>
        </ul>
        <div class="flex justify-end mt-4">
          <button @click="currentPage--" :disabled="currentPage === 1" class="px-4 py-2 rounded-md bg-gray-200 text-gray-700 mr-2">Previous</button>
          <button @click="currentPage++" :disabled="currentPage === totalPages" class="px-4 py-2 rounded-md bg-gray-200 text-gray-700">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect, computed } from 'vue';

// Sample data for sent and inbox emails
const sentEmails = [
  { title: 'Sent Email 1', sender: 'sender@example.com', content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', date: '2024-05-10', time: '10:00 AM' },
  { title: 'Sent Email 2', sender: 'sender@example.com', content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', date: '2024-05-09', time: '11:30 AM' },
  // Add more sample data as needed
];

const inboxEmails = [
  { title: 'Inbox Email 1', sender: 'sender@example.com', content: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', date: '2024-05-10', time: '9:45 AM' },
  { title: 'Inbox Email 2', sender: 'sender@example.com', content: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', date: '2024-05-09', time: '1:15 PM' },
  // Add more sample data as needed
];

const category = ref('sent');
const username = ref('John Doe'); // Sample username, replace it with actual logged-in user's name
const emailsPerPage = 5; // Number of emails per page
let currentPage = ref(1); // Current page number

// Computed property to filter emails based on selected category
const filteredEmails = computed(() => {
  return category.value === 'sent' ? sentEmails : inboxEmails;
});

// Computed property to paginate emails
const paginatedEmails = computed(() => {
  const startIndex = (currentPage.value - 1) * emailsPerPage;
  const endIndex = startIndex + emailsPerPage;
  return filteredEmails.value.slice(startIndex, endIndex);
});

// Computed property for total number of pages
const totalPages = computed(() => {
  return Math.ceil(filteredEmails.value.length / emailsPerPage);
});

// Watcher to reset current page when category changes
watchEffect(() => {
  currentPage.value = 1;
});
</script>

<style scoped>
button {
  cursor: pointer;
}
</style>
