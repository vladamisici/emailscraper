<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <div class="absolute top-5 left-5">
      <button @click="goBack" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-full">
        <img src='C:\emailscraper\frontend\src\assets\styles\Icons\back-arrow.svg' alt="back" class="w-4 h-4" />
      </button>
    </div>
    <div class="flex-grow flex flex-col items-center justify-center">
      <div class="flex justify-center items-center space-x-10 md:space-x-20">
        <div class="flex flex-col items-center">
          <div class="w-32 h-32 bg-gray-300 rounded-full overflow-hidden">
            <div class="h-full w-full bg-cover bg-center" style="background-image: url('src/assets/styles/images/Vlada.JPG');"></div>
          </div>
          <h3 class="mt-4 text-lg font-medium text-gray-900">Misici Vlada</h3>
          <p class="text-sm text-orange-500">Front-end</p>
          <p class="text-center text-gray-500">Responsible for designing and implementing the user interface, ensuring responsiveness and seamless user experience.</p>
          <a href="https://www.linkedin.com" class="text-blue-500">LinkedIn</a>
          <p class="text-xs text-gray-600">vlada.misici02@e-uvt.ro</p>
        </div>

        <div class="flex flex-col items-center">
          <div class="w-32 h-32 bg-gray-300 rounded-full overflow-hidden">
            <div class="h-full w-full bg-cover bg-center" style="background-image: url('src/assets/styles/images/Andi.jpeg');"></div>
          </div>
          <h3 class="mt-4 text-lg font-medium text-gray-900">Andy Dobre</h3>
          <p class="text-sm text-orange-500">Back-end</p>
          <p class="text-center text-gray-500">Focuses on server-side logic, database management, and integration with front-end technologies.</p>
          <a href="https://www.linkedin.com" class="text-blue-500">LinkedIn</a>
          <p class="text-xs text-gray-600">andy.dobre02@e-uvt.ro</p>
        </div>

        <div class="flex flex-col items-center">
          <div class="w-32 h-32 bg-gray-300 rounded-full overflow-hidden">
            <div class="h-full w-full bg-cover bg-center" style="background-image: url('src/assets/styles/images/Paul.jpg');"></div>
          </div>
          <h3 class="mt-4 text-lg font-medium text-gray-900">Paul Babiciu</h3>
          <p class="text-sm text-orange-500">Database</p>
          <p class="text-center text-gray-500">Specializes in database architecture, ensuring data integrity, performance, and scalability.</p>
          <a href="https://www.linkedin.com" class="text-blue-500">LinkedIn</a>
          <p class="text-xs text-gray-600">paul.babiciu02@e-uvt.ro</p>
        </div>
      </div>
    </div>
    <div class="w-full px-4 py-4 bg-gray-100">
      <div class="max-w-sm mx-auto">
        <button class="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-4 rounded-full transition-colors">
          Contact Us
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutUs',
  methods: {
    goBack() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
/* Additional styles if needed */
</style>
