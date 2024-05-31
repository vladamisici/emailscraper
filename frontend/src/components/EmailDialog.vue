<template>
    <Dialog :visible="visible" @update:visible="$emit('update:visible', $event)" header="Email Details" :closable="true" :modal="true">
      <div class="email-details">
        <h3 class="email-subject">{{ email.subject }}</h3>
        <p><strong>From:</strong> {{ email.from }}</p>
        <p><strong>To:</strong> {{ email.to }}</p>
        <p><strong>Date:</strong> {{ email.date }}</p>
        <div class="email-content">
          <p>{{ email.content }}</p>
        </div>
      </div>
    </Dialog>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  import Dialog from 'primevue/dialog';
  
  const props = defineProps({
    email: Object,
    visible: Boolean
  });
  </script>
  
  <style scoped>
  .email-details {
    font-family: Arial, sans-serif;
  }
  
  .email-subject {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .email-content {
    margin-top: 15px;
    white-space: pre-line;
  }
  </style>
  