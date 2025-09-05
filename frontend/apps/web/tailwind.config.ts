import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";
import typography from "@tailwindcss/typography";
import aspectRatio from "@tailwindcss/aspect-ratio";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./features/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          main: "#99F6E4",
          neon: "#38BDF8",
          pink: "#FF8FAB",
          purple: "#A78BFA",
        },
        bg: {
          soft: "#FFF7F9",
        },
        text: {
          dark: "#2B2B2B",
          light: "#FFFFFF",
        },
      },
      borderRadius: {
        lg: "12px",
      },
      boxShadow: {
        card: "0 2px 8px rgba(0,0,0,0.05)",
      },
    },
  },
  plugins: [animate, typography, aspectRatio],
};

export default config;
