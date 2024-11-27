<script setup>
import homeIcon from '@/assets/icons/home.svg';
import connectIcon from '@/assets/icons/connect.svg';
import logsIcon from '@/assets/icons/logs.svg';
import faqIcon from '@/assets/icons/faq.svg';
import settingsIcon from '@/assets/icons/settings.svg';
import appManagerIcon from '@/assets/icons/app-manager.svg';
import sunshineIcon from '@/assets/icons/logo-sunshine.svg';
</script>

<template>
  <div class="sidebar">
    <div class="sidebar-content">
      <div class="title-content">
        <RouterLink to="/home">
          <img src="@/assets/steam-headless-logo.png" id="logo" />
        </RouterLink>
        <RouterLink to="/home" style="text-decoration: none">
          <h1 class="title">Steam Headless</h1>
        </RouterLink>
      </div>
      <div class="sidebar-items">
        <RouterLink to="/home" class="nav-item">
          <img :src="homeIcon"/>
          Home</RouterLink>
        <RouterLink to="/vnc" class="nav-item">
          <img :src="connectIcon"/>
          Connect</RouterLink>
        <RouterLink to="/logs" class="nav-item">
          <img :src="logsIcon"/>
          Logs</RouterLink>
        <RouterLink to="/faq" class="nav-item">
          <img :src="faqIcon"/>
          FAQ</RouterLink>
        <RouterLink to="/appmanager" class="nav-item">
          <img :src="appManagerIcon"/>
          App Manager</RouterLink>
        <RouterLink to="/sunshineconfig" class="nav-item">
          <img :src="sunshineIcon"/>
          Sunshine</RouterLink>
        <RouterLink to="/settings" class="nav-item">
          <img :src="settingsIcon"/>
          Settings</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  /* width: 40vw; */
  max-width: 400px;
  height: 100vh;
  background-color: var(--color-blue-transparent);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px); /* For Safari compatibility */
}
.sidebar-content {
}

.title-content {
  padding: 20px 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid var(--color-black);
}

.title {
  font-size: 26px;
  color: var(--color-text-light);
}

#logo {
  height: 60px;
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
  padding-left: 30px;
  margin: 5px 20px;
  /* background-color: var(--color-nav-dull); */
  border-radius: 10px;
  color: var(--color-text-light);
  text-decoration: none;
  transition: ease-in-out 0.1s;
}

.nav-item:hover {
  background-color: var(--color-nav-active);
}
.nav-item.is-active {
  background-color: var(--color-nav-active);
}
</style>
