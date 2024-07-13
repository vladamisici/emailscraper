<template>
  <div class="email-analysis">
    <div v-if="loading" class="loading-overlay">
      <ProgressSpinner />
      <p>Analyzing your emails...</p>
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else class="charts-container">
      <div class="chart">
        <h2>Emails by Day of Week</h2>
        <Bar :data="weekdayChartData" :options="weekdayChartOptions" />
      </div>
      <div class="chart">
        <h2>Emails by Hour of Day</h2>
        <Bar :data="hourlyChartData" :options="hourlyChartOptions" />
      </div>
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
const weekdayChartData = ref(null);
const hourlyChartData = ref(null);

const weekdayChartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Email Distribution by Day of Week' }
  },
  scales: {
    y: { beginAtZero: true, title: { display: true, text: 'Number of Emails' } }
  }
};

const hourlyChartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Email Distribution by Hour of Day' }
  },
  scales: {
    y: { beginAtZero: true, title: { display: true, text: 'Number of Emails' } },
    x: { title: { display: true, text: 'Hour of Day' } }
  }
};

const fetchAnalysisData = async () => {
  try {
    const response = await axios.get('https://localhost:5000/mail/analysis', { withCredentials: true });
    const data = response.data;

    weekdayChartData.value = {
      labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      datasets: [{
        data: data.weekdayData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      }]
    };

    hourlyChartData.value = {
      labels: Array.from({length: 24}, (_, i) => i),
      datasets: [{
        data: data.hourlyData,
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      }]
    };

    loading.value = false;
  } catch (err) {
    console.error('Error fetching analysis data:', err);
    error.value = 'Failed to load analysis data. Please try again.';
    loading.value = false;
  }
};

onMounted(fetchAnalysisData);
</script>

<style scoped>
.email-analysis {
  position: relative;
  min-height: 400px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.charts-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.chart {
  width: 100%;
  max-width: 500px;
  margin-bottom: 20px;
}

.error-message {
  color: red;
  text-align: center;
  padding: 20px;
}
</style>