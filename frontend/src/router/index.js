import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AboutUsPage from '../views/AboutUsPage.vue'
import ScrapePage from '../views/ScrapePage.vue'
import PricingPage from '../views/PricingPage.vue'
import SignUpPage from '../views/SignUpPage.vue'

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
    // {
    //     path: '/scrape/inbox',
    //     name: 'Inbox',
    //     component: InboxEmailTable
    //   },
    //   {
    //     path: '/scrape/sent',
    //     name: 'Sent',
    //     component: SentEmailTable
    //   },
    //   {
    //     path: '/scrape/draft',
    //     name: 'Drafts',
    //     component: DraftEmailTable
    //   },
    //   {
    //     path: '/scrape/archive',
    //     name: 'Archive',
    //     component: ArchiveEmailTable
    //   },
    {
        path: '/pricing',
        name: 'Pricing',
        component: PricingPage
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUpPage
    },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router