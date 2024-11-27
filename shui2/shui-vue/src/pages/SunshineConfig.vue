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
  <div>
    <iframe
        v-if="iframeSrc"
        :src="iframeSrc"
    ></iframe>
  </div>
</template>

<style scoped>
div {
  width: 100%;
  height: 100%;
}

iframe {
  height: 100%;
  width: 100%;
  border: none;
}
</style>
