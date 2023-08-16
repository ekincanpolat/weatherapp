<template>
  <div>
      <v-main>
      <v-container>
      <NavigationBar :isLoggedIn="isLoggedIn" />
        <h2>It's time to choose !</h2>
        <v-row>
          <v-col cols="12">
            <v-label for="city">City:</v-label>
            <v-text-field v-model="city" @input="debounceSearchCitiesHandler"></v-text-field>
          </v-col>
          <v-col cols="12" v-if="suggestedCities.length > 0">
            <ul>
              <li v-for="suggestedCity in suggestedCities" :key="suggestedCity">
                <v-btn @click="selectCity(suggestedCity)">{{ suggestedCity }}</v-btn>
              </li>
            </ul>
          </v-col>
        </v-row>
        <v-row>
      <v-col cols="12">
        <v-label for="start">Start Date:</v-label>
        <v-menu
          v-model="menuStartDate"
          :close-on-content-click="false"
          :return-value="selectedStartDate"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="selectedStartDate"
              label="Start Date"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="selectedStartDate"
            no-title
            scrollable
          >
            <v-spacer></v-spacer>
            <v-btn
              text
              color="primary"
              @click="menuStartDate = false"
            >
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="saveStartDate"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </v-col>
    </v-row>

        <v-row>
          <v-col cols="12">
        <v-label for="end">End Date:</v-label>
        <v-menu
          v-model="menuEndDate"
          :close-on-content-click="false"
          :return-value="selectedEndDate"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="selectedEndDate"
              label="End Date"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="selectedEndDate"
            no-title
            scrollable
          >
            <v-spacer></v-spacer>
            <v-btn
              text
              color="primary"
              @click="menuEndDate = false"
            >
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="saveEndDate"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </v-col>
    </v-row>
        <v-row>
      <v-col cols="12">
        <v-btn @click="getWeather">Get Weather</v-btn>
      </v-col>
    </v-row>
        <v-row v-if="weatherData">
      <v-col cols="12">
        <h2>{{ weatherData.city }}</h2>
        <ul>
          <li v-for="weather in weatherData.weatherList" :key="weather.date">
            <span>{{ weather.date }}</span> - <span>{{ weather.temperature }}°C</span>
          </li>
        </ul>
      </v-col>
    </v-row>
        <v-row v-if="error">
      <v-col cols="12">
        <div>{{ error }}</div>
      </v-col>
    </v-row>
      </v-container>
      </v-main>



  </div>
</template>

<script>
import axios from "axios";
import { debounce } from "lodash";
import NavigationBar from "@/components/NavigationBar.vue";

export default {
  name: "UserPage",
  components:{
    NavigationBar,
  },

  data() {
    const today = new Date();
    const endDate = new Date();
    endDate.setDate(today.getDate() + 5);


    return {
      city: "",
      startDate: today.toISOString().split("T")[0],
      endDate: endDate.toISOString().split("T")[0],
      weatherData: null,
      error: "",
      suggestedCities: [],
      menuStartDate: false,
      menuEndDate: false,
      selectedStartDate: today.toISOString().split("T")[0],
      selectedEndDate: endDate.toISOString().split("T")[0],
    };
  },

  methods: {
    debounceSearchCitiesHandler: debounce(function () {
      const city = this.city.trim();
      if (city.length < 3) {
        this.suggestedCities = [];
        return;
      }
      this.searchCities(city);
    }, 200),

    searchCities(city) {
      const apiUrl = `http://127.0.0.1:8000/api/city/`;
      axios
        .post(apiUrl, { city })
        .then((response) => {
          this.suggestedCities = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    selectCity(selectedCity) {
      this.city = selectedCity;
      this.suggestedCities = [];
    },

    getWeather() {
      if (this.city.trim() === "") {
        this.error = "City name is required.";
        return;
      }
      this.error = "";

      const apiUrl = "http://127.0.0.1:8000/api/weather/";
      const requestData = {
        city: this.city,
        start_date: this.selectedStartDate,
        end_date: this.selectedEndDate,
      };

      axios
        .post(apiUrl, requestData)
        .then((response) => {
          this.weatherData = {
            city: this.city,
            weatherList: response.data,
          };
        })
        .catch((error) => {
          this.error = "Failed to fetch weather data.";
          console.error(error);
        });
    },

    saveStartDate() {
      this.startDate = this.selectedStartDate;
      this.menuStartDate = false;
    },

    saveEndDate() {
      this.endDate = this.selectedEndDate;
      this.menuEndDate = false;
    },


  },
};
</script>
