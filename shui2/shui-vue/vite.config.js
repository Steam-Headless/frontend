import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import dotenv from 'dotenv'

// Load environment variables from .env in the same directory
dotenv.config({path: new URL('./.env', import.meta.url)})

const backendHost = process.env.BACKEND_HOST || 'localhost'
const backendPort = process.env.BACKEND_PORT || '8083'
const backendUrl = `http://${backendHost}:${backendPort}`
const backendWsUrl = `ws://${backendHost}:${backendPort}`

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
                target: backendUrl,
            },
            '/web': {
                target: backendUrl,
            },
            '/noVNC': {
                target: backendUrl,
            },
            '/websockify': {
                target: backendWsUrl,
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
