<script>
import configService from "@/services/configService.js";

export default {
  data() {
    return {
      iframeSrc: null,
    };
  },
  async mounted() {
    try {
      // Fetch config
      const config = await configService.serverConfig();
      // Get the current hostname from the browser
      const hostname = window.location.hostname;
      const protocol = window.location.protocol;
      console.log(config.sunshineProxyPort)
      // Construct the new URL with the hostname and config-provided port
      this.iframeSrc = `${protocol}//${hostname}:${config.sunshineProxyPort}`;
      console.log(this.iframeSrc)
    } catch (error) {
      console.error("Failed to load config:", error);
    }
  },
};
</script>

<template>
  <div class="iframe-container">
    <iframe
        v-if="iframeSrc"
        :src="iframeSrc"
    ></iframe>
  </div>
</template>

<style scoped>
.iframe-container {
  width: 100%;
  height: calc(100vh - 4px); /* 100vh causes double scrollbar to appear */
}

iframe {
  height: 100%;
  width: 100%;
  border: none;
}
</style>
