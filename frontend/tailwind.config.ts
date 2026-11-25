import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dream: {
          ivory: "#FFFDF9",
          "ivory-dark": "#F7F2EA",
          blush: "#FBE6ED",
          "blush-dark": "#F3BACF",
          lavender: "#EBE6FA",
          "lavender-dark": "#D5CBF5",
          peach: "#FDEAE2",
          "peach-dark": "#F7C7B7",
          sky: "#E2F0FB",
          "sky-dark": "#BADAF4",
          champagne: "#F6ECDC",
          "champagne-dark": "#E2CEB1",
          plum: "#362544",
          "plum-light": "#614C72",
          "plum-muted": "#8A799B",
          gold: "#CCA456",
          rose: "#E498AA",
        },
      },
      fontFamily: {
        serif: ["var(--font-serif)", "Cormorant Garamond", "Georgia", "serif"],
        sans: ["var(--font-sans)", "Plus Jakarta Sans", "Inter", "sans-serif"],
        script: ["var(--font-script)", "Caveat", "cursive"],
      },
      boxShadow: {
        dreamy: "0 10px 40px -10px rgba(186, 160, 217, 0.25)",
        "dreamy-lg": "0 20px 60px -15px rgba(186, 160, 217, 0.35)",
        polaroid: "0 12px 28px rgba(54, 37, 68, 0.08), 0 2px 6px rgba(54, 37, 68, 0.04)",
        glow: "0 0 35px rgba(229, 210, 255, 0.6)",
        "gold-glow": "0 0 25px rgba(204, 164, 86, 0.4)",
      },
      animation: {
        "float-slow": "float 7s ease-in-out infinite",
        "float-reverse": "floatReverse 8s ease-in-out infinite",
        "pulse-glow": "pulseGlow 4s ease-in-out infinite",
        "star-twinkle": "twinkle 3s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px) rotate(0deg)" },
          "50%": { transform: "translateY(-10px) rotate(1deg)" },
        },
        floatReverse: {
          "0%, 100%": { transform: "translateY(0px) rotate(0deg)" },
          "50%": { transform: "translateY(12px) rotate(-1deg)" },
        },
        pulseGlow: {
          "0%, 100%": { opacity: "0.6", transform: "scale(1)" },
          "50%": { opacity: "1", transform: "scale(1.05)" },
        },
        twinkle: {
          "0%, 100%": { opacity: "0.2", transform: "scale(0.8)" },
          "50%": { opacity: "1", transform: "scale(1.2)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
