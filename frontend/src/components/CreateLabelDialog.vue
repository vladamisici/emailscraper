<template>
    <div class="p-fluid">
      <div class="field">
        <label for="label-name" class="block text-gray-700 font-bold mb-2">Label Name</label>
        <InputText 
          v-model="labelName" 
          id="label-name" 
          class="w-full"
        />
      </div>
      <div class="field">
        <label for="label-color" class="block text-gray-700 font-bold mb-2">Label Color</label>
        <input 
          v-model="labelColor" 
          id="label-color" 
          type="color" 
          class="w-full h-10 p-1 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
        />
      </div>
      <div class="flex justify-end mt-4">
        <Button label="Cancel" class="p-button-text" @click="$emit('close')" />
        <Button label="Create" type="submit" class="p-button-success ml-2" @click="createLabel" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  
  const emit = defineEmits(['create-label', 'close']);
  
  const labelName = ref('');
  const labelColor = ref('#FF5733');
  
  const createLabel = () => {
    if (labelName.value.trim() === '') {
      alert('Label name is required.');
      return;
    }
  
    const newLabel = {
      name: labelName.value,
      color: labelColor.value
    };
  
    emit('create-label', newLabel);
    emit('close');
  };
  </script>
  
  <style scoped>
  .field {
    margin-bottom: 1rem;
  }
  
  .field label {
    margin-bottom: 0.5rem;
    display: block;
  }
  
  .field input {
    padding: 0.75rem;
    border-radius: 0.375rem;
    border: 1px solid #dcdcdc;
    width: 100%;
  }
  
  .flex {
    display: flex;
  }
  
  .justify-end {
    justify-content: flex-end;
  }
  
  .mt-4 {
    margin-top: 1rem;
  }
  </style>
  