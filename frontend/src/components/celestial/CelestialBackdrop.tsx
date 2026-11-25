import React from "react";

export function CelestialBackdrop() {
  return (
    <div
      className="fixed inset-0 pointer-events-none -z-10 overflow-hidden"
      aria-hidden="true"
    >
      {/* Radiant ambient glow spheres */}
      <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-dream-blush/40 blur-3xl animate-pulse-glow" />
      <div className="absolute top-1/4 -right-32 w-[30rem] h-[30rem] rounded-full bg-dream-lavender/50 blur-3xl animate-pulse-glow" style={{ animationDelay: "2s" }} />
      <div className="absolute bottom-10 left-1/3 w-[26rem] h-[26rem] rounded-full bg-dream-sky/40 blur-3xl animate-pulse-glow" style={{ animationDelay: "4s" }} />
      <div className="absolute bottom-[-10%] right-10 w-96 h-96 rounded-full bg-dream-champagne/45 blur-3xl animate-pulse-glow" style={{ animationDelay: "1s" }} />

      {/* Floating celestial decorative SVG stars */}
      <svg
        className="absolute top-24 left-[12%] w-6 h-6 text-dream-gold/40 animate-float-slow"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5L12 0Z" />
      </svg>
      <svg
        className="absolute top-48 right-[15%] w-8 h-8 text-dream-lavender-dark/50 animate-float-reverse"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5L12 0Z" />
      </svg>
      <svg
        className="absolute top-[65%] left-[8%] w-7 h-7 text-dream-peach-dark/40 animate-float-slow"
        style={{ animationDelay: "1.5s" }}
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5L12 0Z" />
      </svg>
      <svg
        className="absolute top-[75%] right-[10%] w-5 h-5 text-dream-gold/50 animate-float-reverse"
        style={{ animationDelay: "3s" }}
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5L12 0Z" />
      </svg>
    </div>
  );
}
