<template>
  <div>
    <carousel-3d ref=mycarousel :controls-visible="true" @after-slide-change="onAfterSlideChange" :display="1" width=600>
      <slide v-for="(image, i) in imgs" v-bind:key="i" :index=i>
        <figure @click="() => showSingle(i)">
          <img :src=imgs[i].url alt="Italian Trulli" loading=lazy width=80% height=80%>
          <p>
            {{ imgs[i].description }}
          </p>
        </figure>
      </slide>
    </carousel-3d>
    <l-map ref="myMap"> </l-map>
    <l-map
      :zoom=13
      :center="center"
      :options="mapOptions"
      style="height: 850px; width: 850px"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-marker v-for="(image, i) in imgs" v-bind:key="i" :lat-lng="imgs[i].location" :opacity=0.5 v-on:click="() => goToSlide(i)">
      </l-marker>
    </l-map>
    <!-- all props & events -->
    <vue-easy-lightbox
      escDisabled
      moveDisabled
      :visible="visible"
      :imgs="selected_img"
      :index="index"
      @hide="handleHide"
    ></vue-easy-lightbox>
  </div>
</template>

<script>
  // If VueApp is already registered with VueEasyLightbox, there is no need to register it here.
  import VueEasyLightbox from 'vue-easy-lightbox';
  import { Carousel3d, Slide } from 'vue-carousel-3d';
  //import L from 'leaflet';
  import { LMap, LTileLayer, LMarker } from "vue2-leaflet";

  export default {
    components: {
      VueEasyLightbox,
      Carousel3d,
      Slide,
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
        visible: false,
        index: 0, // default: 0
        selected_img: '',
        center: [46.508, 6.587],
        mapOptions: {
          zoomSnap: 0.5
        },
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',

      }
    },
    methods: {
      showSingle(i) {
        this.selected_img = [{
          title: 'this is a placeholder',
          src: this.imgs[i].url
        }]
        this.show()
      },
      show() {
        this.visible = true
      },
      handleHide() {
        this.visible = false
      },
      onAfterSlideChange(index) {
        console.log('@onAfterSlideChange Callback Triggered', 'Slide Index ' + index)
        this.index = index
      },
      goToSlide(index) {
        this.$refs.mycarousel.goSlide(index)
      }
    }
  }
</script>
<style scoped>
figure {
    border: thin #c0c0c0 solid;
    display: flex;
    flex-flow: column;
    padding: 5px;
    max-width: 220px;
    margin: auto;
}



figcaption {
    background-color: #222;
    color: #fff;
    font: italic smaller sans-serif;
    padding: 3px;
    text-align: center;
}
</style>