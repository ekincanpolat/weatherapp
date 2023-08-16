<template>
  <div class="edit-profile-dialog">
    <NavigationBar />
    <v-col cols="12" sm="6">
      <div class="text-container">
        <h2>Edit Profile</h2>
        <!-- Create a form to edit the profile data -->
        <v-form @submit.prevent="updateProfile">
          <v-text-field
            v-model="userProfile.username"
            label="Username"
            required
          ></v-text-field>
          <v-text-field
            v-model="userProfile.first_name"
            label="First Name"
            required
          ></v-text-field>
          <v-text-field
            v-model="userProfile.last_name"
            label="Last Name"
            required
          ></v-text-field>
          <v-text-field v-model="userProfile.email" label="Email" required></v-text-field>
          <v-text-field v-model="userProfile.city" label="City" required></v-text-field>

          <v-btn @click="cancelEdit">Cancel</v-btn>
          <v-btn type="submit">Save Changes</v-btn>
        </v-form>
      </div>
    </v-col>
  </div>
</template>

<script>
import axios from "axios";
import NavigationBar from "@/components/NavigationBar.vue";

export default {
  components: { NavigationBar },
  data() {
    return {
      userProfile: {},
    };
  },
  methods: {
    fetchUserProfile() {
      axios
        .post("http://127.0.0.1:8000/user/profile/", null, {
          headers: {
            Authorization: "Token " + localStorage.getItem("token"),
          },
        })
        .then((response) => {
          this.userProfile = response.data.user;
        })
        .catch((error) => {
          console.error("Error fetching user profile:", error);
        });
    },
    updateProfile() {
      axios
        .post("http://127.0.0.1:8000/user/profile/", this.userProfile, {
          headers: {
            Authorization: "Token " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          console.log("Profile updated successfully");
          this.$emit("close"); // Close the dialog after updating the profile
        })
        .catch((error) => {
          console.error("Error updating user profile:", error);
        });
    },
    cancelEdit() {
      this.$emit("close"); // Close the dialog without saving changes
    },
  },
  created() {
    this.fetchUserProfile();
  },
};
</script>

<style>
.edit-profile-dialog {
  display: flex;
  justify-content: center; /* Center the container horizontally */
  align-items: center; /* Center the container vertically */
  min-height: 140vh; /* Set a minimum height to occupy the full viewport */
}
.text-container {
  padding: 100px 150px; /* Add padding to create space between text and the container edges */
  border-radius: 8px; /* Add rounded corners to the container */
  box-shadow: 0 20px 20px rgba(0, 0, 0, 0.1); /* Add a subtle shadow effect */
  background-color: #f5f5f5; /* Set the background color */
  max-width: 800px; /* Set the maximum width for the container */
  margin-top: 80px;
}
</style>
