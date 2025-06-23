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
      // Construct the new URL with the hostname and config-provided port
      this.iframeSrc = `/sunshine/`;
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
