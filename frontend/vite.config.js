import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'C:\\Windows\\System32\\localhost+2-key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, 'C:\\Windows\\System32\\localhost+2.pem')),
    },
    port: 5173,
  }
})





// import path from 'path'
// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue()],
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src')
//     }
//   }
// })