<template>
  <div id="app">
    <!-- <navbar/> -->
      <router-view :key="$route.fullPath"/>
  </div>
</template>
<script>
// import navbar from './components/navbar.vue'
export default {
  name: 'App',
  components: {
    // navbar
  }
}
</script>
<style>
</style>
