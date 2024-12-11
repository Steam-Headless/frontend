<script setup>
import Sidebar from './components/Sidebar.vue';
import { RouterView } from "vue-router";
import { useSidebarStore } from "@/stores/sidebar";

const sidebarStore = useSidebarStore();
</script>

<template>
  <main>
    <Sidebar/>
    <div :class="['content', { 'sidebar-expanded': sidebarStore.isExtended }]">
      <RouterView />
    </div>
  </main>
</template>

<style scoped>

main {
  display: flex;
  justify-content: space-between;
  color: var(--text-light);
}

.content {
  margin-bottom: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  padding-left: 85px; /* shift content by width of minimised sidebar */
  transition: padding-left 0.2s ease-in-out;
}
.content.sidebar-expanded {
  padding-left: 300px /* shift the content by width of expanded sidebar  */
}
</style>