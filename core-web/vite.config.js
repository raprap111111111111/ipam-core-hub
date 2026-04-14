import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // This is the cleanest way to point to the file we verified exists
      'vue-toastification': 'vue-toastification/dist/index.mjs'
    }
  },
  // ADD THIS SECTION: It helps Vite 6 handle ESM dependencies better on some servers
  optimizeDeps: {
    include: ['vue-toastification']
  }
})