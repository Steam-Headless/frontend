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
    host: '192.168.8.220',
    port: 8084,
    proxy: {
      '/api': {
          target: 'http://192.168.8.220:3002',
      },
      '/web': {
          target: 'http://192.168.8.220:3002',
      },
      '/noVNC': {
          target: 'http://192.168.8.220:3002',
      },
      '/websockify': {
          target: 'ws://192.168.8.220:3002',
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
