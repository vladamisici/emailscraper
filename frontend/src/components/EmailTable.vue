<template>
    <DataTable 
      :value="emails" 
      :paginator="true" 
      :rows="10" 
      :paginatorPosition="'both'" 
      :sortMode="'multiple'"
      @row-click="openEmail"
      class="email-table"
    >
      <Column field="from" header="From" v-if="category !== 'sent'" :body="fromTemplate" sortable />
      <Column field="to" header="To" v-if="category === 'sent'" :body="toTemplate" sortable />
      <Column field="subject" header="Subject" :body="subjectTemplate" sortable />
      <Column field="date" header="Date" :body="dateTemplate" sortable />
      <LoadingSpinner v-if="isLoading" />
    </DataTable>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import LoadingSpinner from '../components/LoadingSpinner.vue';
  import axios from 'axios';

  
  const props = defineProps({
    emails: Array,
    category: String,
    isLoading: Boolean
  });
  
  const emits = defineEmits(['openEmail']);
  
  const fromTemplate = (rowData) => {
    return `<span>${rowData.from}</span>`;
  };
  
  const toTemplate = (rowData) => {
    return `<span>${rowData.to}</span>`;
  };
  
  const subjectTemplate = (rowData) => {
    return `<span>${rowData.subject}</span>`;
  };
  
  const dateTemplate = (rowData) => {
    return `<span>${rowData.date}</span>`;
  };
  
  // const openEmail = (email) => {
  //   emits('openEmail', email);
  // };
  const openEmail = (event) => {
  const email = event.data;
  emits('openEmail', email);
};
//   const openEmail = (email) => {
//   const emailData = {
//     from: email.from,
//     to: email.to,
//     date: email.date,
//     subject: email.subject,
//     content: email.content,
//   };
//   emits('openEmail', emailData);
// };
  </script>
  
  <style scoped>
  .email-table .p-datatable-tbody > tr > td {
    cursor: pointer;
  }
  
  .email-table .p-datatable-header, 
  .email-table .p-datatable-footer {
    background-color: #f0f2f5;
    border: none;
  }
  
  .email-table .p-datatable-tbody > tr {
    transition: background-color 0.2s;
  }
  
  .email-table .p-datatable-tbody > tr:hover {
    background-color: #f0f8ff;
  }
  </style>
  