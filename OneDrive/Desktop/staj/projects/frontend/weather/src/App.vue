<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Vue from "vue";
import VueRouter from "vue-router";
import IndexVue from "@/components/IndexVue.vue";
import UserPage from "@/components/UserPage.vue";
import ProfilePage from "@/components/ProfilePage.vue";
import EditProfilePage from "@/components/EditProfilePage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: IndexVue,
    name: "index",
  },
  {
    path: "/user",
    component: UserPage,
    name: "user",
  },
  {
    path:"/profile",
    component: ProfilePage,
    name:"profile",
  },

  {
    path: "/edit-profile",
    name: "edit-profile",
    component: EditProfilePage,
  },
];


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default {
  name: "App",
  components: {},
  data() {
    return {
      // isLoggedIn: false,
    };
  },
  methods: {
  },
  router,
};
</script>
