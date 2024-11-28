<script setup>
import Sidebar from './components/Sidebar.vue';
import { RouterView } from "vue-router";
</script>

<template>
  <main>
    <Sidebar/>
    <div class="content">
      <RouterView />
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  justify-content: space-between;
}

.content {
  margin-top: 20px;
  margin-bottom: 4px;
  display: flex;
  justify-content: center;
  flex-grow: 1;
}
</style>