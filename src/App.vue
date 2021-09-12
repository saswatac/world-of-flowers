<template>
  <div>
    <carousel-3d ref=mycarousel :controls-visible="true" @after-slide-change="onAfterSlideChange">
      <slide v-for="(image, i) in imgs" v-bind:key="i" :index=i>
        <div @click="() => showSingle(i)">
          <img :src=imgs[i].url alt="Italian Trulli">
        </div>
      </slide>
    </carousel-3d>
    <GmapMap
      :center='center'
      :zoom='12'
      style='width:100%;  height: 400px;'
    >
      <GmapMarker
        :key="index"
        v-for="(m, index) in imgs"
        :position="imgs[index].location"
        :clickable="true"
        @click="() => goToSlide(index)"
      />
    </GmapMap>
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

  export default {
    components: {
      VueEasyLightbox,
      Carousel3d,
      Slide,
    },
    data() {
      return {
        imgs: [
            { url: "https://images.unsplash.com/photo-1628191012047-e789922abfdf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1650&q=80",
              location: { lat: 47.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            },
            { url: "http://localhost:8000/PXL_20210905_121021611.jpg",
              location: { lat: 46.508, lng: 6.587 }
            }

        ], // Img Url , string or Array of string
        visible: false,
        index: 0, // default: 0
        selected_img: '',
        center: { lat: 46.508, lng: 6.587 },
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