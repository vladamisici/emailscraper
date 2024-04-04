<template>
    <!-- Container for the entire view -->
    <div class="relative bg-no-repeat bg-cover bg-fixed" style="background-image: url('/src/assets/styles/images/fetchybackground.png');">
      
    <!-- Menu Bar -->
    <nav class="bg-orange-500 text-white fixed w-full z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-3 md:space-x-10">
          <router-link to="/" class="text-3xl font-bold hover:text-orange-300">
            FETCHY.CC
          </router-link>
          <div class="hidden md:flex space-x-8">
            <router-link to="/pricing" class="text-base font-medium hover:text-orange-300">
              Pricing
            </router-link>
            <router-link to="/about" class="text-base font-medium hover:text-orange-300">
              About Us
            </router-link>
            <router-link to="/login" class="text-base font-medium hover:text-orange-300">
              Log in
            </router-link>
            <router-link
              to="/signup"
              class="text-base font-medium text-orange-700 bg-white hover:bg-gray-100 px-4 py-2 rounded-md shadow-sm transition duration-150 ease-in-out"
            >
              Sign Up
            </router-link>
          </div>
        </div>
      </div>
    </nav>
      
      <!-- Centered Panel for Content over the background -->
      <div class="relative flex items-center justify-center min-h-screen px-4 pt-16 md:pt-24">
        <div class="max-w-lg p-8 bg-[#FEF7EE] bg-opacity-100 rounded-lg shadow-lg text-center space-y-4">
          <!-- Content elements here: image, title, description, and button -->
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
                <!-- Close button -->
                <button @click="toggleModal" class="text-gray-600 hover:text-gray-900">
                <span class="text-2xl">&times;</span>
                </button>
            </div>
            <!-- Assuming you're using a YouTube video, replace `videoSrc` with your video link -->
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
      padding-top: 4rem; /* Adjust this value based on the height of your navbar */
    }
  </style>
  