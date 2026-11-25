"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { ThemeMode, THEME_PALETTES, ThemeColors } from "@/types/theme";

interface ThemeContextType {
  theme: ThemeMode;
  themeColors: ThemeColors;
  setTheme: (mode: ThemeMode) => void;
  applyAnswerTheme: (favoriteColors: string[], visionText: string) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const THEME_STORAGE_KEY = "converse_ai_theme_mode";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  // Default to Midnight Cosmic dark theme
  const [theme, setCurrentTheme] = useState<ThemeMode>("midnight-cosmic");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode;
      if (saved && THEME_PALETTES[saved]) {
        applyThemeStyles(saved);
        setCurrentTheme(saved);
      } else {
        applyThemeStyles("midnight-cosmic");
      }
    }
  }, []);

  const applyThemeStyles = (mode: ThemeMode) => {
    const palette = THEME_PALETTES[mode] || THEME_PALETTES["midnight-cosmic"];
    const root = document.documentElement;

    root.style.setProperty("--color-bg", palette.bg);
    root.style.setProperty("--color-card", palette.cardBg);
    root.style.setProperty("--color-text", palette.text);
    root.style.setProperty("--color-muted", palette.textMuted);
    root.style.setProperty("--color-accent", palette.accent);
    root.style.setProperty("--color-glow", palette.glow);
    root.style.setProperty("--color-border", palette.border);

    if (mode === "celestial-ivory") {
      root.classList.remove("dark");
    } else {
      root.classList.add("dark");
    }
  };

  const setTheme = (mode: ThemeMode) => {
    setCurrentTheme(mode);
    applyThemeStyles(mode);
    if (typeof window !== "undefined") {
      localStorage.setItem(THEME_STORAGE_KEY, mode);
    }
  };

  // Dynamically adapt theme based on user questionnaire answers
  const applyAnswerTheme = (favoriteColors: string[], visionText: string) => {
    const colorsLower = favoriteColors.map((c) => c.toLowerCase()).join(" ");
    const textLower = visionText.toLowerCase();

    let targetTheme: ThemeMode = "midnight-cosmic";

    if (colorsLower.includes("blush") && (textLower.includes("fire") || textLower.includes("phoenix") || textLower.includes("courage") || textLower.includes("transform"))) {
      targetTheme = "ember-fire";
    } else if (colorsLower.includes("blue") || colorsLower.includes("water") || textLower.includes("ocean") || textLower.includes("stillness") || textLower.includes("calm")) {
      targetTheme = "abyssal-water";
    } else if (colorsLower.includes("peach") || colorsLower.includes("champagne") || textLower.includes("nature") || textLower.includes("grow") || textLower.includes("health")) {
      targetTheme = "forest-earth";
    } else if (colorsLower.includes("lavender") || textLower.includes("freedom") || textLower.includes("curious") || textLower.includes("space")) {
      targetTheme = "twilight-air";
    }

    setTheme(targetTheme);
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        themeColors: THEME_PALETTES[theme] || THEME_PALETTES["midnight-cosmic"],
        setTheme,
        applyAnswerTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider");
  }
  return context;
}
