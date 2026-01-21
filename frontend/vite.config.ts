import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/clariscan-ai/",   // 🔥 THIS IS THE FIX
});
