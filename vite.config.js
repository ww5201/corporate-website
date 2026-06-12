import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        index: resolve(__dirname, 'index.html'),
        category: resolve(__dirname, 'category.html'),
        flash: resolve(__dirname, 'flash.html'),
        chat: resolve(__dirname, 'chat.html'),
        mine: resolve(__dirname, 'mine.html'),
      },
    },
  },
  server: {
    port: 3000,
    open: '/index.html'
  }
});
