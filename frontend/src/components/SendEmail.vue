<template>
    <div class="modal" @click.self="closeModal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h1>Send Email</h1>
        <form @submit.prevent="sendEmail">
          <label for="toEmail">To:</label>
          <input type="email" v-model="emailData.toEmail" required><br><br>
          
          <label for="subject">Subject:</label>
          <input type="text" v-model="emailData.subject" required><br><br>
          
          <label for="messageContent">Message:</label><br>
          <textarea v-model="emailData.messageContent" rows="4" cols="50" required></textarea><br><br>
          
          <label for="scheduleTime">Schedule Time (optional):</label>
          <input type="datetime-local" v-model="emailData.scheduleTime"><br><br>
          
          <button class="nav-button" type="submit">Send Email</button>
        </form>
        <button @click="$emit('close')">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  import Button from 'primevue/button';
  export default {
    data() {
      return {
        emailData: {
          toEmail: '',
          subject: '',
          messageContent: '',
          scheduleTime: ''
        }
      };
    },
    methods: {
      closeModal(){
        this.$emit('close');
      },
      sendEmail() {
        if (this.emailData.scheduleTime) {
          const scheduleTime = new Date(this.emailData.scheduleTime);
          this.emailData.scheduleTime = scheduleTime.toISOString();
        }
        
        fetch('https://localhost:5000/mail/send_email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify(this.emailData)
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          alert(data.success ? 'Email sent successfully!' : 'Failed to send email!');
        })
        .catch(error => {
          console.error('Error sending email:', error);
          alert('An error occurred while sending email.');
        });
      }
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
  
  /* button {
    padding: 5px 10px;
    font-size: 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  } */
  
  button:hover {
    background-color: #0056b3;
  }
  .nav-button {
    width: 100%;
    text-align: left;
    font-size: 1rem;
    padding: 10px 20px;
    background-color: transparent;
    border: 1px solid #ff5733;
    color: #ff5733;
    border-radius: 4px;
    transition: background-color 0.3s, color 0.3s;
  }
  </style>
  