import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // We found index.mjs in your ls output, so use it here:
      'vue-toastification': fileURLToPath(new URL('./node_modules/vue-toastification/dist/index.mjs', import.meta.url))
    }
  }
})