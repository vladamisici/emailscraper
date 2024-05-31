<template>
  <div class="app-container h-full flex overflow-hidden">
    <Sidebar 
      :loggedInEmail="loggedInEmail" 
      @setCategory="setCategory" 
      :category="category" 
      :labels="labels"  
      @setLabel="setLabel"
    />
    <main class="main-content flex-1 overflow-auto p-4">
      <Header :filterText="filterText" @update:filterText="filterText = $event" @clearFilter="clearFilter" @refreshEmails="refreshEmails" />
      <section class="email-section">
        <div class="section-header">
          <h2 class="section-title">{{ categoryHeader }}</h2>
          <button v-if="isLabelCategory" @click="editLabel">Edit label</button>
        </div>
        <EmailTable :emails="filteredEmails" :category="category" :isLoading="isLoading" @openEmail="openEmail" />
      </section>
    </main>
    <EmailDialog :email="selectedEmail" :visible="emailDialogVisible" @update:visible="emailDialogVisible = $event" />
    <EditLabelDialog :visible="editLabelDialogVisible" :label="selectedLabel" @update:visible="editLabelDialogVisible = $event" @saveLabelCriteria="saveLabelCriteria" />
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
import axios from 'axios';

const route = useRoute();
const email_addr = ('');
const loggedInEmail = ref(email_addr || 'user@example.com');
const isLoading = ref(true);

const fetchEmailAddr = async () => {
  try{
    const response = axios.get('https://localhost:5000/authentication/get_email', {withCredentials: true});
    if(response.status === 200 && response.data.email){
      email_addr = response.data.email;
    }
    else{
      console.error('Failed to fetch email', response.data);
    }
  }
  catch(error){
    console.error('Error', error);
  }
};

const pageSize = ref(10);
const filterText = ref('');
const emailDialogVisible = ref(false);
const editLabelDialogVisible = ref(false);
const selectedEmail = ref({});
const category = ref('inbox');
const labels = ref([
  { name: 'Work', criteria: email => email.from.endsWith('@organization.com') },
  { name: 'Personal', criteria: email => email.from.endsWith('@gmail.com') },
  // Add more labels as needed
]);
const selectedLabel = ref(null);

const emails = ref([]); 

// const setCategory = (newCategory) => {
//   category.value = newCategory;
//   selectedLabel.value = null;
// };

const setCategory = async (newCategory) => {
  category.value = newCategory;
  selectedLabel.value = null;
  isLoading.value = true;
  try {
    switch (newCategory) {
      case 'inbox':
        await fetchInboxEmails();
        break;
      case 'sent':
        await fetchSentEmails();
        break;
      case 'drafts':
        await fetchDrafts();
        break;
      case 'archive':
        await fetchArchivedEmails();
        break;
      default:
        break;
    }
  } finally {
    isLoading.value = false;
  }
};



const fetchEmails = async () => {
  const cancelTokenSource = axios.CancelToken.source();

  try {
    let response;
    switch (category.value) {
      case 'inbox':
        response = await axios.get('https://localhost:5000/mail/inbox', {
          withCredentials: true,
          cancelToken: cancelTokenSource.token,
        });
        break;
      case 'sent':
        response = await axios.get('https://localhost:5000/mail/sent', {
          withCredentials: true,
          cancelToken: cancelTokenSource.token,
        });
        break;
      case 'drafts':
        response = await axios.get('https://localhost:5000/mail/drafts', {
          withCredentials: true,
          cancelToken: cancelTokenSource.token,
        });
        break;
      case 'archive':
        response = await axios.get('https://localhost:5000/mail/archive', {
          withCredentials: true,
          cancelToken: cancelTokenSource.token,
        });
        break;
      default:
        break;
    }

    if (response && response.status === 200) {
      emails.value = response.data;
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
    cancelTokenSource.cancel('Request cancelled by user');
    isLoading.value = false;
  }
};

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
    case 'archive': return 'Archived Emails';
    default: return '';
  }
});

const isLabelCategory = computed(() => selectedLabel.value !== null);

const filteredEmails = computed(() => {
  let filtered = emails.value;
  if (filterText.value) {
    filtered = filtered.filter(email => email.subject.includes(filterText.value) || email.content.includes(filterText.value));
  }
  if (selectedLabel.value) {
    filtered = filtered.filter(selectedLabel.value.criteria);
  }
  return filtered;
});

const clearFilter = () => {
  filterText.value = '';
};


// const fetchInboxEmails = async () => {
//   try {
//     const response = await axios.get('https://localhost:5000/mail/inbox', {withCredentials: true});
//     // const response = await axios.get('https://jsonplaceholder.typicode.com/todos/1')
//     if (response.status === 200) {
//       emails.value = response.data;
//     } else {
//       console.error('Failed to fetch emails:', response.data);
//     }
//   } catch (error) {
//     console.error('Error fetching emails:', error);
//   } finally {
//     isLoading.value = false;
//   }
// };

// const fetchSentEmails = async () => {
//   try {
//     const response = await axios.get('https://localhost:5000/mail/sent', {withCredentials: true});
//     // const response = await axios.get('https://jsonplaceholder.typicode.com/todos/1')
//     if (response.status === 200) {
//       emails.value = response.data;
//     } else {
//       console.error('Failed to fetch emails:', response.data);
//     }
//   } catch (error) {
//     console.error('Error fetching emails:', error);
//   } finally {
//     isLoading.value = false;
//   }
// };

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

// onMounted(fetchEmails);
onMounted(() => {
  fetchEmailAddr();
  fetchEmails();
});

const refreshEmails = async () => {
  isLoading.value = true;
  try{
    await fetchEmails();
  }
  finally{
    isLoading.value = false;
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
