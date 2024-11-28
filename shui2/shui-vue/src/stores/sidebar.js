import { defineStore } from "pinia";

export const useSidebarStore = defineStore("sidebar", {
  state: () => ({
    isExtended: false,
  }),
  actions: {
    toggleSidebar() {
      this.isExtended = !this.isExtended;
    },
    extendSidebar() {
      this.isExtended = true;
    },
    collapseSidebar() {
      this.isExtended = false;
    },
  },
});
