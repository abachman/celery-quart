import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  build: {
    outDir: '../static',
  },
  plugins: [react(), tailwindcss()],
  server: {
    host: true,
    port: 3000,
    cors: true,
    proxy: {
      '^/api/.*': {
        target: 'http://web:80/',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
