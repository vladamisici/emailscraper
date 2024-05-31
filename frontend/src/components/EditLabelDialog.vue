<template>
    <transition name="fade">
      <div v-if="visible" class="dialog-overlay">
        <div class="dialog-container">
          <div class="dialog-header">
            <h3>Edit Label Criteria</h3>
            <button class="close-button" @click="closeDialog">✕</button>
          </div>
          <div class="dialog-body">
            <label for="criteria">Criteria (e.g., @organization.com):</label>
            <input
              id="criteria"
              v-model="criteriaText"
              type="text"
              placeholder="Enter criteria"
            />
          </div>
          <div class="dialog-footer">
            <button class="button cancel-button" @click="closeDialog">Cancel</button>
            <button class="button save-button" @click="saveCriteria">Save</button>
          </div>
        </div>
      </div>
    </transition>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';
  
  const props = defineProps({
    visible: {
      type: Boolean,
      required: true,
    },
    label: {
      type: Object,
      required: true,
    },
  });
  
  const emit = defineEmits(['update:visible', 'saveLabelCriteria']);
  
  const criteriaText = ref('');
  
  watch(
    () => props.visible,
    (newVal) => {
      if (newVal) {
        criteriaText.value = props.label.criteria ? props.label.criteria.toString() : '';
      }
    }
  );
  
  const closeDialog = () => {
    emit('update:visible', false);
  };
  
  const saveCriteria = () => {
    const newCriteria = (email) => email.from.includes(criteriaText.value);
    emit('saveLabelCriteria', props.label, newCriteria);
    closeDialog();
  };
  </script>
  
  <style scoped>
  .dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .dialog-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    width: 400px;
    max-width: 90%;
    animation: fadeIn 0.3s ease;
  }
  
  .dialog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .dialog-header h3 {
    margin: 0;
    font-size: 1.25rem;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
  }
  
  .dialog-body {
    padding: 16px;
  }
  
  .dialog-body label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
  }
  
  .dialog-body input {
    width: 100%;
    padding: 8px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    padding: 16px;
    border-top: 1px solid #e0e0e0;
  }
  
  .button {
    padding: 8px 16px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
  }
  
  .cancel-button {
    background: #f0f0f0;
    margin-right: 8px;
  }
  
  .save-button {
    background: #007bff;
    color: white;
  }
  
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s;
  }
  
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  </style>
  