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