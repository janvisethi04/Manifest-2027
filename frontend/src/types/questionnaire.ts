export interface QuestionnaireData {
  // Identity
  fullName: string;
  email: string;
  preferredLanguage: string;

  // 2026 Savouring
  pride2026: string;
  proudAchievementDetail: string;

  // 2027 Audacity & Vision
  pride2027: string;
  dayInTheLife2027: string;
  desiredFeelings: string;

  // Movie Scene & Character
  movieScene: string;
  characterNameIdea?: string;

  // Grounding & Qualities
  coreQualities: string[];
  pastGroundingStory: string;

  // Board Aesthetic
  favoriteColors: string[];
  aestheticVibe: string;
  personalAffirmation: string;

  // Consent
  voiceConsent: boolean;
  completedAt?: string;
}

export interface ManifestationProfile {
  userName: string;
  userEmail: string;
  archetype: {
    title: string;
    element: "Water" | "Fire" | "Earth" | "Air" | "Aether";
    rationale: string;
  };
  personalizedQuote: string;
  vision2027Headline: string;
  coreQualities: string[];
  groundingFeat: string;
  miroBoardUrl?: string;
  miroBoardId?: string;
  createdAt: string;
}

export interface DynamicVariablesContext {
  [key: string]: string | number | boolean;
  user_name: string;
  preferred_language: string;
  pre_call_context: string;
  user_qualities: string;
}
