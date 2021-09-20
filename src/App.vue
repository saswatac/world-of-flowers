<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <router-link to="/">
        <v-icon large>
          mdi-home
        </v-icon>
      </router-link>
      <v-spacer></v-spacer>
      <router-link to="/upload">
        <v-icon large>
          mdi-arrow-up-bold-box-outline
        </v-icon>
      </router-link>
    </v-app-bar>
    <router-view/>
  </v-app>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
