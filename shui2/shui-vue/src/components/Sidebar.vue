<script setup>
import {ref} from 'vue';
import {RouterLink} from 'vue-router';
import Drawer from 'primevue/drawer';

import homeIcon from '@/assets/icons/home.svg';
import vncIcon from '@/assets/icons/vnc.svg';
import logsIcon from '@/assets/icons/logs.svg';
import sunshineIcon from '@/assets/icons/logo-sunshine.svg';

const visible = ref(true);

function show() {
  visible.value = true;
}

function hide() {
  visible.value = false;
}
</script>

<template>
  <!-- always-visible 85px strip -->
  <div
      class="mini-trigger flex flex-column align-items-center"
      @mouseover="show"
  >
    <!-- top-aligned logo -->
    <img src="@/assets/steam-headless-logo.png"
         style="height: 44px;"/>

    <!-- this grows to fill the rest of the 100vh and centers its child -->
    <div class="flex-grow-1 flex align-items-center justify-content-center">
      <i class="pi pi-angle-double-right open-icon"></i>
    </div>
  </div>

  <!-- overlay drawer -->
  <Drawer
      v-model:visible="visible"
      position="left"
      :modal="false"
      :dismissable="false"
      :showCloseIcon="false"
      @hide="hide"
      baseZIndex="1000"
      class="sidebar-drawer"
  >
    <div class="sidebar-drawer-content" @mouseleave="hide">
      <div class="sidebar-drawer-title-content">
        <RouterLink to="/">
          <img src="@/assets/steam-headless-logo.png" style="height: 44px;"/>
        </RouterLink>
        <h1>Steam Headless</h1>
      </div>

      <div class="sidebar-drawer-items">
        <RouterLink to="/" class="sidebar-drawer-nav-item">
          <img :src="homeIcon" class="sidebar-drawer-nav-item-icon"/>
          Home
        </RouterLink>
        <RouterLink to="/vnc" class="sidebar-drawer-nav-item">
          <img :src="vncIcon" class="sidebar-drawer-nav-item-icon"/>
          Connect
        </RouterLink>
        <RouterLink to="/logs" class="sidebar-drawer-nav-item">
          <img :src="logsIcon" class="sidebar-drawer-nav-item-icon"/>
          Logs
        </RouterLink>
        <RouterLink to="/sunshineconfig" class="sidebar-drawer-nav-item">
          <img :src="sunshineIcon" class="sidebar-drawer-nav-item-icon"/>
          Sunshine
        </RouterLink>
        <!-- add/remove links as needed -->
      </div>
    </div>
  </Drawer>
</template>

<style>
/* Mini mouseover strip */
.mini-trigger {
  position: fixed;
  top: 0;
  left: 0;
  width: 85px;
  height: 100vh;
  background-color: var(--color-blue);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 11px;
  z-index: 999;
}

/* Sidebar Drawer */
.sidebar-drawer {
  background-color: var(--color-blue) !important;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

/* Sidebar Drawer Content */
.sidebar-drawer-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-drawer-title-content {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-drawer-title-content h1 {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--color-off-white);
}

.sidebar-drawer-items {
  flex: 1;
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
}

.sidebar-drawer-nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  margin: 0.25rem 0;
  border-radius: 0.5rem;
  color: var(--color-off-white);
  text-decoration: none;
  transition: background 0.1s;
  font-size: 1.5rem;
  font-weight: 500;
}

.sidebar-drawer-nav-item:hover {
  background-color: var(--color-nav-active);
}

.sidebar-drawer-nav-item-icon {
  height: 2rem;
}
</style>
