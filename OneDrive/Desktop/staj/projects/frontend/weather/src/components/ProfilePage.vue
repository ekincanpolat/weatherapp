<template>
  <div class="profile-container">
    <NavigationBar v-if="loggedIn" />
    <v-col cols="12" sm="6">
      <div class="text-container">
        <h2>{{ userProfile.username }}'s Profile</h2>
        <hr class="divider" />
        <p><strong>Username:</strong> {{ userProfile.username }}</p>
        <p><strong>Email:</strong> {{ userProfile.email }}</p>
        <p><strong>First Name:</strong> {{ userProfile.first_name }}</p>
        <p><strong>Last Name:</strong> {{ userProfile.last_name }}</p>
        <p><strong>City:</strong> {{ userProfile.city }}</p>

        <!-- Add a button to trigger the file input dialog -->
        <v-btn @click="openFileInput">Upload Avatar</v-btn>

      <v-btn v-if="loggedIn" @click="handleEdit">Edit Profile</v-btn>
      </div>
    </v-col>
  </div>
</template>

<script>
import NavigationBar from "@/components/NavigationBar";
import axios from "axios";

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      loggedIn: false,
      userProfile: {},
    };
  },
  async created() {
    this.loggedIn = !!localStorage.getItem("token");
    if (this.loggedIn) {
      await this.fetchUserProfile();
    }
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/user/profile/",
          null,
          {
            headers: {
              Authorization: "Token " + localStorage.getItem("token"),
            },
          }
        );
        this.userProfile = response.data.user; // Update the userProfile data
        console.log("userProfile:", this.userProfile); // Add this line to check the content
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    },


    handleEdit(){
      this.$router.push("/edit-profile");

    },
  },
};
</script>

<style>
.profile-container {
  display: flex;
  justify-content: center; /* Center the container horizontally */
  align-items: center; /* Center the container vertically */
  min-height: 100vh; /* Set a minimum height to occupy the full viewport */
}

.text-container {
  padding: 100px 150px; /* Add padding to create space between text and the container edges */
  border-radius: 8px; /* Add rounded corners to the container */
  box-shadow: 0 20px 20px rgba(0, 0, 0, 0.1); /* Add a subtle shadow effect */
  background-color: #f5f5f5; /* Set the background color */
  max-width: 800px; /* Set the maximum width for the container */
  margin-top: 80px;
}

h2 {
  margin-bottom: 20px; /* Add space between the h2 and the next element */
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin: 10px 0;
}
</style>
