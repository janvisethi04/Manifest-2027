import React from "react";
import { Sparkles, Heart, Compass, Star, Calendar, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export function BoardPreviewSection() {
  return (
    <section id="board" className="py-20 md:py-28 relative">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <Badge variant="gold">Bespoke Scrapbook Canvas</Badge>
          <h2 className="font-serif text-4xl sm:text-5xl font-bold text-dream-plum tracking-tight">
            Your 2027 Manifestation Board.
          </h2>
          <p className="text-base sm:text-lg text-dream-plum-muted leading-relaxed font-normal">
            Every user receives a dedicated, high-resolution vision board synthesized from their voice session. Not a generic template — an intimate collage of your specific aspirations.
          </p>
        </div>

        {/* Board Canvas Preview Container */}
        <div className="max-w-5xl mx-auto p-4 sm:p-8 rounded-3xl bg-dream-ivory border border-dream-champagne-dark/40 shadow-dreamy-lg paper-texture relative overflow-hidden">
          {/* Subtle celestial pin decorations */}
          <div className="absolute top-4 left-6 flex items-center gap-2 text-dream-plum-muted text-xs font-serif italic">
            <Sparkles className="w-4 h-4 text-[#8C6D1F]" />
            <span>Curated Manifestation • Sarah&apos;s 2027 Sanctuary</span>
          </div>

          <div className="pt-8 grid grid-cols-1 md:grid-cols-12 gap-6">
            {/* Top Left: Main Headline & Archetype Banner */}
            <div className="md:col-span-7 space-y-4">
              <Card variant="default" className="bg-white/80 border-dream-lavender/50">
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="lavender">The Moonlit Creator</Badge>
                  <span className="text-xs text-dream-plum-muted font-mono">2027 Anchor</span>
                </div>
                <h3 className="font-serif text-2xl sm:text-3xl font-bold text-dream-plum leading-tight">
                  &quot;I am stepping into sovereign creative freedom, designing a life of quiet depth and intentional pace.&quot;
                </h3>
                <p className="font-script text-xl text-dream-plum-light mt-2">
                  Personal Quote: &quot;Where intuition guides, quiet empires bloom.&quot;
                </p>
              </Card>

              {/* Middle Row: Two Polaroid Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Card variant="polaroid" withTape>
                  <div className="aspect-[4/3] rounded bg-gradient-to-tr from-dream-lavender via-dream-sky to-dream-peach p-3 flex flex-col justify-between">
                    <span className="text-[10px] uppercase font-bold tracking-wider text-dream-plum bg-white/70 px-2 py-0.5 rounded w-fit">
                      Creative Studio
                    </span>
                    <p className="font-serif text-base font-bold text-dream-plum leading-snug">
                      Sunlight across drafting tables and quiet mornings of focus.
                    </p>
                  </div>
                  <p className="font-script text-sm text-center text-dream-plum-muted mt-2">
                    Daily Sanctuary 2027
                  </p>
                </Card>

                <Card variant="polaroid" withTape>
                  <div className="aspect-[4/3] rounded bg-gradient-to-tr from-dream-blush via-dream-champagne to-dream-peach p-3 flex flex-col justify-between">
                    <span className="text-[10px] uppercase font-bold tracking-wider text-dream-plum bg-white/70 px-2 py-0.5 rounded w-fit">
                      Inner Stillness
                    </span>
                    <p className="font-serif text-base font-bold text-dream-plum leading-snug">
                      Reclaiming energy, boundaried work, and joyful coastal walks.
                    </p>
                  </div>
                  <p className="font-script text-sm text-center text-dream-plum-muted mt-2">
                    Soul Rhythm • Water Element
                  </p>
                </Card>
              </div>
            </div>

            {/* Right Column: Affirmations, Qualities & Intentions */}
            <div className="md:col-span-5 space-y-4">
              {/* Symbolic Element Card */}
              <Card variant="bordered" className="bg-gradient-to-br from-white to-dream-sky/20">
                <div className="flex items-center gap-2 mb-2">
                  <Star className="w-4 h-4 text-[#8C6D1F]" />
                  <span className="font-serif text-sm font-bold uppercase tracking-wider text-dream-plum">
                    Symbolic Element: Water
                  </span>
                </div>
                <p className="text-xs text-dream-plum-muted leading-relaxed">
                  Water embodies adaptive flow, emotional depth, and silent persistence. You move past resistance by finding natural contours rather than forceful struggle.
                </p>
              </Card>

              {/* Core Qualities Sticky Note */}
              <div className="relative p-5 rounded-2xl bg-[#FFF9D2]/70 border border-[#EBE1A4] shadow-sm transform rotate-1">
                <div className="washi-tape" style={{ background: "rgba(235, 225, 164, 0.7)" }} />
                <h4 className="font-serif text-base font-bold text-dream-plum mb-2">
                  Core Qualities in Motion
                </h4>
                <ul className="text-xs text-dream-plum-light space-y-1.5 font-medium">
                  <li className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#8C6D1F]" />
                    Uncompromising Artistic Integrity
                  </li>
                  <li className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#8C6D1F]" />
                    Empathetic & Grounded Leadership
                  </li>
                  <li className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#8C6D1F]" />
                    Protective of Creative Solitude
                  </li>
                  <li className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#8C6D1F]" />
                    Courage to Release What Has Ended
                  </li>
                </ul>
              </div>

              {/* Affirmation Card */}
              <Card variant="default" className="bg-white/90 border-dream-blush/60 text-center p-4">
                <p className="font-serif text-lg font-bold text-dream-plum">
                  &quot;I am already the person who lives this vision.&quot;
                </p>
                <p className="text-[11px] text-dream-plum-muted mt-1 uppercase tracking-wider font-mono">
                  Personal Affirmation • 2027
                </p>
              </Card>
            </div>
          </div>

          {/* Bottom Action Bar */}
          <div className="mt-8 pt-6 border-t border-dream-champagne-dark/30 flex flex-col sm:flex-row items-center justify-between gap-4">
            <span className="text-xs text-dream-plum-muted italic">
              Editable in your account • Exportable as 300 DPI PNG & PDF
            </span>
            <Link href="/auth/register">
              <Button size="sm" variant="primary">
                <span>Create Your Own Board</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
