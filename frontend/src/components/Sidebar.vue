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
                :icon="getIconClass(cat)"
                class="nav-button"
            />
            <Button 
                @click="showAnalysisModal = true"
                class="nav-button"
                label="Email Analysis"
                icon="pi pi-chart-bar"
            />
            <Button 
                @click="showTopSendersModal = true"
                class="nav-button"
                label="Top Senders Analysis"
                icon="pi pi-users"
            />
            <Button class="nav-button" @click="$emit('send-email')" label = "Send Email" icon="pi pi-plus"/>
        </nav>
        
    
    <Dialog v-model:visible="showAnalysisModal" header="Email Analysis" :modal="true" :style="{width: '80vw'}">
      <EmailAnalysis />
    </Dialog>
    <Dialog v-model:visible="showTopSendersModal" header="Top Email Senders" :modal="true" :style="{width: '80vw'}">
      <TopSendersAnalysis />
    </Dialog>
        <div class="logout-section mt-auto">
            <Button 
                label="Log Out" 
                class="nav-button logout-button"
                @click="logout"
            />
        </div>

    </aside>
</template>

<script setup>
import { ref } from 'vue';
import { defineProps, defineEmits } from 'vue';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import CreateLabelDialog from './CreateLabelDialog.vue';
import EmailForm from '../components/EmailForm.vue'
import axios from 'axios';
import EmailAnalysis from '../views/EmailAnalysis.vue';
import TopSendersAnalysis from '../views/TopSenders.vue';

import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  loggedInEmail: String,
  category: String,
  labels: Array 
});

const getIconClass = (category) => {
  switch (category) {
    case 'inbox':
      return 'pi pi-inbox';
    case 'sent':
      return 'pi pi-send';
    case 'spam':
      return 'pi pi-exclamation-triangle';
    case 'drafts':
      return 'pi pi-pencil';
    default:
      return 'pi pi-inbox';
  }
};


const showAnalysisModal = ref(false);
const showTopSendersModal = ref(false);

const emit = defineEmits(['setCategory', 'setLabel', 'toggleSendEmail', 'send-email']);

const categories = ['inbox', 'sent', 'drafts', 'spam'];

const setCategory = (cat) => {
  emit('setCategory', cat);
};

// const setLabel = (label) => {
//   emit('setLabel', label);
// };

const categoryButtonClass = (btnCategory) => {
  return {
    'active-button': props.category === btnCategory,
    'inactive-button': props.category !== btnCategory,
  };
};

const showCreateLabelDialog = ref(false);



const logout = () => {
  console.log('Logged out');
  window.location.href = 'https://localhost:5000/mail/logout';
};

const navigateToAnalysis = () => {
  router.push('/email-analysis');
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
  