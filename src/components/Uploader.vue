<template>
    <v-main>
      <v-container>
        <v-row>
          <v-col>
            <v-row>
              <v-col>
                <v-file-input v-model="selectedFile" @change=previewImage accept="image/*" ></v-file-input>
              </v-col>
              <v-col>
                <v-text-field
                  label="Description"
                  v-model="description"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-btn @click="upload">
                  Upload
                  <v-icon
                    right
                    dark
                  >
                    mdi-cloud-upload
                  </v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
          <v-col>
            <v-img :src=url></v-img>
          </v-col>
         </v-row>
      </v-container>
    </v-main>
</template>

<script>
  export default {
    components: {
    },
    data() {
      return {
        url: '',
        selectedFile: null,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        description: ''
      }
    },
    methods: {
      previewImage(file) {
        if (file !== null) {
          this.url = URL.createObjectURL(file)
        } else {
          this.url = ''
        }
      },
      upload() {
        if (this.selectedFile === null) {
          alert("Select file")
          return
        }
        if (this.description === '') {
          alert("Add description")
          return
        }
        console.log("uploading")
        this.selectedFile = null
        this.description = ''
        this.url = ''
      }
    }
  }
</script>
<style scoped>
</style>