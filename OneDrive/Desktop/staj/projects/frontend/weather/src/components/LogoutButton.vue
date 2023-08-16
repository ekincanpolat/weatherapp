<template>
  <v-btn icon @click="logout">
    <v-icon>mdi-logout</v-icon>
  </v-btn>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async logout() {
      try {

        await axios.post('http://127.0.0.1:8000/user/logout/', null, {
          headers: {
            Authorization: `Token ` + localStorage.getItem('token'),

          },
        });

        this.$emit('logoutSuccess');
      } catch (error) {
        console.error('Logout Error:', error.response.data);
      }
    },
  },
};
</script>

<style>
/* Your styles here */
</style>
