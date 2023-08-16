<template>
  <div>
    <v-btn icon @click="showRegistrationDialog = true">
      <v-icon>mdi-account-outline</v-icon>
    </v-btn>
    <v-dialog v-model="showRegistrationDialog" max-width="500" @click:outside="closeDialog" class="register-dialog">
      <v-card>
        <v-card-title class="register-title">
          <span class="white--text">REGISTER TO BE READY!</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="registerUser">
            <v-text-field v-model="registrationData.username" label="Select a username!" required></v-text-field>
            <v-text-field v-model="registrationData.password" label="It's time to choose a password." type="password" required></v-text-field>
            <v-text-field v-model="registrationData.confirm_password" label="Let's check, do you remember the password?" type="password" required></v-text-field>
            <v-text-field v-model="registrationData.email" label="And your Email" required></v-text-field>
            <v-text-field v-model="registrationData.first_name" label="First Name"></v-text-field>
            <v-text-field v-model="registrationData.last_name" label="Last Name"></v-text-field>
            <v-text-field v-model="registrationData.city" label="Which city do you live? (So that we don't tire you)"></v-text-field>
            <!-- Add other registration fields here -->
            <v-btn type="submit" class="register-button">Register</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Vuetify alert to show registration error messages -->
    <v-alert v-if="registrationErrorMessage" type="error" prominent :value="showAlert" class="registration-alert">
      {{ registrationErrorMessage }}
    </v-alert>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      showRegistrationDialog: false,
      registrationData: {
        username: "",
        password: "",
        confirm_password: "",
        email: "",
        first_name: "",
        last_name: "",
        city: "",
      },
      registrationErrorMessage: "",
      showAlert: false, // New data property to control the alert visibility
    };
  },
  watch: {
    value(newVal) {
      this.showRegistrationDialog = newVal;
    },
  },
  methods: {
    closeDialog() {
      // Emit an event to notify the parent component about the closing of the dialog
      this.$emit("input", false);
    },
    async registerUser() {
      try {
        // Clear any previous error message when attempting to register
        this.registrationErrorMessage = "";

        // Validate the registration form fields
        if (!this.registrationData.username || !this.registrationData.password || !this.registrationData.confirm_password || !this.registrationData.email) {
          this.registrationErrorMessage = "We cannot let you go if you leave any blanks behind.";
          this.showAlert = true; // Show the alert
        } else {
          // All required fields are provided, proceed with registration
          const response = await axios.post('http://127.0.0.1:8000/user/register/', this.registrationData);
          // Registration successful
          this.$emit('registerSuccess', response.data);
          this.$emit('input', false); // Close the dialog
        }

        // Set a timer to hide the alert after 3 seconds
        setTimeout(() => {
          this.showAlert = false;
        }, 3000);
      } catch (error) {
        // Registration failed, handle the error
        console.error('Registration Error:', error.response.data);
      }
    },
  },
};
</script>

<style>
.register-title {
  background-color: #333;
}

.register-button {
  background-color: #333;
  color: #ffffff; /* Set the text color to white */
}

.register-dialog {
  position: relative;
  z-index: 200; /* Set a higher z-index for the dialog */
}

.registration-alert {
  position: relative; /* Change the position to relative */
  margin-top: -20px; /* Adjust the margin-top to bring the alert in front of the dialog */
  z-index: 201; /* Set a higher z-index for the alert to appear in front of the dialog */
}
</style>
