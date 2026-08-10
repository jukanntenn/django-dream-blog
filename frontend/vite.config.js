import { defineConfig } from "vite";
import { resolve } from "node:path";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
  base: "/static/",
  server: {
    // Read PORT from environment variable for dev-manager-mcp integration
    // Fallback to 5173 if not set
    port: Number(process.env.PORT) || 5173,
    host: "0.0.0.0",
  },
  build: {
    manifest: "manifest.json",
    outDir: resolve(__dirname, "dist"),
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/main.ts"),
        admin: resolve(__dirname, "src/admin/main.ts"),
      },
    },
  },
});
