export type ThemeMode =
  | "midnight-cosmic"
  | "ember-fire"
  | "abyssal-water"
  | "forest-earth"
  | "twilight-air"
  | "celestial-ivory";

export interface ThemeColors {
  id: ThemeMode;
  name: string;
  element: "Cosmic" | "Fire" | "Water" | "Earth" | "Air" | "Light";
  bg: string;
  cardBg: string;
  text: string;
  textMuted: string;
  accent: string;
  glow: string;
  border: string;
}

export const THEME_PALETTES: Record<ThemeMode, ThemeColors> = {
  "midnight-cosmic": {
    id: "midnight-cosmic",
    name: "Midnight Celestial",
    element: "Cosmic",
    bg: "#0B0813",
    cardBg: "rgba(22, 17, 36, 0.85)",
    text: "#F3EFFC",
    textMuted: "#A399BA",
    accent: "#CCA456",
    glow: "rgba(167, 139, 250, 0.35)",
    border: "rgba(167, 139, 250, 0.2)",
  },
  "ember-fire": {
    id: "ember-fire",
    name: "Midnight Phoenix (Fire)",
    element: "Fire",
    bg: "#0E080C",
    cardBg: "rgba(30, 16, 25, 0.85)",
    text: "#FFF1F2",
    textMuted: "#BE9CA8",
    accent: "#F59E0B",
    glow: "rgba(244, 63, 94, 0.35)",
    border: "rgba(244, 63, 94, 0.25)",
  },
  "abyssal-water": {
    id: "abyssal-water",
    name: "Abyssal Moonlit (Water)",
    element: "Water",
    bg: "#050A14",
    cardBg: "rgba(11, 20, 38, 0.85)",
    text: "#F0F9FF",
    textMuted: "#8DA3C2",
    accent: "#38BDF8",
    glow: "rgba(56, 189, 248, 0.35)",
    border: "rgba(56, 189, 248, 0.2)",
  },
  "forest-earth": {
    id: "forest-earth",
    name: "Deep Moss & Stone (Earth)",
    element: "Earth",
    bg: "#060F09",
    cardBg: "rgba(13, 28, 18, 0.85)",
    text: "#F0FDF4",
    textMuted: "#8FA896",
    accent: "#E2CEB1",
    glow: "rgba(52, 211, 153, 0.3)",
    border: "rgba(52, 211, 153, 0.2)",
  },
  "twilight-air": {
    id: "twilight-air",
    name: "Starlight Horizon (Air)",
    element: "Air",
    bg: "#09081A",
    cardBg: "rgba(18, 16, 42, 0.85)",
    text: "#FAF5FF",
    textMuted: "#9E99C2",
    accent: "#FCD34D",
    glow: "rgba(129, 140, 248, 0.35)",
    border: "rgba(129, 140, 248, 0.22)",
  },
  "celestial-ivory": {
    id: "celestial-ivory",
    name: "Celestial Ivory (Light)",
    element: "Light",
    bg: "#FFFDF9",
    cardBg: "rgba(255, 255, 255, 0.9)",
    text: "#362544",
    textMuted: "#8A799B",
    accent: "#CCA456",
    glow: "rgba(235, 230, 250, 0.6)",
    border: "rgba(213, 203, 245, 0.4)",
  },
};
