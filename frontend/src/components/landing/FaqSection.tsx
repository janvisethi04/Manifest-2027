"use client";

import React, { useState } from "react";
import { ChevronDown } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

const faqs = [
  {
    q: "Who is Hero and how does the voice conversation work?",
    a: "Hero is an emotionally intelligent voice companion powered by ElevenLabs Conversational AI. Before your call, Hero reads your personalized questionnaire. When you join at your scheduled time, Hero conducts a real-time, 7-stage conversation tailored to your aspirations, speaking with empathy, natural pauses, and human warmth in English or Hinglish.",
  },
  {
    q: "Is Hero a therapist or psychological counsellor?",
    a: "No. Hero is an imaginative, reflective manifestation companion designed for creative visioning and self-reflection. Hero never claims to be a mental health professional or therapist. If immediate distress or safety concerns arise, Hero follows strict safety protocols and points to real-world support resources.",
  },
  {
    q: "How does the appointment booking system work?",
    a: "After completing your questionnaire, you choose an available date and time slot. Our database verifies the slot in real-time, displays it in your local timezone, and locks it to prevent any double-booking. You receive an instant confirmation email and can join directly through your authenticated browser room at the booked time.",
  },
  {
    q: "How is my voice and personal data kept private?",
    a: "Your privacy is paramount. We separate your consent for real-time voice processing from optional transcript retention. If you decline transcript storage, raw conversation logs are permanently purged from the database after your manifestation profile is synthesized. We never sell or share your data.",
  },
  {
    q: "How do I receive my manifestation board?",
    a: "Immediately following your call, our personalization engine synthesizes your archetype, quote, symbolic element, and vision into a bespoke scrapbook-style board. It is saved directly to your account, exportable as high-resolution PNG or PDF, and delivered to your inbox.",
  },
  {
    q: "What is the 15-day surprise mentioned at the close of the call?",
    a: "In accordance with Hero's exact grounding statement ('Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise'), your account schedules a curated follow-up reflection milestone to reconnect you with the intentions you planted during your session.",
  },
];

export function FaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section id="faq" className="py-20 md:py-28 relative bg-white/30 backdrop-blur-sm border-t border-dream-lavender/40">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-4 mb-16">
          <Badge variant="sky">Clarity & Sanctuary</Badge>
          <h2 className="font-serif text-4xl sm:text-5xl font-bold text-dream-plum tracking-tight">
            Frequently Asked Questions.
          </h2>
          <p className="text-base sm:text-lg text-dream-plum-muted leading-relaxed font-normal">
            Everything you need to know about your Hero session, your privacy, and your 2027 manifestation board.
          </p>
        </div>

        <div className="space-y-4">
          {faqs.map((item, idx) => {
            const isOpen = openIndex === idx;
            return (
              <Card
                key={idx}
                variant="default"
                className="p-5 sm:p-6 transition-all duration-300 bg-white/80 hover:bg-white"
              >
                <button
                  onClick={() => setOpenIndex(isOpen ? null : idx)}
                  className="w-full flex items-center justify-between text-left gap-4 focus:outline-none"
                  aria-expanded={isOpen}
                >
                  <span className="font-serif text-lg sm:text-xl font-bold text-dream-plum">
                    {item.q}
                  </span>
                  <div
                    className={`flex-shrink-0 w-8 h-8 rounded-full bg-dream-lavender/50 flex items-center justify-center transition-transform duration-300 ${
                      isOpen ? "rotate-180 bg-dream-lavender" : ""
                    }`}
                  >
                    <ChevronDown className="w-4 h-4 text-dream-plum" />
                  </div>
                </button>
                {isOpen && (
                  <p className="text-sm sm:text-base text-dream-plum-muted leading-relaxed mt-4 pt-4 border-t border-dream-lavender/40 animate-in fade-in duration-300">
                    {item.a}
                  </p>
                )}
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
