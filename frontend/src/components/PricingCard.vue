<template>
    <div :class="['pricing-card', { 'border-orange-500': featured, 'shadow-lg': featured, 'bg-white': !featured, 'bg-orange-100': featured }]">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">{{ title }}</h2>
      <p class="text-3xl font-bold text-gray-800 mb-4">{{ price }}</p>
      <ul class="features-list text-gray-700 mb-6">
        <li v-for="feature in features" :key="feature" class="mb-2 flex items-center">
          <i class="pi pi-check text-orange-500 mr-2"></i>{{ feature }}
        </li>
      </ul>
      <button @click="handleClick" :class="['pricing-button', { 'bg-orange-500 text-white': !featured, 'bg-white text-orange-500 border border-orange-500': featured }]" class="px-6 py-3 rounded-md font-medium transition-colors">
        {{ buttonText }}
      </button>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  const props = defineProps({
    title: String,
    price: String,
    features: Array,
    buttonText: String,
    featured: {
      type: Boolean,
      default: false
    }
  });
  
  const handleClick = () => {
    if (props.title === 'Enterprise') {
      window.location.href = '/contact';  // Or the appropriate route for contacting sales
    } else {
      window.location.href = '/signup';  // Or the appropriate route for signup
    }
  };
  </script>
  
  <style scoped>
  .pricing-card {
    border-radius: 12px;
    padding: 24px;
    width: 320px;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .pricing-card:hover {
    transform: translateY(-8px);
  }
  
  .features-list {
    text-align: left;
  }
  
  .pricing-button:hover {
    background-color: #f97316;  /* Hover state color */
  }
  </style>
  