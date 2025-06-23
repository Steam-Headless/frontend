import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  server: {
    port: 8084,
    host: '0.0.0.0',
    proxy: {
      '/api': {
          target: 'http://localhost:8083',
      },
      '/web': {
          target: 'http://localhost:8083',
      },
      '/noVNC': {
          target: 'http://localhost:8083',
      },
      '/websockify': {
          target: 'ws://localhost:8083',
          ws: true,
      }
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
