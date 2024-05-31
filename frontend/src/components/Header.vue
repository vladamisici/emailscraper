<template>
    <header class="header">
      <div class="search-bar">
        <InputText :value="filterText" @input="$emit('update:filterText', $event.target.value)" placeholder="Search..." />
        <Button @click="$emit('clearFilter')" label="Clear" icon="pi pi-times" class="clear-button" />
      </div>
      <Button @click="$emit('refreshEmails')" label="Refresh" icon="pi pi-refresh" class="refresh-button" />
    </header>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  
  const props = defineProps({
    filterText: String
  });
  
  const emits = defineEmits(['update:filterText', 'clearFilter', 'refreshEmails']);
  </script>
  
  <style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
  }
  
  .search-bar {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .clear-button, .refresh-button {
    background-color: #ff5733;
    border: none;
    color: #fff;
  }
  
  .clear-button:hover, .refresh-button:hover {
    background-color: #e04e24;
  }
  </style>
  