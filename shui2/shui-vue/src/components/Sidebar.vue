<script setup>
import homeIcon from '@/assets/icons/home.svg';
import connectIcon from '@/assets/icons/connect.svg';
import logsIcon from '@/assets/icons/logs.svg';
import faqIcon from '@/assets/icons/faq.svg';
import settingsIcon from '@/assets/icons/settings.svg';
import appManagerIcon from '@/assets/icons/app-manager.svg';
import sunshineIcon from '@/assets/icons/logo-sunshine.svg';
import { useSidebarStore } from "@/stores/sidebar";

const sidebarStore = useSidebarStore();
</script>

<template>
  <div class="sidebar"
    @mouseover="sidebarStore.extendSidebar"
    @mouseleave="sidebarStore.collapseSidebar"
    :class="['sidebar', { extended: sidebarStore.isExtended }]"
  >
    <div class="sidebar-content">
      <div class="title-content"
      :class="['title-content', { extended: sidebarStore.isExtended }]">
        <RouterLink to="/home">
          <img src="@/assets/steam-headless-logo.png" id="logo" />
        </RouterLink>
        <RouterLink to="/home" style="text-decoration: none">
          <h1 class="title">{{ sidebarStore.isExtended ? "Steam Headless" : "" }}</h1>
        </RouterLink>
      </div>
      <div class="sidebar-items">
        <RouterLink to="/home" class="nav-item">
          <img :src="homeIcon"/>
          {{ sidebarStore.isExtended ? "Home" : "" }}
        </RouterLink>
        <RouterLink to="/vnc" class="nav-item">
          <img :src="connectIcon"/>
          {{ sidebarStore.isExtended ? "Connect" : "" }}
        </RouterLink>
        <RouterLink to="/logs" class="nav-item">
          <img :src="logsIcon"/>
          {{ sidebarStore.isExtended ? "Logs" : "" }}
        </RouterLink>
        <RouterLink to="/faq" class="nav-item">
          <img :src="faqIcon"/>
          {{ sidebarStore.isExtended ? "FAQ" : "" }}
        </RouterLink>
        <RouterLink to="/appmanager" class="nav-item">
          <img :src="appManagerIcon"/>
          {{ sidebarStore.isExtended ? "App Manager" : "" }}
        </RouterLink>
        <RouterLink to="/sunshineconfig" class="nav-item">
          <img :src="sunshineIcon"/>
          {{ sidebarStore.isExtended ? "Sunshine" : "" }}
        </RouterLink>
        <RouterLink to="/settings" class="nav-item">
          <img :src="settingsIcon"/>
          {{ sidebarStore.isExtended ? "Settings" : "" }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 85px;
  height: 100vh;
  background-color: var(--color-blue-transparent);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px); /* For Safari compatibility */
  transition: width 0.2s;
}
.sidebar.extended {
  width: 300px;
}

.title-content {
  display: flex;
  align-items: center;
  padding: 20px 20px;
  border-bottom: 1px solid var(--color-black);
}
.title-content.extended {
  gap: 10px;
}

.title {
  font-size: 26px;
  color: var(--color-text-light);
  white-space: nowrap;
}

#logo {
  height: 44px;
}

.sidebar-items {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  margin: 5px 20px;
  /* background-color: var(--color-nav-dull); */
  border-radius: 10px;
  color: var(--color-text-light);
  text-decoration: none;
  transition: ease-in-out 0.1s;
  white-space: nowrap;
}

.nav-item:hover {
  background-color: var(--color-nav-active);
}
.nav-item.is-active {
  background-color: var(--color-nav-active);
}
</style>
