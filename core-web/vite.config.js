import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // This is what makes the "@" work!
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})