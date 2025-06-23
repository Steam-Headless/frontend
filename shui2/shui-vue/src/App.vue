<script setup>
import Sidebar from './components/Sidebar.vue';
import {RouterView} from "vue-router";

</script>

<template>
  <main>
    <Sidebar/>
    <div class="content">
      <RouterView/>
    </div>
  </main>
</template>

<style scoped>

main {
  display: flex;
  justify-content: space-between;
}

.content {
  margin-bottom: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  padding-left: 85px; /* shift content by width of minimised sidebar */
  transition: padding-left 0.2s ease-in-out;
}
</style>
