<template>
  <div class="container">
    <NavigationBar />
    <div class="headline-lg-container">
      <h1 class="headline-lg">
        So, what do you plan for today?
      </h1>
    </div>

    <div class="headline">
      <div class="icon-container">
        <div class="icon-description">
          <span class="icon icon-large">
            <i class="fas fa-book"></i>
          </span>
          <p class="background-text">
            Staying home and reading, maybe? If this is your plan, you might enjoy the rain or sun, let's set your mood up!
          </p>
        </div>
        <div class="icon-description">
          <span class="icon icon-large">
            <i class="fas fa-coffee"></i>
          </span>
          <p class="background-text">
            Going out with some friends and family? Without proper clothing, you might regret your decision.
          </p>
        </div>
        <div class="icon-description">
          <span class="icon icon-large">
            <i class="fas fa-running"></i>
          </span>
          <p class="background-text">
            You woke up today and said "It's a great day for a walk or maybe jog." But, is it?
          </p>
        </div>
      </div>
      <hr class="divider" />

      <h2 class="headline-md">
        But, do you know how is the weather?
      </h2>
      <hr class="divider" />

      <div class="weather-descriptions">
        <div class="icon-description">
          <span class="icon icon-large">
            <i class="fas fa-sun"></i>
          </span>
          <p class="background-text">
            On a sunny day, skies so blue,
            Golden rays, shining through.
            Nature smiles, warm and bright,
            Joyful moments, hearts alight.
          </p>
        </div>
        <div class="icon-description">
          <span class="icon icon-large">
            <i class="fas fa-cloud"></i>
          </span>
          <p class="background-text">
            Cloudy day, sky of gray,
            Whispers soft, rain's on its way.
            Clouds gather, blocking light,
            Nature's charm, in muted sight.
          </p>
        </div>
        <div class="icon-description">
          <span class="icon icon-large">
            <i class="fas fa-umbrella"></i>
          </span>
          <p class="background-text">
            Rainy day, come and play,
            Pitter-patter, throughout the day.
            Umbrellas up, rain boots on,
            Splashing joy, we'll carry on.
          </p>
        </div>
      </div>

      <hr class="divider" />
      <h3 class="headline-sm">Why would you risk it? Let's find out!</h3>

    </div>
  </div>
</template>

<script>
import NavigationBar from "@/components/NavigationBar.vue";



export default {
  name: "IndexVue",
  components: { NavigationBar  },


};
</script>

<style>
.container {
  text-align: center;
}

.headline {
  font-family: "Garamond", serif;
  margin: 0;
  padding: 10px;
}

.icon-container {
  display: flex;
  justify-content: space-between;
  max-width: 1000px;
  margin: 0 auto 20px;
}

.icon {
  background-color: #f5f5f5;
  border-radius: 70%;
  padding: 30px;
}

.icon-large {
  font-size: 40px; /* Adjust this value to make the icons bigger */
  padding: 50px; /* Adjust this value to add more space around the icons */
}

.headline-lg-container {
  background-color: #333;
  display: inline-block;
  padding: 10px 20px;
  margin-bottom: 10px;
  width: 100%;
}

.headline-lg {
  font-size: 36px;
  font-weight: normal;
  color: #fff;
  margin: 0;
}

.headline-md {
  font-size: 28px;
  font-weight: normal;
  background-color: #eee;
  padding: 10px 15px;
}

.headline-sm {
  font-size: 20px;
  font-weight: normal;
  background-color: #f5f5f5;
  padding: 10px 10px;
  margin-top: 15px;
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin: 10px 0;
}

/* Additional styles for icon descriptions */
.icon-description {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px; /* Add padding to separate the backgrounds */
  background-color: #f9f9f9; /* Add background color for each icon description */
}

.weather-descriptions {
  display: flex;
  justify-content: space-between;
}

.background-text {
  font-size: 14px;
}

.action-icon.mdi-48px {
  font-size: 48px;
  padding: 8px;
}

.action-icons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}


</style>