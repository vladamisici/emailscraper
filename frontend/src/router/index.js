import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AboutUsPage from '../views/AboutUsPage.vue'
import ScrapePage from '../views/ScrapePage.vue'

const routes = [
    {
        path: '/',
        name: 'Landing',
        component: LandingPage
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/about',
        name: 'AboutUs',
        component: AboutUsPage
    },
    {
        path: '/scrape',
        name: 'Scrape',
        component: ScrapePage
    },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
