import React from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, Heart } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export function CallToAction() {
  return (
    <section className="py-20 md:py-28 relative overflow-hidden">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="relative p-10 sm:p-16 rounded-3xl bg-gradient-to-tr from-dream-blush/80 via-dream-lavender/70 to-dream-champagne/80 border border-white/80 shadow-dreamy-lg text-center space-y-6 overflow-hidden">
          {/* Ambient luminous glow */}
          <div className="absolute top-0 right-0 w-72 h-72 rounded-full bg-white/40 blur-2xl -z-10" />
          <div className="absolute bottom-0 left-0 w-72 h-72 rounded-full bg-dream-sky/40 blur-2xl -z-10" />

          <Badge variant="gold" className="mx-auto">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Step Across The Threshold</span>
          </Badge>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold text-dream-plum tracking-tight max-w-3xl mx-auto leading-[1.12]">
            The 2027 You Are Becoming is Waiting to Speak.
          </h2>

          <p className="text-base sm:text-lg text-dream-plum-muted max-w-2xl mx-auto font-normal leading-relaxed">
            Begin with a quiet reflection, converse with Hero in real time, and hold in your hands a vision board born not from algorithms, but from your authentic voice.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link href="/auth/register" className="w-full sm:w-auto">
              <Button size="lg" variant="primary" className="w-full sm:w-auto shadow-dreamy-lg">
                <span>Begin Your 2027 Manifestation</span>
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Link href="/auth/login" className="w-full sm:w-auto">
              <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                <span>Already Have a Sanctuary? Sign In</span>
              </Button>
            </Link>
          </div>

          <p className="text-xs text-dream-plum-muted pt-2 flex items-center justify-center gap-1.5">
            <Heart className="w-3.5 h-3.5 text-dream-rose fill-dream-rose/30" />
            <span>Private, personal, and grounded in emotional safety.</span>
          </p>
        </div>
      </div>
    </section>
  );
}
