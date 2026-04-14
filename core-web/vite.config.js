// vite.config.js
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // Add the $ at the end!
      'vue-toastification$': fileURLToPath(new URL('./node_modules/vue-toastification/dist/index.mjs', import.meta.url))
    }
  }
})