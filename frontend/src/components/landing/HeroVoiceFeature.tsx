import React from "react";
import { Mic, Volume2, Sparkles, MessageSquareHeart, ShieldCheck, HeartHandshake } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export function HeroVoiceFeature() {
  return (
    <section id="hero-voice" className="py-20 md:py-28 relative bg-white/40 backdrop-blur-sm border-y border-dream-lavender/40">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: The Glowing Hero Voice Orb Interactive Showcase */}
          <div className="lg:col-span-5 flex flex-col items-center justify-center">
            <div className="relative w-72 sm:w-80 h-72 sm:h-80 flex items-center justify-center">
              {/* Layered Ethereal Glowing Halos */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-dream-blush/60 via-dream-lavender/70 to-dream-sky/60 blur-3xl animate-pulse-glow" />
              <div className="absolute inset-4 rounded-full bg-gradient-to-tr from-dream-peach/50 via-dream-lavender-dark/60 to-dream-blush-dark/50 blur-2xl animate-pulse" />

              {/* The Hero Orb Central Presence */}
              <div className="relative w-44 h-44 rounded-full bg-gradient-to-tr from-white via-dream-lavender to-dream-blush shadow-glow flex flex-col items-center justify-center p-6 border-2 border-white/80 transition-transform duration-700 hover:scale-105">
                <Sparkles className="w-8 h-8 text-dream-plum mb-2 animate-bounce" style={{ animationDuration: "3s" }} />
                <span className="font-serif text-xl font-bold text-dream-plum text-center leading-none">
                  Hero
                </span>
                <span className="text-[10px] text-dream-plum-muted uppercase tracking-widest mt-1">
                  Speaking • 2027
                </span>

                {/* Sub-orb ripples */}
                <div className="absolute -inset-3 rounded-full border border-dream-lavender-dark/40 animate-ping opacity-30" style={{ animationDuration: "3s" }} />
              </div>

              {/* Status Pill */}
              <div className="absolute -bottom-4 bg-white/90 backdrop-blur-md px-4 py-1.5 rounded-full border border-dream-lavender shadow-dreamy text-xs font-medium text-dream-plum flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span>Seven-Stage Grounded Dialogue</span>
              </div>
            </div>

            <p className="mt-8 text-center text-xs text-dream-plum-muted italic max-w-xs font-serif text-sm">
              &quot;Consider your manifestation ready. We&apos;ll come back to you within the next 15 days with a surprise.&quot;
            </p>
          </div>

          {/* Right Column: Hero Intelligence Pillars */}
          <div className="lg:col-span-7 space-y-6">
            <Badge variant="blush">Voice AI Architecture</Badge>
            <h2 className="font-serif text-4xl sm:text-5xl font-bold text-dream-plum tracking-tight leading-[1.15]">
              Meet Hero: An Emotionally Grounded Voice Sanctuary.
            </h2>
            <p className="text-base sm:text-lg text-dream-plum-muted leading-relaxed font-normal">
              Hero is powered by ElevenLabs Conversational AI, initialized with your questionnaire context, and trained on a strict seven-stage dialogue structure. Hero does not interrogate or lecture — Hero holds space, reflects your true words, and anchors your vision into tangible clarity.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <Card variant="bordered" className="p-4 bg-white/60">
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-xl bg-dream-lavender text-dream-plum">
                    <MessageSquareHeart className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-serif text-base font-bold text-dream-plum">
                      Contextual Memory
                    </h4>
                    <p className="text-xs text-dream-plum-muted mt-1 leading-relaxed">
                      Hero references your questionnaire answers organically. Never reads them off like a clinical script.
                    </p>
                  </div>
                </div>
              </Card>

              <Card variant="bordered" className="p-4 bg-white/60">
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-xl bg-dream-blush text-dream-plum">
                    <Mic className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-serif text-base font-bold text-dream-plum">
                      Natural Turn-Taking
                    </h4>
                    <p className="text-xs text-dream-plum-muted mt-1 leading-relaxed">
                      Interrupt naturally, take thoughtful pauses, and speak in English or Hinglish without robotic latency.
                    </p>
                  </div>
                </div>
              </Card>

              <Card variant="bordered" className="p-4 bg-white/60">
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-xl bg-dream-peach text-dream-plum">
                    <HeartHandshake className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-serif text-base font-bold text-dream-plum">
                      7-Stage Grounding
                    </h4>
                    <p className="text-xs text-dream-plum-muted mt-1 leading-relaxed">
                      From opening calibration and proud reflections to future scene exploration and grounded affirmations.
                    </p>
                  </div>
                </div>
              </Card>

              <Card variant="bordered" className="p-4 bg-white/60">
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-xl bg-dream-sky text-dream-plum">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-serif text-base font-bold text-dream-plum">
                      Ethical & Safe
                    </h4>
                    <p className="text-xs text-dream-plum-muted mt-1 leading-relaxed">
                      Hero never claims to be a therapist, never invents unstated facts, and prioritizes emotional safety.
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
