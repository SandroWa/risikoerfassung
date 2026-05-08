import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite-Devserver leitet /api/* an das Litestar-Backend (Port 8000) weiter,
// dadurch entfällt CORS-Konfiguration im Backend.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});

