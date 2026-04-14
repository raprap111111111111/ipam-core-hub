import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // ADD THIS SECTION BELOW TO FIX THE BUILD ERROR
  optimizeDeps: {
    include: ['vue-toastification'],
  },
  build: {
    commonjsOptions: {
      include: [/vue-toastification/, /node_modules/],
    },
  },
})