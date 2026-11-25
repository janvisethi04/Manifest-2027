"use client";

import React from "react";
import { HeroSection } from "@/components/landing/HeroSection";
import { JourneyTimeline } from "@/components/landing/JourneyTimeline";
import { HeroVoiceFeature } from "@/components/landing/HeroVoiceFeature";
import { ArchetypeShowcase } from "@/components/landing/ArchetypeShowcase";
import { BoardPreviewSection } from "@/components/landing/BoardPreviewSection";
import { FaqSection } from "@/components/landing/FaqSection";
import { CallToAction } from "@/components/landing/CallToAction";

export default function HomePage() {
  return (
    <div className="relative">
      <HeroSection />
      <JourneyTimeline />
      <HeroVoiceFeature />
      <ArchetypeShowcase />
      <BoardPreviewSection />
      <FaqSection />
      <CallToAction />
    </div>
  );
}
