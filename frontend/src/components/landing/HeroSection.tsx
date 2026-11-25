import React from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, Mic, Calendar, Compass, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

export function HeroSection() {
  return (
    <section className="relative pt-12 pb-20 md:pt-20 md:pb-32 overflow-hidden">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          {/* Left Column: Heading, Value Prop, CTA */}
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            <div className="inline-flex items-center gap-2">
              <Badge variant="gold" className="shadow-sm">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Manifest 2027 Experience</span>
              </Badge>
              <Badge variant="lavender" className="hidden sm:inline-flex">
                <Mic className="w-3.5 h-3.5" />
                <span>ElevenLabs Hero Voice</span>
              </Badge>
            </div>

            <h1 className="font-serif text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-dream-plum leading-[1.08]">
              Speak Your <span className="italic font-normal bg-gradient-to-r from-dream-rose via-dream-plum to-dream-plum-light bg-clip-text text-transparent">2027 Future</span> Into Reality.
            </h1>

            <p className="text-lg sm:text-xl text-dream-plum-muted max-w-2xl mx-auto lg:mx-0 font-normal leading-relaxed">
              Step into an intimate sanctuary where you converse with <span className="font-medium text-dream-plum">Hero</span>, your real-time AI voice companion. Together, uncover your character archetype, crystallize your vision, and receive a bespoke celestial manifestation board.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <Link href="/auth/register" className="w-full sm:w-auto">
                <Button size="lg" variant="primary" className="w-full sm:w-auto shadow-dreamy-lg">
                  <span>Begin Your Manifestation</span>
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
              <Link href="#journey" className="w-full sm:w-auto">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  <Compass className="w-4 h-4 mr-2" />
                  <span>How It Works</span>
                </Button>
              </Link>
            </div>

            {/* Key Trust Signals */}
            <div className="grid grid-cols-3 gap-4 pt-6 border-t border-dream-lavender/40 text-left max-w-lg mx-auto lg:mx-0">
              <div className="space-y-1">
                <span className="font-serif text-xl sm:text-2xl font-bold text-dream-plum">100%</span>
                <p className="text-xs text-dream-plum-muted">Personalized to Your Words</p>
              </div>
              <div className="space-y-1">
                <span className="font-serif text-xl sm:text-2xl font-bold text-dream-plum">Real-Time</span>
                <p className="text-xs text-dream-plum-muted">Voice with Hero</p>
              </div>
              <div className="space-y-1">
                <span className="font-serif text-xl sm:text-2xl font-bold text-dream-plum">15-Day</span>
                <p className="text-xs text-dream-plum-muted">Manifestation Surprise</p>
              </div>
            </div>
          </div>

          {/* Right Column: Floating Aesthetic Polaroid Collage */}
          <div className="lg:col-span-5 relative flex items-center justify-center">
            <div className="relative w-full max-w-md sm:max-w-lg h-[460px] sm:h-[500px]">
              {/* Decorative background aura */}
              <div className="absolute inset-0 bg-gradient-to-tr from-dream-blush/60 via-dream-lavender/50 to-dream-champagne/60 rounded-full blur-2xl transform scale-90 -z-10" />

              {/* Card 1: Polaroid Card - The Moonlit Creator */}
              <div className="absolute top-4 left-4 sm:left-6 w-64 sm:w-72 transform -rotate-6 hover:rotate-0 transition-transform duration-500 z-20">
                <Card variant="polaroid" withTape>
                  <div className="aspect-[4/3] rounded bg-gradient-to-br from-dream-lavender via-dream-sky to-dream-peach p-4 flex flex-col justify-between overflow-hidden relative">
                    <div className="absolute inset-0 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:12px_12px] opacity-40" />
                    <div className="flex items-center justify-between relative z-10">
                      <span className="text-[10px] tracking-widest uppercase bg-white/70 px-2 py-0.5 rounded text-dream-plum font-semibold">
                        Archetype
                      </span>
                      <Sparkles className="w-4 h-4 text-[#8C6D1F]" />
                    </div>
                    <div className="relative z-10">
                      <p className="font-serif text-2xl font-bold text-dream-plum leading-tight">
                        The Moonlit Creator
                      </p>
                      <p className="text-xs text-dream-plum-light font-sans mt-0.5">
                        Element: Water • Intention: Artistry & Stillness
                      </p>
                    </div>
                  </div>
                  <div className="mt-3 text-center">
                    <p className="font-script text-lg text-dream-plum-light">
                      &quot;Where intuition guides, quiet empires bloom.&quot;
                    </p>
                  </div>
                </Card>
              </div>

              {/* Card 2: Voice Call with Hero Card */}
              <div className="absolute top-28 right-0 sm:right-2 w-64 sm:w-72 transform rotate-4 hover:rotate-0 transition-transform duration-500 z-30">
                <Card variant="default" className="bg-white/90 shadow-dreamy-lg border-dream-lavender-dark/40">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className="relative flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-tr from-dream-rose to-dream-lavender">
                        <Mic className="w-4 h-4 text-white" />
                        <span className="absolute -top-0.5 -right-0.5 flex h-2.5 w-2.5">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                        </span>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-dream-plum">Hero Companion</p>
                        <p className="text-[10px] text-emerald-600 font-medium">Listening to your 2027...</p>
                      </div>
                    </div>
                    <span className="text-[10px] bg-dream-lavender/60 text-dream-plum px-2 py-0.5 rounded-full font-mono">
                      04:18
                    </span>
                  </div>

                  {/* Pulsing Voice Orb Visualizer */}
                  <div className="h-16 rounded-xl bg-gradient-to-r from-dream-blush/40 via-dream-lavender/40 to-dream-peach/40 flex items-center justify-center gap-1.5 px-3">
                    <span className="w-1.5 h-6 bg-dream-plum rounded-full animate-pulse" style={{ animationDelay: "0ms" }} />
                    <span className="w-1.5 h-10 bg-dream-plum rounded-full animate-pulse" style={{ animationDelay: "150ms" }} />
                    <span className="w-1.5 h-14 bg-dream-plum rounded-full animate-pulse" style={{ animationDelay: "300ms" }} />
                    <span className="w-1.5 h-8 bg-dream-plum rounded-full animate-pulse" style={{ animationDelay: "450ms" }} />
                    <span className="w-1.5 h-12 bg-dream-plum rounded-full animate-pulse" style={{ animationDelay: "200ms" }} />
                    <span className="w-1.5 h-5 bg-dream-plum rounded-full animate-pulse" style={{ animationDelay: "350ms" }} />
                  </div>

                  <p className="text-[11px] text-dream-plum-muted mt-2.5 italic text-center">
                    &quot;Tell me about the feeling when you first step into that studio...&quot;
                  </p>
                </Card>
              </div>

              {/* Card 3: 2027 Vision Polaroid */}
              <div className="absolute bottom-4 left-10 sm:left-14 w-60 sm:w-64 transform -rotate-2 hover:rotate-0 transition-transform duration-500 z-10">
                <Card variant="polaroid">
                  <div className="aspect-[5/3] rounded bg-gradient-to-tr from-dream-peach via-dream-champagne to-dream-sky p-3 flex flex-col justify-between">
                    <div className="flex items-center justify-between">
                      <span className="text-[9px] uppercase tracking-wider font-semibold text-dream-plum bg-white/60 px-1.5 py-0.5 rounded">
                        2027 Vision
                      </span>
                      <Calendar className="w-3.5 h-3.5 text-dream-plum/70" />
                    </div>
                    <p className="font-serif text-lg font-bold text-dream-plum leading-snug">
                      Living between the ocean and my dream design lab.
                    </p>
                  </div>
                  <div className="mt-2 text-center">
                    <p className="font-script text-sm text-dream-plum-muted">
                      Scheduled for reality • Manifest 2027
                    </p>
                  </div>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
