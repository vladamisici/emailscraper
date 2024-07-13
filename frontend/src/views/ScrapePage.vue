<template>
  <div class="app-container h-full flex overflow-hidden">
    <Sidebar 
      :loggedInEmail="loggedInEmail" 
      @setCategory="setCategory" 
      :category="category" 
      :labels="labels"  
      @setLabel="setLabel"
      @send-email="openEmailForm"
    />
    <main class="main-content flex-1 overflow-auto p-4">
      <Header :filterText="filterText" @update:filterText="filterText = $event" @clearFilter="clearFilter" @refreshEmails="refreshEmails" />
      <section class="email-section" v-if="!showSendEmail.value">
        <div class="section-header">
          <h2 class="section-title">{{ categoryHeader }}</h2>
          <button v-if="isLabelCategory" @click="editLabel">Edit label</button>
        </div>
        <EmailTable :emails="filteredEmails" :category="category" :isLoading="isLoading" @openEmail="openEmail" />
      </section>

      <!-- <Button label="Send Email" @click="showEmailModal = true" /> -->
      <!-- <Dialog v-model:visible="showSendEmailModal" modal header="Send Email">
        <SendEmail @close="showSendEmailModal = false" />
      </Dialog> -->
    </main>
    <EmailDialog :email="selectedEmail" :visible="emailDialogVisible" @update:visible="emailDialogVisible = $event" />
    <EditLabelDialog :visible="editLabelDialogVisible" :label="selectedLabel" @update:visible="editLabelDialogVisible = $event" @saveLabelCriteria="saveLabelCriteria" />
    <email-form v-if="showEmailForm" @close-form="closeEmailForm" :credentials="credentials" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Header from '../components/Header.vue';
import EmailTable from '../components/EmailTable.vue';
import EmailDialog from '../components/EmailDialog.vue';
import EditLabelDialog from '../components/EditLabelDialog.vue';
import Dialog from 'primevue/dialog';
import EmailForm from '../components/EmailForm.vue';
import axios from 'axios';


const showSendEmail = ref(false);
const route = useRoute();
const email_addr = ('');
const loggedInEmail = ref('');
const isLoading = ref(true);
let currentRequestCancelToken = null;

const fetchEmailAddr = async () => {
  try{
    const response = await axios.get('https://localhost:5000/authentication/get_email', {withCredentials: true});
    if(response.status === 200 && response.data.email){
      loggedInEmail.value = response.data.email;
    }
    else{
      console.error('Failed to fetch email', response.data);
    }
  }
  catch(error){
    console.error('Error', error);
  }
};

const showEmailForm = ref(false);
const credentials = ref(null);

const openEmailForm = () => {
  showEmailForm.value = true;
};

const closeEmailForm = () => {
  showEmailForm.value = false;
};

const pageSize = ref(10);
const filterText = ref('');
const emailDialogVisible = ref(false);
const editLabelDialogVisible = ref(false);
const selectedEmail = ref({});
const category = ref('inbox');
const labels = ref([
  { name: 'Work', criteria: email => email.from.endsWith('@medium.com') },
  { name: 'Personal', criteria: email => email.from.endsWith('@gmail.com') },
]);
const selectedLabel = ref(null);

const emails = ref([]); 
// const emailCache ={};
const emailCache = ref({});


const setCategory = async (newCategory) => {
  category.value = newCategory;
  selectedLabel.value = null;
  isLoading.value = true;
  
  if (currentRequestCancelToken) {
    currentRequestCancelToken.cancel('Request cancelled due to category change');
  }
  
  currentRequestCancelToken = axios.CancelToken.source();
  
  try {
    await fetchEmails(currentRequestCancelToken.token);
  } finally {
    isLoading.value = false;
  }
};


const isRefreshing = ref(false);

const fetchEmails = async (cancelToken) => {
  isLoading.value = true;

  if (emailCache.value[category.value] && !isRefreshing.value) {
    emails.value = emailCache.value[category.value];
    isLoading.value = false;
    return;
  }

  try {
    let response;
    switch (category.value) {
      case 'inbox':
        response = await axios.get('https://localhost:5000/mail/inbox', {
          withCredentials: true,
          cancelToken: cancelToken,
        });
        break;
      case 'sent':
        response = await axios.get('https://localhost:5000/mail/sent', {
          withCredentials: true,
          cancelToken: cancelToken,
        });
        break;
      case 'drafts':
        response = await axios.get('https://localhost:5000/mail/drafts', {
          withCredentials: true,
          cancelToken: cancelToken,
        });
        break;
      case 'spam':
        response = await axios.get('https://localhost:5000/mail/spam', {
          withCredentials: true,
          cancelToken: cancelToken,
        });
        break;
      default:
        break;
    }

    if (response && response.status === 200) {
      if (response.data.message) {
        emails.value = [];
      } else {
        emails.value = response.data;
        emailCache.value[category.value] = response.data;
      }
    } else {
      console.error('Failed to fetch emails:', response);
    }
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request cancelled:', error.message);
    } else {
      console.error('Error fetching emails:', error);
    }
  } finally {
    isLoading.value = false;
    isRefreshing.value = false;
  }
};


// const toggleSendEmail = () => {
//   showSendEmail.value = !showSendEmail.value;
// };

const setLabel = (label) => {
  selectedLabel.value = label;
  category.value = `label:${label.name}`;
};

const categoryHeader = computed(() => {
  if (selectedLabel.value) {
    return `Label: ${selectedLabel.value.name}`;
  }
  switch (category.value) {
    case 'inbox': return 'Inbox Emails';
    case 'sent': return 'Sent Emails';
    case 'drafts': return 'Drafts';
    case 'spam': return 'Spam Emails';
    default: return '';
  }
});

const isLabelCategory = computed(() => selectedLabel.value !== null);

const filteredEmails = computed(() => {
  let filtered = emails.value || [];
  if (filterText.value) {
    filtered = filtered.filter(email => 
      (email.subject?.toLowerCase().includes(filterText.value.toLowerCase()) || 
       email.content?.toLowerCase().includes(filterText.value.toLowerCase())) ?? false
    );
  }
  if (selectedLabel.value) {
    filtered = filtered.filter(email => selectedLabel.value.criteria(email));
  }
  return filtered;
});

const clearFilter = () => {
  filterText.value = '';
};



const openEmail = (email) => {
  selectedEmail.value = email;
  emailDialogVisible.value = true;
};

const editLabel = () => {
  editLabelDialogVisible.value = true;
};

const saveLabelCriteria = (label, newCriteria) => {
  label.criteria = newCriteria;
  editLabelDialogVisible.value = false;
};

onMounted(async () => {
  fetchEmailAddr();
  fetchEmails();
});

const clearCacheForCategory = () => {
  delete emailCache[category.value];
};

const refreshEmails = async () => {
  isLoading.value = true;
  isRefreshing.value = true;
  try {
    delete emailCache.value[category.value];
    await fetchEmails();
  } finally {
    isLoading.value = false;
    isRefreshing.value = false;
  }
};
</script>
<style scoped>
.app-container {
  height: 100%;
  display: flex;
  background-color: #f0f2f5;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.email-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.5rem;
}

button {
  padding: 5px 10px;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
