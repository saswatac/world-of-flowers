<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-spacer></v-spacer>
      <router-link to="/upload">
        <v-icon large>
          mdi-arrow-up-bold-box-outline
        </v-icon>
      </router-link>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <v-row>
          <v-col cols="12" lg="9">
            <v-carousel v-model="index" height="auto" hide-delimiters>
              <v-carousel-item
                v-for="(image, i) in imgs"
                v-bind:key="i"
              >
                <v-row>
                  <v-col>
                    <v-img :src=imgs[i].url max-height="750"></v-img>
                  </v-col>
                </v-row>
                <v-row><v-col><v-subheader>{{ imgs[i].description }}</v-subheader></v-col></v-row>
              </v-carousel-item>
            </v-carousel>
          </v-col>
          <v-col cols="12" lg="3">
            <l-map
              :zoom=13
              :center="center"
              :options="mapOptions"
              style="height: 300px"
            >
              <l-tile-layer
                :url="url"
                :attribution="attribution"
              />
              <l-marker v-for="(image, i) in imgs" v-bind:key="i" :lat-lng="imgs[i].location" v-on:click="() => goToSlide(i)">
              </l-marker>
            </l-map>
          </v-col>
         </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  // If VueApp is already registered with VueEasyLightbox, there is no need to register it here.
  //import VueEasyLightbox from 'vue-easy-lightbox';
  //import { Carousel3d, Slide } from 'vue-carousel-3d';
  //import L from 'leaflet';
  import { LMap, LTileLayer, LMarker } from "vue2-leaflet";

  export default {
    components: {
      LMap,
      LMarker,
      LTileLayer,
      //LPopup,
      //LTooltip
    },
    data() {
      return {
        imgs: [
            { url: "http://localhost:8000/PXL_20210905_112008235.MP.jpg",
              location: [47.508, 6.587],
              description: "test"
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test",
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test"
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test"
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test"
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test"
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test"
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: [46.508, 6.587],
              description: "test"
            }

        ], // Img Url , string or Array of string
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