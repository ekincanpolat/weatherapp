<template>
  <div>
    <v-btn icon @click="showLoginDialog = true">
      <v-icon>mdi-login</v-icon>
    </v-btn>
    <v-dialog v-model="showLoginDialog" max-width="500" @click:outside="closeDialog" class="login-dialog">
      <v-card>
        <v-card-title class="login-title">
          <span class="white--text">LET'S LOGIN!</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="login">
            <v-text-field v-model="loginData.username_or_email" label="Username or Email- whatever you remember!"></v-text-field>
            <v-text-field v-model="loginData.password" label="Password-we hope that you remember!" type="password"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn type="submit" class="login-button" @click="login">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Vuetify alert to show login error messages -->
    <v-alert v-if="loginErrorMessage" type="error" prominent :value="showAlert" class="login-alert">
      {{ loginErrorMessage }}
    </v-alert>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showLoginDialog: false,
      loginData: {
        username_or_email: "",
        password: "",
      },
      loginErrorMessage: "",
      showAlert: false, // New data property to control the alert visibility
      isLoggedIn:null
    };
  },
  methods: {
    closeDialog() {
      this.$emit("input", false);
    },
    async login() {
      try {
        this.loginErrorMessage = "";

        // Validate the login form fields
        if (!this.loginData.username_or_email) {
          this.loginErrorMessage = "You forgot to write your username.";
          this.showAlert = true; // Show the alert
        } else if (!this.loginData.password) {
          this.loginErrorMessage = "You forgot to write your password.";
          this.showAlert = true; // Show the alert
        } else {
          // Both username/email and password are provided, proceed with login
          const response = await axios.post('http://127.0.0.1:8000/user/login/', this.loginData);

          this.$emit('loginSuccess', response.data);
          this.$emit('input', false);
          localStorage.setItem('token', response.data.token);
        }

        // Set a timer to hide the alert after 3 seconds
        setTimeout(() => {
          this.showAlert = false;
        }, 3000);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Handle incorrect password case
          this.loginErrorMessage = "We both know that this is not your password.";
          this.showAlert = true; // Show the alert

          // Set a timer to hide the alert after 3 seconds
          setTimeout(() => {
            this.showAlert = false;
          }, 3000);
        } else {
          console.error('Login Error:', error.response.data);
        }
      }
    },
  },
};
</script>


<style>
.login-title {
  background-color: #333;
}

.login-button {
  background-color: #333;
}

.login-dialog {
  position: relative;
  z-index: 200; /* Set a higher z-index for the dialog */
}

.login-alert {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  z-index: 201; /* Set a higher z-index for the alert to appear above the dialog */
}
</style>
