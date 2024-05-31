<template>
    <div class="pricing-page min-h-screen bg-gray-100 flex flex-col items-center py-12">
      <h1 class="text-4xl font-bold text-gray-800 mb-8">Pricing Plans</h1>
      <div class="pricing-cards flex flex-wrap justify-center gap-6">
        <PricingCard
          title="Basic"
          price="Free"
          :features="['10 emails per day', 'Limited email scraping', 'Email notifications']"
          buttonText="Sign Up for Free"
        />
        <PricingCard
          title="Pro"
          price="$9.99/month"
          :features="['Unlimited emails', 'Advanced email scraping', 'Priority support', 'Daily email reports']"
          buttonText="Get Pro"
          featured
        />
        <PricingCard
          title="Enterprise"
          price="Contact Us"
          :features="['Custom email limits', 'API access', '24/7 dedicated support', 'Custom integrations', 'Advanced analytics']"
          buttonText="Contact Sales"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import PricingCard from '../components/PricingCard.vue';
  </script>
  
  <style scoped>
  .pricing-page {
    background: linear-gradient(to bottom, #f7f7f7, #e9e9e9);
  }
  
  .pricing-cards {
    max-width: 1200px;
  }
  </style>
  