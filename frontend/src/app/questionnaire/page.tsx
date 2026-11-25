"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Sparkles, ArrowRight, ArrowLeft, CheckCircle2, Mail, User, ShieldCheck, AlertCircle, Palette } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { QuestionnaireData } from "@/types/questionnaire";
import { loadQuestionnaire, saveQuestionnaire, defaultQuestionnaire } from "@/lib/storage";
import { validateEmail, checkVagueAnswer, VagueCheckResult } from "@/lib/validation";
import { useTheme } from "@/context/ThemeContext";
import { ThemeMode } from "@/types/theme";

const availableQualities = [
  "Deep Intuition",
  "Resilience & Grit",
  "Gentle Empathy",
  "Creative Sovereignty",
  "Unshakeable Focus",
  "Strategic Vision",
  "Playful Curiosity",
  "Grounded Stillness",
  "Courageous Truth",
  "Generous Warmth",
];

const colorThemes: { name: string; themeMode: ThemeMode; bgPreview: string }[] = [
  { name: "Midnight Cosmic", themeMode: "midnight-cosmic", bgPreview: "#0B0813" },
  { name: "Midnight Phoenix (Fire)", themeMode: "ember-fire", bgPreview: "#0E080C" },
  { name: "Abyssal Moonlit (Water)", themeMode: "abyssal-water", bgPreview: "#050A14" },
  { name: "Forest Moss & Stone (Earth)", themeMode: "forest-earth", bgPreview: "#060F09" },
  { name: "Starlight Horizon (Air)", themeMode: "twilight-air", bgPreview: "#09081A" },
  { name: "Celestial Ivory (Light)", themeMode: "celestial-ivory", bgPreview: "#FFFDF9" },
];

export default function QuestionnairePage() {
  const router = useRouter();
  const { theme, setTheme, applyAnswerTheme } = useTheme();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<QuestionnaireData>(defaultQuestionnaire);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  // Vague answer feedback states
  const [vaguePride2026, setVaguePride2026] = useState<VagueCheckResult>({ isVague: false });
  const [vaguePride2027, setVaguePride2027] = useState<VagueCheckResult>({ isVague: false });

  useEffect(() => {
    const saved = loadQuestionnaire();
    setFormData(saved);
  }, []);

  const handleChange = (field: keyof QuestionnaireData, value: any) => {
    const updated = { ...formData, [field]: value };
    setFormData(updated);
    saveQuestionnaire(updated);

    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }

    // Check vague answers in real-time
    if (field === "pride2026") {
      setVaguePride2026(checkVagueAnswer(value, "pride2026"));
    } else if (field === "pride2027") {
      setVaguePride2027(checkVagueAnswer(value, "pride2027"));
    }
  };

  const toggleQuality = (quality: string) => {
    const current = formData.coreQualities || [];
    const updated = current.includes(quality)
      ? current.filter((q) => q !== quality)
      : [...current, quality];
    handleChange("coreQualities", updated);
  };

  const handleSelectTheme = (mode: ThemeMode, colorName: string) => {
    setTheme(mode);
    handleChange("favoriteColors", [colorName]);
  };

  const validateStep = (currentStep: number): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (currentStep === 1) {
      if (!formData.fullName.trim()) {
        newErrors.fullName = "Please enter your name or preferred name.";
      }
      
      // Strict Email Validation
      const emailValidation = validateEmail(formData.email);
      if (!emailValidation.isValid) {
        newErrors.email = emailValidation.error || "Please enter a valid email address.";
      }
    } else if (currentStep === 2) {
      if (!formData.pride2026.trim()) {
        newErrors.pride2026 = "Please share at least one thing from 2026 you are proud of.";
      } else if (formData.pride2026.trim().length < 5) {
        newErrors.pride2026 = "Please share a few more words so Hero can ground this milestone.";
      }
    } else if (currentStep === 3) {
      if (!formData.pride2027.trim()) {
        newErrors.pride2027 = "Please share what you want to manifest or be proud of in 2027.";
      } else if (formData.pride2027.trim().length < 5) {
        newErrors.pride2027 = "Close the audacity gap! What does your sovereign 2027 look like?";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(step)) {
      if (step < 6) {
        setStep(step + 1);
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        // Complete and proceed to APPOINTMENT BOOKING (not direct call)
        saveQuestionnaire({ ...formData, completedAt: new Date().toISOString() });
        router.push("/booking");
      }
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 max-w-3xl mx-auto space-y-6">
      {/* Header & Step Indicator */}
      <div className="text-center space-y-3">
        <Badge variant="gold" className="mx-auto">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Step {step} of 6 • Manifestation Mapping</span>
        </Badge>
        <h1 className="font-serif text-3xl sm:text-4xl font-bold" style={{ color: "var(--color-text)" }}>
          {step === 1 && "Your Coordinates & Verified Contact"}
          {step === 2 && "Savouring Your 2026"}
          {step === 3 && "Your 2027 Audacious Vision"}
          {step === 4 && "The Character & The Movie Scene"}
          {step === 5 && "Grounding & Proof of You"}
          {step === 6 && "Dynamic Theme & Appointment Lock"}
        </h1>
        <p className="text-xs sm:text-sm max-w-lg mx-auto" style={{ color: "var(--color-muted)" }}>
          {step === 1 && "Hero reads these answers before your call. Genuine email is required for your Miro board."}
          {step === 2 && "Before we project forward, we acknowledge the ground beneath your feet."}
          {step === 3 && "Close the audacity gap: what does the version of you who has already won look like?"}
          {step === 4 && "Picture your 2027 like a film. What are you doing, and what do others see?"}
          {step === 5 && "Evidence from your own life that this character is already inside you."}
          {step === 6 && "Select your dynamic theme and proceed to appointment slot booking."}
        </p>

        {/* Progress Bar */}
        <div className="w-full h-2 rounded-full overflow-hidden mt-4" style={{ background: "var(--color-border)" }}>
          <div
            className="h-full transition-all duration-500 rounded-full"
            style={{ width: `${(step / 6) * 100}%`, background: "var(--color-accent)" }}
          />
        </div>
      </div>

      {/* Main Questionnaire Card */}
      <Card variant="default" className="p-6 sm:p-10 shadow-dreamy-lg">
        
        {/* STEP 1: ABOUT YOU & STRICT EMAIL */}
        {step === 1 && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                What is your name or preferred name? *
              </label>
              <div className="relative">
                <User className="absolute left-3.5 top-3 w-4 h-4 text-purple-400" />
                <input
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => handleChange("fullName", e.target.value)}
                  placeholder="e.g. Sarah"
                  className={`w-full pl-10 pr-4 py-2.5 rounded-xl border ${
                    errors.fullName ? "border-rose-500" : ""
                  } text-sm focus:outline-none`}
                  style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: errors.fullName ? "#F43F5E" : "var(--color-border)" }}
                />
              </div>
              {errors.fullName && <p className="text-xs text-rose-400 mt-1">{errors.fullName}</p>}
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                Your Real Email Address (Strict Verification) *
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-3 w-4 h-4 text-purple-400" />
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleChange("email", e.target.value)}
                  placeholder="sarah@manifest2027.com"
                  className={`w-full pl-10 pr-4 py-2.5 rounded-xl border ${
                    errors.email ? "border-rose-500" : ""
                  } text-sm focus:outline-none`}
                  style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: errors.email ? "#F43F5E" : "var(--color-border)" }}
                />
              </div>
              <p className="text-[11px] mt-1" style={{ color: "var(--color-muted)" }}>
                Your Miro Manifestation Board, booking confirmation, and 15-day surprise are delivered here. Disposable/fake emails are rejected.
              </p>
              {errors.email && (
                <div className="flex items-center gap-1.5 text-xs text-rose-400 mt-1">
                  <AlertCircle className="w-3.5 h-3.5 flex-shrink-0" />
                  <span>{errors.email}</span>
                </div>
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                Preferred Language with Hero
              </label>
              <select
                value={formData.preferredLanguage}
                onChange={(e) => handleChange("preferredLanguage", e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              >
                <option value="English / Hinglish" style={{ background: "#161124", color: "#FFF" }}>English / Hinglish (Bilingual)</option>
                <option value="English" style={{ background: "#161124", color: "#FFF" }}>English</option>
                <option value="Hindi" style={{ background: "#161124", color: "#FFF" }}>Hindi</option>
              </select>
            </div>
          </div>
        )}

        {/* STEP 2: 2026 SAVOURING + VAGUE HELPER */}
        {step === 2 && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                What&apos;s the one thing from 2026 you&apos;re really proud of? *
              </label>
              <textarea
                rows={3}
                value={formData.pride2026}
                onChange={(e) => handleChange("pride2026", e.target.value)}
                placeholder="e.g. Taking the leap to step away from burnout, or finishing my creative thesis against all odds..."
                className={`w-full p-3.5 rounded-xl border text-sm focus:outline-none`}
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: errors.pride2026 ? "#F43F5E" : "var(--color-border)" }}
              />
              {errors.pride2026 && <p className="text-xs text-rose-400 mt-1">{errors.pride2026}</p>}

              {/* Vague Answer Guidance Box */}
              {vaguePride2026.isVague && (
                <div className="mt-3 p-3.5 rounded-xl border bg-amber-500/10 border-amber-500/30 text-xs space-y-2">
                  <p className="font-semibold text-amber-300">{vaguePride2026.message}</p>
                  <div className="flex flex-wrap gap-2">
                    {vaguePride2026.suggestions?.map((sug) => (
                      <button
                        key={sug}
                        type="button"
                        onClick={() => handleChange("pride2026", sug)}
                        className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-amber-200 text-left transition-colors"
                      >
                        + &quot;{sug}&quot;
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                Why does this milestone feel so meaningful to your soul?
              </label>
              <textarea
                rows={2}
                value={formData.proudAchievementDetail}
                onChange={(e) => handleChange("proudAchievementDetail", e.target.value)}
                placeholder="e.g. Because nobody thought I could do it quietly without compromising my peace..."
                className="w-full p-3.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              />
            </div>
          </div>
        )}

        {/* STEP 3: 2027 VISION + VAGUE HELPER */}
        {step === 3 && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                What do you want to be proud of in 2027? (Close the audacity gap) *
              </label>
              <textarea
                rows={3}
                value={formData.pride2027}
                onChange={(e) => handleChange("pride2027", e.target.value)}
                placeholder="e.g. Running my independent design studio, living by the coast, having full creative sovereignty..."
                className={`w-full p-3.5 rounded-xl border text-sm focus:outline-none`}
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: errors.pride2027 ? "#F43F5E" : "var(--color-border)" }}
              />
              {errors.pride2027 && <p className="text-xs text-rose-400 mt-1">{errors.pride2027}</p>}

              {/* Vague Answer Guidance Box */}
              {vaguePride2027.isVague && (
                <div className="mt-3 p-3.5 rounded-xl border bg-amber-500/10 border-amber-500/30 text-xs space-y-2">
                  <p className="font-semibold text-amber-300">{vaguePride2027.message}</p>
                  <div className="flex flex-wrap gap-2">
                    {vaguePride2027.suggestions?.map((sug) => (
                      <button
                        key={sug}
                        type="button"
                        onClick={() => handleChange("pride2027", sug)}
                        className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-amber-200 text-left transition-colors"
                      >
                        + &quot;{sug}&quot;
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                The version of you who has already won that — what does their day look like?
              </label>
              <textarea
                rows={2}
                value={formData.dayInTheLife2027}
                onChange={(e) => handleChange("dayInTheLife2027", e.target.value)}
                placeholder="e.g. Waking up without anxiety, sipping tea in soft morning sunlight, focusing on deep craft..."
                className="w-full p-3.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              />
            </div>
          </div>
        )}

        {/* STEP 4: MOVIE SCENE & CHARACTER */}
        {step === 4 && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                Picture your 2027 like a movie. Which scene do you love most?
              </label>
              <textarea
                rows={3}
                value={formData.movieScene}
                onChange={(e) => handleChange("movieScene", e.target.value)}
                placeholder="e.g. Walking into an airy studio filled with finished canvases, smiling at my team, knowing we built something enduring..."
                className="w-full p-3.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                If this character had an archetype name, what might it be?
              </label>
              <input
                type="text"
                value={formData.characterNameIdea || ""}
                onChange={(e) => handleChange("characterNameIdea", e.target.value)}
                placeholder="e.g. The Moonlit Creator, The Quiet Phoenix, The Sovereign Architect..."
                className="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              />
            </div>
          </div>
        )}

        {/* STEP 5: GROUNDING & EVIDENCE */}
        {step === 5 && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-2" style={{ color: "var(--color-text)" }}>
                Which qualities do you already carry in your bones? (Select 2 to 4)
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {availableQualities.map((quality) => {
                  const isSelected = formData.coreQualities.includes(quality);
                  return (
                    <button
                      key={quality}
                      type="button"
                      onClick={() => toggleQuality(quality)}
                      className={`p-2.5 rounded-xl text-xs font-medium border text-left transition-all ${
                        isSelected
                          ? "bg-purple-600 text-white border-purple-400 shadow-sm"
                          : "hover:bg-white/10"
                      }`}
                      style={!isSelected ? { background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" } : {}}
                    >
                      {quality}
                    </button>
                  );
                })}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                When have you already been this person, even for a moment? (Your Grounding Feat)
              </label>
              <textarea
                rows={3}
                value={formData.pastGroundingStory}
                onChange={(e) => handleChange("pastGroundingStory", e.target.value)}
                placeholder="e.g. When I launched our community initiative alone with zero budget and saw 100 people benefit..."
                className="w-full p-3.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              />
            </div>
          </div>
        )}

        {/* STEP 6: DYNAMIC THEME SELECTION & PROCEED TO BOOKING */}
        {step === 6 && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-2 flex items-center gap-1.5" style={{ color: "var(--color-text)" }}>
                <Palette className="w-4 h-4 text-purple-400" />
                <span>Choose Your Dynamic Sanctuary Theme (Live Preview)</span>
              </label>
              <p className="text-xs mb-3" style={{ color: "var(--color-muted)" }}>
                Click any theme to transform the entire app into your chosen atmospheric resonance:
              </p>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {colorThemes.map((ct) => {
                  const isSelected = theme === ct.themeMode;
                  return (
                    <button
                      key={ct.themeMode}
                      type="button"
                      onClick={() => handleSelectTheme(ct.themeMode, ct.name)}
                      className={`p-3 rounded-2xl border text-left transition-all flex items-center gap-2.5 ${
                        isSelected
                          ? "border-purple-400 ring-2 ring-purple-500 shadow-lg scale-102"
                          : "hover:border-purple-400/50"
                      }`}
                      style={{ background: "rgba(0,0,0,0.3)", borderColor: isSelected ? "var(--color-accent)" : "var(--color-border)" }}
                    >
                      <span className="w-5 h-5 rounded-full border border-white/30 flex-shrink-0" style={{ background: ct.bgPreview }} />
                      <span className="text-xs font-medium" style={{ color: "var(--color-text)" }}>{ct.name}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "var(--color-text)" }}>
                Personal Affirmation or Dream Motto
              </label>
              <input
                type="text"
                value={formData.personalAffirmation}
                onChange={(e) => handleChange("personalAffirmation", e.target.value)}
                placeholder="e.g. Where quiet intuition guides, lasting beauty blooms without noise."
                className="w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none"
                style={{ background: "rgba(0,0,0,0.25)", color: "var(--color-text)", borderColor: "var(--color-border)" }}
              />
            </div>

            <div className="p-4 rounded-2xl border flex items-start gap-3" style={{ background: "rgba(0,0,0,0.25)", borderColor: "var(--color-border)" }}>
              <ShieldCheck className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div className="text-xs space-y-1">
                <p className="font-semibold" style={{ color: "var(--color-text)" }}>Next: Select Dedicated Appointment Slot</p>
                <p style={{ color: "var(--color-muted)" }}>
                  You will now book an appointment date & time slot. Call does not start immediately — you lock your slot first!
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="mt-8 pt-6 border-t flex items-center justify-between" style={{ borderColor: "var(--color-border)" }}>
          {step > 1 ? (
            <Button type="button" variant="ghost" onClick={handleBack} size="sm">
              <ArrowLeft className="w-4 h-4 mr-1.5" />
              <span>Back</span>
            </Button>
          ) : (
            <div />
          )}

          <Button type="button" variant="primary" onClick={handleNext}>
            <span>{step === 6 ? "Lock In Coordinates ➔ Book Appointment Slot" : "Continue"}</span>
            <ArrowRight className="w-4 h-4 ml-1.5" />
          </Button>
        </div>
      </Card>
    </div>
  );
}
