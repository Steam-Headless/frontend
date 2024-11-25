<script>
export default {
  data() {
    return {
      iframeSrc: null,
    };
  },
  async mounted() {
    try {
      // const response = await fetch("/api/config"); // fetch config from backend
      // const config = await response.json();
      this.iframeSrc = `http://192.168.8.220:8082/web/index.html?autoconnect=true`;
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
  }
</style>