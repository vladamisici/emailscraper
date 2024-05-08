<template>
  <!-- Container for the entire view -->
  <div class="relative">

    <!-- PrimeVue Toolbar -->
    <Toolbar class="bg-orange-500 shadow-md bg-gradient-to-r from-orange-500/70 to-orange-600/80 fixed top-0 left-0 right-0 z-10">
      <template #start>
        <!-- Logo or Icon -->
        <router-link to="/" class="flex items-center space-x-2 text-white font-bold hover:text-orange-300">
          <img :src="fetchyLogo" alt="Fetchy Logo" class="h-8 w-8">
          <span>FETCHY.CC</span>
        </router-link>
      </template>
      <template #end>
        <!-- Navigation Links -->
        <div class="flex items-center gap-3">
          <router-link to="/pricing" class="text-white hover:bg-orange-700 px-3 py-2 rounded-md">Pricing</router-link>
          <router-link to="/about" class="text-white hover:bg-orange-700 px-3 py-2 rounded-md">About Us</router-link>
          <router-link to="/login" class="text-white hover:bg-orange-700 px-3 py-2 rounded-md">Log in</router-link>
          <router-link to="/signup" class="bg-white text-orange-700 hover:bg-gray-100 px-4 py-2 rounded-md">Sign Up</router-link>
        </div>
      </template>
    </Toolbar>

    <!-- Centered Panel for Content -->
    <div class="relative flex items-center justify-center min-h-screen px-4 pt-24 md:pt-32">
      <div class="max-w-lg p-8 bg-white rounded-lg shadow-lg text-center space-y-4">
        <img :src="fetchyLogo" alt="Fetchy Logo" class="h-16 md:h-24 lg:h-32 mx-auto">
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-orange-800">FETCHY.CC</h1>
        <p class="text-md md:text-lg text-gray-700">
          Streamline your email management with our cutting-edge email scraper service. Fetchy.cc offers unparalleled precision, transforming email chaos into organized bliss.
        </p>
        <button @click="viewDemo" class="bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-6 rounded-lg shadow">
          View Demo
        </button>
      </div>
    </div>

    <!-- Video Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center z-30">
      <div class="bg-white p-4 rounded-lg shadow-xl" @click.stop>
        <div class="flex justify-end">
          <button @click="toggleModal" class="text-gray-600 hover:text-gray-900">
            <span class="text-2xl">&times;</span>
          </button>
        </div>
        <iframe
          width="560"
          height="315"
          :src="videoSrc"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import fetchyLogo from '/src/assets/styles/images/fetchylogo.png';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
</script>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      isModalOpen: false,
      videoSrc: 'https://www.youtube.com/embed/L_LUpnjgPso', // Set your video embed URL here
    };
  },
  methods: {
    toggleModal() {
      this.isModalOpen = !this.isModalOpen;
      if (!this.isModalOpen) {
        this.videoSrc += ''; // This triggers the iframe to reload and therefore stop the video
      }
    },
    viewDemo() {
      this.toggleModal(); // When 'View Demo' is clicked, open the modal
    },
  },
};
</script>

<style scoped>
/* Ensure the menu bar is not hidden behind the browser's toolbar */
nav {
  position: fixed;
  width: 100%;
  top: 0;
}

/* Add padding to the top of the container to account for the fixed navbar */
.min-h-screen {
  padding-top: 5rem; /* Adjust this value based on the height of your navbar */
}
</style>
