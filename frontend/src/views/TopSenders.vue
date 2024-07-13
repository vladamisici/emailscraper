<template>
  <div class="top-senders-analysis">
    <div v-if="loading" class="loading-overlay">
      <ProgressSpinner />
      <p>Analyzing top email senders...</p>
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else class="chart-container">
      <h2>Top Email Senders</h2>
      <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import axios from 'axios';
import ProgressSpinner from 'primevue/progressspinner';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const loading = ref(true);
const error = ref(null);
const chartData = ref(null);

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Top 10 Email Senders' }
  },
  scales: {
    y: { 
      beginAtZero: true, 
      title: { display: true, text: 'Number of Emails' },
      ticks: { stepSize: 1 }
    },
    x: {
      title: { display: true, text: 'Sender' },
      ticks: { maxRotation: 45, minRotation: 45 }
    }
  }
};

const fetchTopSendersData = async () => {
  try {
    const response = await axios.get('https://localhost:5000/mail/top-senders', { withCredentials: true });
    const data = response.data;
    console.log('Received data:', data);

    if (!data.senders || !data.counts || data.senders.length === 0) {
      throw new Error('Invalid data received from server');
    }

    chartData.value = {
      labels: data.senders,
      datasets: [{
        data: data.counts,
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
      }]
    };
    console.log('Chart data:', chartData.value);
    loading.value = false;
  } catch (err) {
    console.error('Error fetching top senders data:', err);
    error.value = 'Failed to load top senders data. Please try again.';
    loading.value = false;
  }
};

onMounted(fetchTopSendersData);
</script>

<style scoped>
/* Your existing styles here */
</style>