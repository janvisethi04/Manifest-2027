import React from "react";
import { FileText, CalendarClock, Sparkles, LayoutTemplate, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

const steps = [
  {
    step: "01",
    title: "Personalized Questionnaire",
    subtitle: "Map Your Starting Coordinates",
    icon: FileText,
    badge: "Reflective Onboarding",
    badgeVariant: "blush" as const,
    description:
      "Share your authentic self, the moments that make you happiest, your proudest achievements, and the feelings you want to anchor in 2027. Your answers form Hero's contextual foundation.",
    bulletPoints: [
      "About You & Preferred Name",
      "Current Strengths & Happiness Triggers",
      "2027 Aspirations & Core Feelings",
      "Visual Aesthetics & Preferred Colors",
    ],
  },
  {
    step: "02",
    title: "Appointment Booking",
    subtitle: "Claim Your Dedicated Sanctuary",
    icon: CalendarClock,
    badge: "Database-Backed Slots",
    badgeVariant: "peach" as const,
    description:
      "Select an available time slot converted cleanly to your local timezone. Our backend locks your appointment to prevent conflicts and sends an instant confirmation.",
    bulletPoints: [
      "Automatic Local Timezone Display",
      "Zero Double-Booking Guarantee",
      "Instant Calendar Confirmation",
      "Flexible Rescheduling Rules",
    ],
  },
  {
    step: "03",
    title: "Voice Call with Hero",
    subtitle: "7-Stage Real-Time Voice Conversation",
    icon: Sparkles,
    badge: "ElevenLabs Conversational AI",
    badgeVariant: "lavender" as const,
    description:
      "At your booked time, enter the voice sanctuary. Hero greets you by name, recalls your questionnaire naturally without reading it like an interview, and conducts an emotionally grounding conversation.",
    bulletPoints: [
      "Dynamic Variable Context Injection",
      "Natural Interruption & Turn-Taking",
      "Audio-Reactive Glowing Hero Orb",
      "Exact 15-Day Manifestation Promise",
    ],
  },
  {
    step: "04",
    title: "Bespoke Manifestation Board",
    subtitle: "Your Vision Synthesized into Art",
    icon: LayoutTemplate,
    badge: "Pinterest Scrapbook Aesthetic",
    badgeVariant: "gold" as const,
    description:
      "Our personalization engine distills your voice session and questionnaire into a memorable character archetype, original quote, symbolic element, and high-resolution exportable board.",
    bulletPoints: [
      "Unique Character / Archetype (e.g. Moonlit Creator)",
      "Symbolic Element (Fire, Water, Earth, Air, Aether)",
      "Curated Polaroid & Affirmation Cards",
      "High-Resolution PNG / PDF Export",
    ],
  },
];

export function JourneyTimeline() {
  return (
    <section id="journey" className="py-20 md:py-28 relative">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16 md:mb-20">
          <Badge variant="lavender">The Connected Journey</Badge>
          <h2 className="font-serif text-4xl sm:text-5xl font-bold text-dream-plum tracking-tight">
            From Inner Whisper to Celestial Reality.
          </h2>
          <p className="text-base sm:text-lg text-dream-plum-muted leading-relaxed font-normal">
            No disconnected demo screens or generic chatbot threads. Every step flows seamlessly into the next, creating a lasting emotional milestone for your 2027 life.
          </p>
        </div>

        {/* Step Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((item, idx) => {
            const Icon = item.icon;
            return (
              <Card
                key={item.step}
                variant="default"
                className="flex flex-col justify-between hover:-translate-y-1 transition-all duration-300 relative group overflow-hidden"
              >
                {/* Step watermarked number */}
                <span className="absolute top-3 right-4 font-serif text-5xl font-bold text-dream-lavender/40 select-none group-hover:text-dream-lavender-dark/40 transition-colors">
                  {item.step}
                </span>

                <div className="space-y-4 relative z-10">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-dream-lavender to-dream-blush border border-white shadow-sm">
                      <Icon className="w-6 h-6 text-dream-plum" />
                    </div>
                  </div>

                  <div>
                    <Badge variant={item.badgeVariant} className="mb-2 text-[10px]">
                      {item.badge}
                    </Badge>
                    <h3 className="font-serif text-2xl font-bold text-dream-plum leading-snug">
                      {item.title}
                    </h3>
                    <p className="text-xs text-dream-plum-light font-medium mt-0.5">
                      {item.subtitle}
                    </p>
                  </div>

                  <p className="text-xs sm:text-sm text-dream-plum-muted leading-relaxed">
                    {item.description}
                  </p>

                  <div className="pt-3 border-t border-dream-lavender/40 space-y-1.5">
                    {item.bulletPoints.map((point) => (
                      <div key={point} className="flex items-center text-xs text-dream-plum-light">
                        <span className="w-1.5 h-1.5 rounded-full bg-dream-plum-muted mr-2 flex-shrink-0" />
                        <span>{point}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
