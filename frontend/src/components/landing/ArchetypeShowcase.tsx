"use client";

import React, { useState } from "react";
import { Sparkles, Flame, Droplets, Mountain, Wind, Sun } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

const archetypes = [
  {
    id: "moonlit-creator",
    title: "The Moonlit Creator",
    element: "Water",
    elementIcon: Droplets,
    colorVariant: "lavender" as const,
    bgGradient: "from-dream-lavender/50 to-dream-sky/40",
    quote: "Where quiet intuition guides, lasting beauty blooms without noise.",
    qualities: ["Deep Intuition", "Quiet Mastery", "Artistic Depth", "Calm Presence"],
    rationale:
      "Assigned to those whose dreams stem from inner stillness, reflective depth, and an instinct to craft meaningful works rather than chase loud recognition.",
  },
  {
    id: "quiet-phoenix",
    title: "The Quiet Phoenix",
    element: "Fire",
    elementIcon: Flame,
    colorVariant: "blush" as const,
    bgGradient: "from-dream-blush/60 to-dream-peach/50",
    quote: "Every quiet season was only the gathering of heat for an undeniable dawn.",
    qualities: ["Resilience", "Quiet Transformation", "Courage", "Renewed Vitality"],
    rationale:
      "Assigned to those who navigated subtle rebirths in recent seasons and now step forward with sovereign inner fire and unwavering resolve for 2027.",
  },
  {
    id: "blooming-soul",
    title: "The Blooming Soul",
    element: "Earth",
    elementIcon: Mountain,
    colorVariant: "peach" as const,
    bgGradient: "from-dream-peach/50 to-dream-champagne/60",
    quote: "Rooted in devotion, the highest self expands naturally with the seasons.",
    qualities: ["Grounded Nurturing", "Generosity", "Organic Growth", "Deep Warmth"],
    rationale:
      "Assigned to those whose vision weaves personal flourishing with community care, anchored in daily rituals that nourish the body, heart, and spirit.",
  },
  {
    id: "golden-explorer",
    title: "The Golden Explorer",
    element: "Air",
    elementIcon: Wind,
    colorVariant: "gold" as const,
    bgGradient: "from-dream-champagne/60 to-dream-sky/50",
    quote: "The horizon is not a boundary, but an open invitation to expanded perception.",
    qualities: ["Boundless Curiosity", "Visionary Thinking", "Playful Freedom", "Clarity"],
    rationale:
      "Assigned to those whose aspirations cross physical, creative, and philosophical borders, driven by an appetite for wisdom and joyful adventure.",
  },
  {
    id: "fearless-builder",
    title: "The Fearless Builder",
    element: "Aether",
    elementIcon: Sun,
    colorVariant: "sky" as const,
    bgGradient: "from-dream-sky/60 to-dream-lavender/50",
    quote: "Form follows intention; what is dreamed with discipline becomes architecture.",
    qualities: ["Strategic Clarity", "Unshakeable Focus", "Architectural Grit", "Elevation"],
    rationale:
      "Assigned to those who bridge ambitious visionary ideals into tangible systems, ventures, and legacy-grade contributions.",
  },
];

export function ArchetypeShowcase() {
  const [activeArchetype, setActiveArchetype] = useState(archetypes[0]);

  return (
    <section id="archetypes" className="py-20 md:py-28 relative">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <Badge variant="champagne">Identity & Symbolic Elements</Badge>
          <h2 className="font-serif text-4xl sm:text-5xl font-bold text-dream-plum tracking-tight">
            Creative Archetypes for 2027.
          </h2>
          <p className="text-base sm:text-lg text-dream-plum-muted leading-relaxed font-normal">
            Our personalization engine assigns a memorable character archetype and symbolic element grounded solely in the qualities and dreams you express.
          </p>
        </div>

        {/* Tab Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-3 mb-10">
          {archetypes.map((arch) => {
            const Icon = arch.elementIcon;
            const isSelected = activeArchetype.id === arch.id;
            return (
              <button
                key={arch.id}
                onClick={() => setActiveArchetype(arch)}
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-all duration-300 ${
                  isSelected
                    ? "bg-dream-plum text-white shadow-dreamy scale-105"
                    : "bg-white/80 text-dream-plum hover:bg-dream-lavender/40 border border-dream-lavender/40"
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isSelected ? "text-dream-blush" : "text-dream-plum-muted"}`} />
                <span>{arch.title}</span>
              </button>
            );
          })}
        </div>

        {/* Active Archetype Detailed Showcase Card */}
        <div className="max-w-4xl mx-auto">
          <Card
            variant="default"
            className="p-8 sm:p-12 bg-white/90 shadow-dreamy-lg border-dream-lavender transition-all duration-500 overflow-hidden relative"
          >
            <div className={`absolute top-0 right-0 w-80 h-80 rounded-full bg-gradient-to-bl ${activeArchetype.bgGradient} blur-3xl -z-10`} />

            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
              <div className="md:col-span-7 space-y-4">
                <div className="flex items-center gap-2">
                  <Badge variant={activeArchetype.colorVariant}>
                    Element: {activeArchetype.element}
                  </Badge>
                  <span className="text-xs text-dream-plum-muted">Symbolic Synthesis</span>
                </div>

                <h3 className="font-serif text-3xl sm:text-4xl font-bold text-dream-plum leading-tight">
                  {activeArchetype.title}
                </h3>

                <blockquote className="font-script text-xl sm:text-2xl text-dream-plum-light border-l-2 border-dream-rose/50 pl-4 py-1 italic">
                  &quot;{activeArchetype.quote}&quot;
                </blockquote>

                <p className="text-sm text-dream-plum-muted leading-relaxed">
                  {activeArchetype.rationale}
                </p>

                <div className="pt-2">
                  <p className="text-xs font-semibold text-dream-plum uppercase tracking-wider mb-2">
                    Key Manifested Strengths
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {activeArchetype.qualities.map((q) => (
                      <span
                        key={q}
                        className="text-xs px-3 py-1 rounded-full bg-dream-lavender/40 text-dream-plum font-medium border border-dream-lavender-dark/30"
                      >
                        {q}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Decorative Artistic Seal */}
              <div className="md:col-span-5 flex items-center justify-center">
                <div className="w-48 h-48 sm:w-56 sm:h-56 rounded-full border-4 border-dashed border-dream-lavender flex flex-col items-center justify-center p-6 bg-gradient-to-tr from-white via-dream-ivory to-dream-lavender/30 shadow-inner text-center">
                  <Sparkles className="w-8 h-8 text-[#8C6D1F] mb-2 animate-spin" style={{ animationDuration: "16s" }} />
                  <span className="font-serif text-lg font-bold text-dream-plum leading-snug">
                    {activeArchetype.title}
                  </span>
                  <span className="text-[11px] text-dream-plum-muted uppercase tracking-widest mt-1">
                    Element {activeArchetype.element}
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
}
