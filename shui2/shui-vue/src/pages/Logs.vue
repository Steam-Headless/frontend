<script setup>
import {ref} from "vue";
import arrowRight from '@/assets/icons/keyboard_arrow_down.svg';
import arrowDown from '@/assets/icons/keyboard_arrow_right.svg';

const logTitles = ['audiostream.err.log', 'audiostream.log', 'desktop.err.log', 'desktop.log', 'novnc.err.log', 'novnc.log', 'pulseaudio.err.log', 'sunshine.err.log', 'sunshine.log', 'x11vnc.err.log', 'x11vnc.log', 'xorg.err.log', 'xorg.log'];

const logs = ["Log 1", "Log 2", "Log 3"];

const dropdownStates = ref(
  logTitles.reduce((acc, title) => {
    acc[title] = false;
    return acc;
  }, {})
);

const toggleDropdown = (logTitle) => {
  dropdownStates.value[logTitle] = !dropdownStates.value[logTitle]; // toggle dropdown state
};
</script>

<template>
    <div class="page-wrapper">
      <h1 class="page-title">Logs</h1>
      <div class="logs-container">
        <div v-for="logTitle in logTitles" :key="logTitle" class="log-wrapper">

          <div @click="toggleDropdown(logTitle)" class="log-title">
            <img 
              :src="dropdownStates[logTitle] ? arrowRight : arrowDown"
              alt="Toggle Arrow"
              class="arrow-icon"
            />
            <label style="cursor: pointer; font-weight: 600;">{{ logTitle }}</label>
          </div>
            
          <!-- render logs if dropdown is open -->
           <div v-if="dropdownStates[logTitle]" class="log-content">
            <div v-for="log in logs" :key="log">
              <p>{{ log }}</p>
            </div>
           </div>

        </div>
      </div>
  </div>
</template>

<style scoped>
.logs-container {
  background-color: var(--color-white);
  color: var(--color-text-dark);
  width: 100%;
  max-height: 100%;
  overflow-y: auto;
  padding: 20px;
  border-radius: 10px;
}

.log-wrapper {
  border: 1px solid var(--color-border-grey);
  border-radius: 2px;
  margin: 5px;
}

.log-title {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  padding: 10px;
  font-size: 16px;
}

.log-content {
  padding: 10px;
  border-top: 1px solid var(--color-border-grey);
  background-color: var(--color-off-white);
}
</style>