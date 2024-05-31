<template>
    <aside class="sidebar">
        <div class="sidebar-header">
            <h1 class="title">fetchy.cc</h1>
            <p class="logged-in-email">Logged in as {{ loggedInEmail }}</p>
        </div>
        <nav class="nav-menu">
            <Button 
                v-for="cat in categories" 
                :key="cat" 
                @click="setCategory(cat)" 
                :class="categoryButtonClass(cat)" 
                :label="cat.charAt(0).toUpperCase() + cat.slice(1)"
                class="nav-button"
            />
        </nav>
        <div class="labels-section">
            <div class="labels-header flex justify-between items-center">
                <label class="block text-gray-700 font-bold">Labels</label>
                <Button 
                    icon="pi pi-plus" 
                    class="p-button-rounded p-button-text p-button-icon-only"
                    @click="showCreateLabelDialog = true" 
                />
            </div>
            <div class="labels-list mt-2">
                <span 
                    v-for="label in labels" 
                    :key="label.name" 
                    @click="setLabel(label)"
                    class="label-item inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
                    :style="{ backgroundColor: label.color }"
                >
                    {{ label.name }}
                </span>
            </div>
        </div>
        <div class="logout-section mt-auto">
            <Button 
                label="Log Out" 
                class="nav-button logout-button"
                @click="logout"
            />
        </div>
        <Dialog
            v-model:visible="showCreateLabelDialog"
            header="Create New Label"
            :modal="true"
            :closable="false"
            class="w-full max-w-sm"
        >
            <CreateLabelDialog @close="showCreateLabelDialog = false" @create-label="addLabel" />
        </Dialog>
    </aside>
</template>

<script setup>
import { ref } from 'vue';
import { defineProps, defineEmits } from 'vue';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import CreateLabelDialog from './CreateLabelDialog.vue';
import axios from 'axios';

const props = defineProps({
  loggedInEmail: String,
  category: String,
  labels: Array  // Ensure labels prop is defined
});

const emit = defineEmits(['setCategory', 'setLabel']);

const categories = ['inbox', 'sent', 'drafts', 'archive'];

const setCategory = (cat) => {
  emit('setCategory', cat);
};

const setLabel = (label) => {
  emit('setLabel', label);
};

const categoryButtonClass = (btnCategory) => {
  return {
    'active-button': props.category === btnCategory,
    'inactive-button': props.category !== btnCategory,
  };
};

const showCreateLabelDialog = ref(false);

const logout = () => {
  console.log('Logged out');
  window.location.href = 'https://127.0.0.1:5000/mail/logout';
};
</script>
  
  <style scoped>
  .sidebar {
    width: 250px;
    background-color: #fff;
    border-right: 1px solid #e6e6e6;
    display: flex;
    flex-direction: column;
    padding: 20px;
    transition: width 0.3s;
  }
  
  .sidebar-header {
    margin-bottom: 30px;
    text-align: center;
  }
  
  .title {
    font-size: 1.8rem;
    color: #ff5733;
    margin-bottom: 0.5rem;
  }
  
  .logged-in-email {
    color: #666;
    font-size: 0.9rem;
  }
  
  .nav-menu {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .nav-button {
    width: 100%;
    text-align: left;
    font-size: 1rem;
    padding: 10px 20px;
    background-color: transparent;
    border: 1px solid #ff5733;
    color: #ff5733;
    border-radius: 4px;
    transition: background-color 0.3s, color 0.3s;
  }
  
  .nav-button:hover {
    background-color: #ff5733;
    color: #fff;
  }
  
  .active-button {
    background-color: #ff5733 !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(255, 87, 51, 0.3);
  }
  
  .inactive-button {
    background-color: transparent;
    border: 1px solid #ff5733;
    color: #ff5733;
  }
  
  .inactive-button:hover {
    background-color: #ff5733 !important;
    color: #fff !important;
  }
  
  .labels-section {
    margin-top: 15px;
  }
  
  .labels-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .labels-list {
    margin-top: 5px;
  }
  
  .label-item {
    cursor: pointer;
  }
  
  .logout-section {
    padding-top: 15px;
  }
  
  .logout-button {
    background-color: transparent;
    border: 1px solid #ff5733;
    color: #ff5733;
    border-radius: 4px;
  }
  
  .logout-button:hover {
    background-color: #ff5733 !important;
    color: #fff !important;
  }
  
  /* Media Queries for Responsive Design */
  @media (max-width: 1024px) {
    .sidebar {
      width: 200px;
    }
  }
  
  @media (max-width: 768px) {
    .sidebar {
      width: 150px;
    }
    .title {
      font-size: 1.5rem;
    }
    .nav-button {
      font-size: 0.9rem;
    }
  }
  </style>
  