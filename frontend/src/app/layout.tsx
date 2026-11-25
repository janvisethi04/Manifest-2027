import type { Metadata, Viewport } from "next";
import "./globals.css";
import { CelestialBackdrop } from "@/components/celestial/CelestialBackdrop";
import { Navbar } from "@/components/navigation/Navbar";
import { Footer } from "@/components/navigation/Footer";
import { ThemeProvider } from "@/context/ThemeContext";

export const metadata: Metadata = {
  title: "Converse AI – Manifest 2027 | ElevenLabs Hero Voice Sanctuary",
  description:
    "An intimate manifestation sanctuary. Reflect on your goals, speak in real time with Hero via ElevenLabs, and receive a bespoke celestial manifestation board for your 2027 reality.",
  keywords: [
    "Converse AI",
    "Manifest 2027",
    "ElevenLabs Conversational AI",
    "Hero Voice Agent",
    "Vision Board",
    "Personalized Manifestation",
    "Creative Archetypes",
  ],
  authors: [{ name: "Converse AI Team" }],
};

export const viewport: Viewport = {
  themeColor: "#0B0813",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="min-h-screen flex flex-col antialiased selection:bg-purple-900 selection:text-white">
        <ThemeProvider>
          <CelestialBackdrop />
          <Navbar />
          <main className="flex-grow">{children}</main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
