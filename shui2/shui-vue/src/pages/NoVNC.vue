<script>
export default {
  data() {
    return {
      iframeSrc: null,
    };
  },
  async mounted() {
    try {
      // Ref for args: https://github.com/novnc/noVNC/blob/master/docs/EMBEDDING.md
      this.iframeSrc = `/web/index.html?autoconnect=true&resize=scale`;
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
    height: calc(100vh - 4px); /* 100vh causes scrollbar to appear */
  }
  iframe {
    height: 100%;
    width: 100%;
    border: none;
  }
</style>