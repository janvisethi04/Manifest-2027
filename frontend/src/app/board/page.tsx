"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Sparkles, ExternalLink, Download, Mail, Heart, RefreshCw, Star, Layers } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { loadProfile, loadQuestionnaire, synthesizeProfile } from "@/lib/storage";
import { ManifestationProfile, QuestionnaireData } from "@/types/questionnaire";

export default function BoardPage() {
  const [profile, setProfile] = useState<ManifestationProfile | null>(null);
  const [questionnaire, setQuestionnaire] = useState<QuestionnaireData | null>(null);
  const [miroStatus, setMiroStatus] = useState<{ loading: boolean; url?: string; message?: string }>({ loading: true });
  const [emailStatus, setEmailStatus] = useState<string>("");

  useEffect(() => {
    let p = loadProfile();
    const q = loadQuestionnaire();
    setQuestionnaire(q);

    if (!p && q.fullName) {
      p = synthesizeProfile(q);
    }
    setProfile(p);

    if (p) {
      // 1. Generate / Link Miro Board
      fetch("/api/miro/create-board", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(p),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            setMiroStatus({ loading: false, url: data.viewLink, message: data.message });
            
            // 2. Dispatch Email Delivery
            if (p?.userEmail) {
              fetch("/api/email/send-manifestation", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ...p, miroBoardUrl: data.viewLink }),
              })
                .then((r) => r.json())
                .then((eData) => {
                  if (eData.success) {
                    setEmailStatus(`Sent to ${p?.userEmail}`);
                  }
                })
                .catch(() => {});
            }
          }
        })
        .catch((err) => {
          setMiroStatus({ loading: false, message: "Local canvas mode active." });
        });
    }
  }, []);

  const handlePrint = () => {
    window.print();
  };

  if (!profile) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center p-4 text-center">
        <h2 className="font-serif text-2xl font-bold text-dream-plum mb-2">No Manifestation Board Found</h2>
        <p className="text-sm text-dream-plum-muted mb-6">Complete the questionnaire and speak with Hero to generate your 2027 board.</p>
        <Link href="/questionnaire">
          <Button variant="primary">Start Questionnaire</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-10 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
      {/* Top Banner & Actions */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-white/70 backdrop-blur-md p-6 rounded-3xl border border-dream-lavender/60 shadow-dreamy">
        <div className="space-y-1 text-center md:text-left">
          <div className="flex items-center justify-center md:justify-start gap-2">
            <Badge variant="gold">Manifest 2027 Sealed</Badge>
            {emailStatus && (
              <span className="text-xs text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200 flex items-center gap-1">
                <Mail className="w-3 h-3" />
                {emailStatus}
              </span>
            )}
          </div>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-dream-plum">
            {profile.userName}&apos;s 2027 Manifestation Sanctuary
          </h1>
          <p className="text-xs text-dream-plum-muted">
            Archetype: <span className="font-semibold text-dream-plum">{profile.archetype.title}</span> • Element: <span className="font-semibold text-dream-plum">{profile.archetype.element}</span>
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3">
          {miroStatus.url && (
            <a href={miroStatus.url} target="_blank" rel="noopener noreferrer">
              <Button size="sm" variant="primary" className="bg-[#4262FF] hover:bg-[#3151EE]">
                <Layers className="w-4 h-4 mr-1.5" />
                <span>Open in Miro Board</span>
                <ExternalLink className="w-3.5 h-3.5 ml-1" />
              </Button>
            </a>
          )}

          <Button size="sm" variant="secondary" onClick={handlePrint}>
            <Download className="w-4 h-4 mr-1.5" />
            <span>Export / Print</span>
          </Button>

          <Link href="/call">
            <Button size="sm" variant="ghost">
              <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
              <span>Talk to Hero Again</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* Main Vision Board Canvas */}
      <div id="manifestation-canvas" className="p-6 sm:p-12 rounded-3xl bg-dream-ivory border-2 border-dream-champagne-dark/40 shadow-dreamy-lg paper-texture space-y-8 relative overflow-hidden">
        
        {/* Subtle Celestial Pins */}
        <div className="flex items-center justify-between text-xs text-dream-plum-muted font-serif italic pb-4 border-b border-dream-champagne-dark/30">
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-[#8C6D1F]" />
            <span>Miro & Canvas Manifestation • Sovereign Anchor for 2027</span>
          </span>
          <span>Created with Hero Voice Companion</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          
          {/* Left Column (Col 7) */}
          <div className="md:col-span-7 space-y-6">
            
            {/* Main Headline Card */}
            <Card variant="default" className="bg-white/90 p-6 border-dream-lavender">
              <div className="flex items-center justify-between mb-3">
                <Badge variant="lavender">{profile.archetype.title}</Badge>
                <span className="text-[11px] font-mono text-dream-plum-muted uppercase">Core Vision 2027</span>
              </div>
              <h2 className="font-serif text-2xl sm:text-3xl font-bold text-dream-plum leading-tight">
                &quot;{profile.vision2027Headline}&quot;
              </h2>
              <p className="font-script text-xl sm:text-2xl text-dream-plum-light mt-4 pt-3 border-t border-dream-lavender/40">
                {profile.personalizedQuote}
              </p>
            </Card>

            {/* Two Polaroids Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              
              {/* Polaroid 1: The Movie Scene */}
              <Card variant="polaroid" withTape>
                <div className="aspect-[4/3] rounded bg-gradient-to-tr from-dream-lavender via-dream-sky to-dream-peach p-4 flex flex-col justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-wider bg-white/70 text-dream-plum px-2 py-0.5 rounded w-fit">
                    The Movie Scene
                  </span>
                  <p className="font-serif text-base font-bold text-dream-plum leading-snug">
                    {questionnaire?.movieScene || "Walking confidently through a bright, sunlit studio crafted by my own hands."}
                  </p>
                </div>
                <p className="font-script text-sm text-center text-dream-plum-muted mt-3">
                  Scene of Sovereign Reality • 2027
                </p>
              </Card>

              {/* Polaroid 2: Day In The Life */}
              <Card variant="polaroid" withTape>
                <div className="aspect-[4/3] rounded bg-gradient-to-tr from-dream-blush via-dream-champagne to-dream-peach p-4 flex flex-col justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-wider bg-white/70 text-dream-plum px-2 py-0.5 rounded w-fit">
                    Day in the Life
                  </span>
                  <p className="font-serif text-base font-bold text-dream-plum leading-snug">
                    {questionnaire?.dayInTheLife2027 || "Mornings of quiet tea, boundaried work, and deep joyful creative flow."}
                  </p>
                </div>
                <p className="font-script text-sm text-center text-dream-plum-muted mt-3">
                  Daily Rhythm • Element {profile.archetype.element}
                </p>
              </Card>
            </div>
          </div>

          {/* Right Column: Sticky Notes & Symbolic Seal (Col 5) */}
          <div className="md:col-span-5 space-y-6">
            
            {/* Symbolic Element Card */}
            <Card variant="bordered" className="bg-gradient-to-br from-white to-dream-sky/20 p-5">
              <div className="flex items-center gap-2 mb-2">
                <Star className="w-4 h-4 text-[#8C6D1F]" />
                <span className="font-serif text-sm font-bold uppercase tracking-wider text-dream-plum">
                  Symbolic Element: {profile.archetype.element}
                </span>
              </div>
              <p className="text-xs text-dream-plum-muted leading-relaxed">
                {profile.archetype.rationale}
              </p>
            </Card>

            {/* Sticky Note 1: 2026 Grounding Feat (Yellow Note) */}
            <div className="relative p-5 rounded-2xl bg-[#FFF9D2]/90 border border-[#EBE1A4] shadow-sm transform -rotate-1">
              <div className="washi-tape" style={{ background: "rgba(235, 225, 164, 0.7)" }} />
              <h4 className="font-serif text-sm font-bold text-dream-plum mb-1.5 uppercase tracking-wider text-[11px]">
                Grounding Proof • Who You Already Are
              </h4>
              <p className="text-xs text-dream-plum leading-relaxed">
                {profile.groundingFeat}
              </p>
            </div>

            {/* Sticky Note 2: Core Qualities (Pink Note) */}
            <div className="relative p-5 rounded-2xl bg-[#FFE4EC]/90 border border-[#F5C2D2] shadow-sm transform rotate-1">
              <h4 className="font-serif text-sm font-bold text-dream-plum mb-2 uppercase tracking-wider text-[11px]">
                Active Soul Qualities
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {profile.coreQualities.map((q) => (
                  <span key={q} className="text-xs px-2.5 py-1 rounded-full bg-white/80 text-dream-plum font-medium border border-rose-200">
                    {q}
                  </span>
                ))}
              </div>
            </div>

            {/* Affirmation Seal */}
            <Card variant="default" className="bg-white/95 text-center p-5 border-dream-blush">
              <p className="font-serif text-lg font-bold text-dream-plum">
                &quot;Consider your manifestation ready.&quot;
              </p>
              <p className="text-[11px] text-dream-plum-muted mt-1 uppercase tracking-wider font-mono">
                15-Day Reflection Milestone Scheduled
              </p>
            </Card>
          </div>
        </div>

      </div>
    </div>
  );
}
