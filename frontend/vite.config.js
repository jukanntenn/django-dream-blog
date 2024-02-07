import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./dist"),
    rollupOptions: {
      input: "src/main.ts",
    },
  },
});
