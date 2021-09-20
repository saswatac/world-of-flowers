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
         <v-row><v-col><div id="google-signin-button"></div></v-col></v-row>
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
        description: '',
        id_token: ''
      }
    },
    mounted() {
      window.gapi.signin2.render('google-signin-button', {
        onsuccess: this.onSignIn
      })
    },
    methods: {
      previewImage(file) {
        if (file !== null) {
          this.url = URL.createObjectURL(file)
        } else {
          this.url = ''
        }
      },
      async upload() {
        if (this.selectedFile === null) {
          alert("Select file")
          return
        }
        if (this.description === '') {
          alert("Add description")
          return
        }
        if (this.id_token === '') {
          alert("You must sign in to upload")
        }
        var formData = new FormData();
        formData.append("image", this.selectedFile, this.selectedFile.name);
        formData.append("description", this.description);
        const response = await fetch(`http://192.168.1.112:8081?token=${this.id_token}`, {
          method: 'POST',
          mode: 'cors',
          cache: 'no-cache',
          credentials: 'same-origin',
          redirect: 'follow', // manual, *follow, error
          referrerPolicy: 'no-referrer',
          body: formData
        });
        if (response.ok !== true) {
          alert(await response.text())
        } else {
          this.selectedFile = null
          this.description = ''
          this.url = ''
        }
      },
      onSignIn (user) {
        this.id_token = user.getAuthResponse().id_token
      }
    }
  }
</script>
<style scoped>
</style>