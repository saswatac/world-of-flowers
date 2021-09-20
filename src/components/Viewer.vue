<template>
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
                    <v-img :src=imgs[i].src lazy-src="https://picsum.photos/id/11/100/60" max-height="750">
                    <template v-slot:placeholder>
                      <v-row
                        class="fill-height ma-0"
                        align="center"
                        justify="center"
                      >
                        <v-progress-circular
                          indeterminate
                          color="grey lighten-5"
                        ></v-progress-circular>
                      </v-row>
                    </template>
                    </v-img>
                  </v-col>
                </v-row>
                <v-row><v-col><v-subheader>{{ imgs[i].description }}</v-subheader></v-col></v-row>
              </v-carousel-item>
            </v-carousel>
          </v-col>
          <v-col cols="12" lg="3">
            <l-map
              :zoom=13
              :bounds="bounds"
              :options="mapOptions"
              @update:bounds="updateBounds"
              style="height: 300px"
            >
              <l-tile-layer
                :url="url"
                :attribution="attribution"
              />
              <l-marker v-for="(image, i) in imgs" v-bind:key="i" :lat-lng="imgs[i].latlng" :opacity="i===index ? 1.0 : 0.5" v-on:click="() => goToSlide(i)">
              </l-marker>
            </l-map>
          </v-col>
         </v-row>
      </v-container>
    </v-main>
</template>

<script>
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
        imgs: [],
        index: 0, // default: 0
        //center: [46.508, 6.587],
        bounds: [
          [47.90932351276647, 10.3417396],
          [45.65280826414791, 5.991153717]
        ],
        mapOptions: {
          zoomSnap: 0.5
        },
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',

      }
    },
    created() {
      fetch(`http://192.168.1.112:8081?ne=${this.bounds[0]}&sw=${this.bounds[1]}`)
        .then(response => response.json())
        .then(data => this.imgs = data["images"]);
    },
    methods: {
      goToSlide(index) {
        this.index = index
      },
      updateBounds(x) {
        fetch(`http://192.168.1.112:8081?ne=${x._northEast.lat},${x._northEast.lng}&sw=${x._southWest.lat},${x._southWest.lng}`)
        .then(response => response.json())
        .then(data => this.imgs = data["images"]);
        this.index = 0
      }
    }
  }
</script>
<style scoped>
</style>