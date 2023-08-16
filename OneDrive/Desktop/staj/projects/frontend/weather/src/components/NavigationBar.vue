<template>
  <div id="app">
    <v-app-bar
      absolute
      color="#647698"
      dark
      shrink-on-scroll
      src="@/assets/Weather.png"
    >
      <template v-slot:img="{ props }">
        <v-img v-bind="props"></v-img>
      </template>

      <v-app-bar-nav-icon/>

      <v-app-bar-title>What's the Weather?</v-app-bar-title>

      <v-spacer></v-spacer>

      <RegisterButton
        v-if="!isLoggedIn"
        v-model="showRegistrationDialog"
        @registerSuccess="handleRegistration"
      />

      <LoginButton
        v-if="!isLoggedIn"
        v-model="showLoginDialog"
        @loginSuccess="handleLoginSuccess"
      />

      <v-btn v-if="isLoggedIn" icon @click="$router.push('/profile')">
      <v-icon>mdi-account-box-outline</v-icon>
    </v-btn>



      <v-btn v-if="isLoggedIn" icon>
        <v-icon>mdi-email</v-icon>
      </v-btn>

      <LogoutButton v-if="isLoggedIn" @logoutSuccess="handleLogout"/>

    </v-app-bar>

    <v-container style="height: 150px;"></v-container>
  </div>
</template>

<script>
import RegisterButton from './RegisterButton.vue';
import LoginButton from './LoginButton.vue';
import LogoutButton from "@/components/LogoutButton.vue";

export default {
  name: "NavigationBar",

  components: {
    LogoutButton,
    RegisterButton,
    LoginButton,
  },
  data() {
    return {
      showRegistrationDialog: false,
      showLoginDialog: false,
      isLoggedIn:false,
    };
  },
  methods: {

    handleRegistration(data) {
      console.log("Registration Data:", data);
      this.showRegistrationDialog = false;
    },
    handleLoginSuccess() {
      this.isLoggedIn = true;
      localStorage.setItem('isLoggedIn', "true");
      this.$router.push("/user");
    },
    handleLogout() {
      this.isLoggedIn = false;
      localStorage.setItem('isLoggedIn', "false");
      this.$router.push("/");
    },
    handleShowRegisterButton(value) {
      this.showRegistrationDialog = value;
    },
    handleShowLoginButton(value) {
      this.showLoginDialog = value;
    },
  },
  created() {
    this.$parent.$on("show-register-button", this.handleShowRegisterButton);
    this.$parent.$on("show-login-button", this.handleShowLoginButton);
    this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

  },
  beforeDestroy() {
    this.$parent.$off("show-register-button", this.handleShowRegisterButton);
    this.$parent.$off("show-login-button", this.handleShowLoginButton);
  },
};
</script>

<style>
</style>