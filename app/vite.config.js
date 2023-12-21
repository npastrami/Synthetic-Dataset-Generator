import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/upload': 'http://localhost:5174',
      '/convert': 'http://localhost:5174',
      '/download': 'http://localhost:5174',
      '/craft': 'http://localhost:5174',
      '/copy': 'http://localhost:5174',
      '/makecopies': 'http://localhost:5174',
    }
  }
})
