import { QuestionnaireData, DynamicVariablesContext, ManifestationProfile } from "@/types/questionnaire";

const STORAGE_KEY = "converse_ai_manifest_2027_questionnaire";
const PROFILE_KEY = "converse_ai_manifest_2027_profile";

export const defaultQuestionnaire: QuestionnaireData = {
  fullName: "",
  email: "",
  preferredLanguage: "English / Hinglish",
  pride2026: "",
  proudAchievementDetail: "",
  pride2027: "",
  dayInTheLife2027: "",
  desiredFeelings: "",
  movieScene: "",
  characterNameIdea: "",
  coreQualities: [],
  pastGroundingStory: "",
  favoriteColors: ["Blush Pink", "Soft Lavender"],
  aestheticVibe: "Celestial Scrapbook & Polaroids",
  personalAffirmation: "",
  voiceConsent: true,
};

export function saveQuestionnaire(data: QuestionnaireData): void {
  if (typeof window !== "undefined") {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }
}

export function loadQuestionnaire(): QuestionnaireData {
  if (typeof window !== "undefined") {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      try {
        return { ...defaultQuestionnaire, ...JSON.parse(raw) };
      } catch (e) {
        console.error("Failed to parse questionnaire", e);
      }
    }
  }
  return defaultQuestionnaire;
}

export function buildDynamicVariables(q: QuestionnaireData): DynamicVariablesContext {
  const name = q.fullName.trim() || "Friend";
  const lang = q.preferredLanguage || "English / Hinglish";
  const qualities = q.coreQualities.length > 0 ? q.coreQualities.join(", ") : "Thoughtful, resilient, visionary";

  // Build compact, rich pre-call context for Hero
  const contextParts: string[] = [];
  if (q.pride2026) {
    contextParts.push(`2026 Pride: "${q.pride2026}"`);
  }
  if (q.proudAchievementDetail) {
    contextParts.push(`2026 Feat Detail: "${q.proudAchievementDetail}"`);
  }
  if (q.pride2027) {
    contextParts.push(`2027 Audacious Vision: "${q.pride2027}"`);
  }
  if (q.dayInTheLife2027) {
    contextParts.push(`2027 Day-in-the-life: "${q.dayInTheLife2027}"`);
  }
  if (q.movieScene) {
    contextParts.push(`Desired 2027 Movie Scene: "${q.movieScene}"`);
  }
  if (q.characterNameIdea) {
    contextParts.push(`Character Name Idea: "${q.characterNameIdea}"`);
  }
  if (q.pastGroundingStory) {
    contextParts.push(`Past Grounding Feat: "${q.pastGroundingStory}"`);
  }

  const preCallContext = contextParts.join(" | ") || "Ready to explore 2027 aspirations and ground the character.";

  return {
    user_name: name,
    preferred_language: lang,
    pre_call_context: preCallContext,
    user_qualities: qualities,
  };
}

export function synthesizeProfile(q: QuestionnaireData, characterFromCall?: string): ManifestationProfile {
  // Determine element & archetype based on user's vision & qualities
  const text = (q.pride2027 + " " + q.desiredFeelings + " " + q.movieScene).toLowerCase();

  let element: "Water" | "Fire" | "Earth" | "Air" | "Aether" = "Water";
  let title = "The Moonlit Creator";
  let rationale = "Grounded in quiet intuition, thoughtful depth, and sovereign artistic stillness.";

  if (text.includes("fire") || text.includes("reborn") || text.includes("rise") || text.includes("courage") || text.includes("energy") || text.includes("transform")) {
    element = "Fire";
    title = characterFromCall || q.characterNameIdea || "The Quiet Phoenix";
    rationale = "Navigating subtle rebirths with sovereign inner fire and unwavering resolve.";
  } else if (text.includes("grow") || text.includes("root") || text.includes("nurture") || text.includes("peace") || text.includes("health") || text.includes("nature")) {
    element = "Earth";
    title = characterFromCall || q.characterNameIdea || "The Blooming Soul";
    rationale = "Rooted in devotion, expanding organically through daily rituals and quiet care.";
  } else if (text.includes("build") || text.includes("lead") || text.includes("company") || text.includes("create") || text.includes("architect") || text.includes("venture")) {
    element = "Aether";
    title = characterFromCall || q.characterNameIdea || "The Fearless Builder";
    rationale = "Translating visionary ideals into enduring architecture, ventures, and elevated forms.";
  } else if (text.includes("travel") || text.includes("free") || text.includes("explore") || text.includes("air") || text.includes("adventure") || text.includes("curious")) {
    element = "Air";
    title = characterFromCall || q.characterNameIdea || "The Golden Explorer";
    rationale = "Dissolving artificial boundaries with boundless curiosity and joyful freedom.";
  } else {
    title = characterFromCall || q.characterNameIdea || "The Moonlit Creator";
  }

  // Generate personalized quote from user's stated words
  const quote = q.personalAffirmation
    ? `"${q.personalAffirmation}"`
    : q.pride2027
    ? `"Where ${q.pride2026 ? "2026 roots took hold" : "courage guided"}, 2027 becomes the open canvas for ${q.pride2027}."`
    : `"Where quiet intuition guides, lasting beauty blooms without noise."`;

  const profile: ManifestationProfile = {
    userName: q.fullName || "Friend",
    userEmail: q.email || "",
    archetype: {
      title,
      element,
      rationale,
    },
    personalizedQuote: quote,
    vision2027Headline: q.pride2027 || "Living into sovereign creative mastery and inner stillness.",
    coreQualities: q.coreQualities.length > 0 ? q.coreQualities : ["Intuitive Depth", "Resilience", "Creative Sovereignty"],
    groundingFeat: q.pastGroundingStory || q.proudAchievementDetail || "Demonstrated persistence and personal conviction in past seasons.",
    createdAt: new Date().toISOString(),
  };

  if (typeof window !== "undefined") {
    localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
  }

  return profile;
}

export function loadProfile(): ManifestationProfile | null {
  if (typeof window !== "undefined") {
    const raw = localStorage.getItem(PROFILE_KEY);
    if (raw) {
      try {
        return JSON.parse(raw);
      } catch (e) {
        console.error("Failed to parse profile", e);
      }
    }
  }
  return null;
}
