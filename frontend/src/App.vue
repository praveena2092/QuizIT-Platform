<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from "./components/Footer.vue"

</script>

<template>
        <div class="full-screen">
        <Navbar/>
        <router-view/>
        <Footer></Footer>
       
        </div>
     
</template>

<style scoped>
.full-screen {
  width: 100vw;
  height: 100vh;
   /* Optional: prevents scrollbars */
}
</style>

