<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main>
      Upload file
    </v-main>
  </v-app>
</template>

<script>
  export default {
    components: {
    },
    data() {
      return {
        index: 0, // default: 0
        center: [46.508, 6.587],
        mapOptions: {
          zoomSnap: 0.5
        },
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',

      }
    },
    methods: {
      goToSlide(index) {
        this.index = index
      }
    }
  }
</script>
<style scoped>
</style>