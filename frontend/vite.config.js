import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./dist"),
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/main.ts"),
        preview: resolve(__dirname, "src/styles/preview.css"),
        "admin-theme-sync": resolve(__dirname, "src/admin-theme-sync.ts"),
      },
    },
  },
});
