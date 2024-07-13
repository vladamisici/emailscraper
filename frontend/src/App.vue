<script setup>
import Toolbar from 'primevue/toolbar';
import fetchyLogo from '/src/assets/styles/images/fetchylogo.png'; 
import { useRoute } from 'vue-router';
import { computed } from 'vue';


const route = useRoute();

const isScrapeRoute = computed(() => {
  return route.path === '/scrape';
});
</script>

<template>
  <div id="app" class="flex flex-col h-screen">
    <Toolbar v-if="!isScrapeRoute" class="bg-orange-500 shadow-md bg-gradient-to-r from-orange-500/70 to-orange-600/80 fixed top-0 left-0 right-0 z-10">
      <template #start>
        <router-link to="/" class="flex items-center space-x-2 text-white font-bold hover:text-orange-300">
          <img :src="fetchyLogo" alt="Fetchy Logo" class="h-8 w-8">
          <span>FETCHY.CC</span>
        </router-link>
      </template>
      <template #end>
        <div class="flex items-center gap-3">
          <router-link to="/pricing" class="text-white hover:bg-orange-700 px-3 py-2 rounded-md">Pricing</router-link>
          <router-link to="/about" class="text-white hover:bg-orange-700 px-3 py-2 rounded-md">About Us</router-link>
          <router-link to="/login" class="text-white hover:bg-orange-700 px-3 py-2 rounded-md">Log in</router-link>
          <!-- <router-link to="/signup" class="bg-white text-orange-700 hover:bg-gray-100 px-4 py-2 rounded-md">Sign Up</router-link> -->
        </div>
      </template>
    </Toolbar>

    <main :class="{'pt-20': !isScrapeRoute, 'p-0': isScrapeRoute}" class="flex-1 overflow-hidden">
      <router-view />
    </main>
  </div>
</template>

<style scoped>

main.pt-20 {
  padding-top: 64px;
  transition: padding-top 0.3s;
}
main.p-0 {
  padding: 0;
}
</style>