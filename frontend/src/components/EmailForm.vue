<template>
    <div class="email-form">
      <h2>Send Email</h2>
      <button class="close-button" @click="$emit('close-form')">X</button>
      <form @submit.prevent="sendEmail">
        <label for="toEmail">To:</label>
        <input type="email" id="toEmail" v-model="toEmail" required>
  
        <label for="subject">Subject:</label>
        <input type="text" id="subject" v-model="subject" required>
  
        <label for="messageContent">Message:</label>
        <textarea id="messageContent" v-model="messageContent" required></textarea>
  
        <label for="scheduleTime">Schedule Time (optional):</label>
        <input type="datetime-local" id="scheduleTime" v-model="scheduleTime">
  
        <button class="send-button" type="submit">Send</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    emits:['send-email', 'close-form'],
    data() {
      return {
        toEmail: '',
        subject: '',
        messageContent: '',
        scheduleTime: ''
      };
    },
    methods: {
        async sendEmail() {
  try {
    let scheduleTimeISO = null;
    if (this.scheduleTime) {
      scheduleTimeISO = new Date(this.scheduleTime).toISOString();
    }
    const response = await axios.post('https://localhost:5000/mail/send_email', {
      toEmail: this.toEmail,
      subject: this.subject,
      messageContent: this.messageContent,
      scheduleTime: scheduleTimeISO
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });

    if (response.status === 200) {
      console.log('Email sent successfully:', response.data);
      
      this.toEmail = '';
      this.subject = '';
      this.messageContent = '';
      this.scheduleTime = '';
    } else {
      console.error('Error sending email:', response.statusText);
    }
  } catch (error) {
    console.error('Error sending email:', error);
  }
}

    }
  };
  </script>

  
<style scoped>
.send-email-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.send-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>