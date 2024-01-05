<template>
  <DownloadInput msg="Welcome to Your Vue.js App"/>
  <br>
  <VideoTable msg="Welcome to Your Vue.js App"/>
  
</template>

<script>
import VideoTable from './components/VideoTable.vue'
import DownloadInput from './components/DownloadInput.vue'

export default {
  name: 'App',
  components: {
    VideoTable,
    DownloadInput
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
