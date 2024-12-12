<script>
import { ref } from "vue";
import closeIcon from '@/assets/icons/close.svg';

export default {
  setup() {
    const logsList = ref([]);
    const logContent = ref(null);
    const isPanelOpen = ref(false);
    const activeFileName = ref("");
    const activeLogContent = ref([]);

    const fetchLogsList = async() => {
      try {
        const response = await fetch('/api/logs/list');
        const data = await response.json();
        logsList.value = data;
      } catch (error) {
        console.error('Error fetching logs list: ', error);
        logsList.value = ["Error fetching logs list"]
      }
    };

    // fetch content of specific log file
    const fetchLogContent = async (fileName) => {
      try {
        const response = await fetch(`/api/logs/content/${fileName}`);
        const data = await response.json();
        console.log(data);
        logContent.value = data;
        activeLogContent.value = logContent.value;

        // if no logs exist in file
        if (logContent.value == "") {
          activeLogContent.value = ["No logs in this file"]
        }
      } catch (error) {
        console.error('Error fetching log content: ', error);
        activeLogContent.value = ["Error fetching log content."]
      }
    };

    // open the dialog panel and set content
    const openPanel = (fileName) => {
      activeFileName.value = fileName;
      fetchLogContent(fileName);
      activeLogContent.value = logContent;
      isPanelOpen.value = true;
    }

    const closePanel = () => {
      isPanelOpen.value = false;
      activeFileName.value = "";
      activeLogContent.value = [];
    }

    // call fetchLogsList on component mount
    fetchLogsList();

    return {
      logsList,
      logContent,
      activeLogTitle: activeFileName,
      activeLogContent,
      isPanelOpen,
      openPanel,
      closePanel,
      closeIcon
    };
  },
};

</script>

<template>
  <div class="page-wrapper">
    <div class="page-container">
      <h1 class="page-title">Logs</h1>

      <!-- List of logs -->
      <div class="logs-list">
        <div v-for="fileName in logsList" :key="fileName" class="log-title-wrapper">
          <div @click="openPanel(fileName)" class="log-title">
            <label style="cursor: pointer; font-weight: 500;">{{ fileName }}</label>
          </div>
        </div>
      </div>

      <!-- Side Panel -->
      <div class="panel-container" :class="{ open: isPanelOpen }">
        <div class="side-panel" >
          <header class="panel-header">
            <h2>{{ activeLogTitle }}</h2>
            <button @click="closePanel" class="close-button">
              <img :src="closeIcon" alt="Close Icon" />
            </button>
          </header>

          <!-- Logs content container -->
          <div class="log-content">
            <div class="log-line" v-for="(log, index) in activeLogContent" :key="index">
              <div class="log-index">{{ index + 1 }}</div>
              <div class="log-message">{{ log }}</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.logs-list {
  margin-top: 2rem;
  background-color: var(--color-light-grey);
  overflow-y: auto;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 2px 0px 10px rgba(0, 0, 0, 0.5);
}

.log-title-wrapper {
  border: 1px solid var(--color-nav-dull);
  border-radius: 4px;
  margin: 5px;
}

.log-title {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  padding: 10px;
  font-size: 16px;
  transition: ease-in-out 0.1s;
}
.log-title:hover {
  border-radius: 4px;
  background-color: var(--color-nav-active);
}

/* Side panel styles */
.panel-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  position: fixed;
  top: 0;
  right: -60vw; /* off screen by default */
  width: 60vw;
  height: 100vh;
  transition: right 0.2s ease-in-out;
  visibility: hidden; /* hides panel so it doesnt peak out on browser resize */
}

.side-panel {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 3rem); /* full height minus the margin */
  margin-right: 1.5rem;
  width: 100%;
  background-color: var(--color-light-grey);
  border-left: 1px solid var(--color-grey);
  box-shadow: 2px 0px 20px rgba(0, 0, 0, 0.5);
  padding: 20px;
  border-radius: 4px;
}

.panel-container.open {
  right: 0px; /* move into view when open */
  visibility: visible;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.log-content {
  flex-grow: 1; /* makes the div full height even if content does not fill the full height*/
  background-color: var(--color-grey);
  padding: 10px;
  border-top: 1px solid var(--color-text-light);
  overflow-y: auto;
  border-radius: 2px;
  border: 1px solid var(--color-nav-active);
}

.log-index, .log-message {
  padding: 2px 0;
  font-family: monospace;
}

.log-line {
  display: flex;
}

.log-index {
  min-width: 2rem;
  color: var(--color-nav-active);
}
.log-message {
  flex-grow: 1;
  color: var(--color-text-light);
}

/* Scrollbar styles */
.log-content::-webkit-scrollbar {
  width: 8px;
  
  background-color: var(--color-nav-dull);
  
}
.log-content::-webkit-scrollbar-thumb {
  background: var(--color-nav-active);
  border-radius: 4px;
}

.close-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  padding: 4px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: ease-in-out 0.1s;
}
.close-button:hover {
  background-color: var(--color-nav-active);
}
</style>