/**
 * Validation & Input Quality Engine
 * Strict Email Verification & Vague Answer Detection
 */

// Known disposable / burner email domains
const DISPOSABLE_EMAIL_DOMAINS = new Set([
  "mailinator.com",
  "tempmail.com",
  "temp-mail.org",
  "guerrillamail.com",
  "10minutemail.com",
  "trashmail.com",
  "yopmail.com",
  "fakeinbox.com",
  "throwawaymail.com",
  "dispostable.com",
  "getnada.com",
  "mohmal.com",
  "sharklasers.com",
  "crazymailing.com",
  "maildrop.cc",
  "inboxkitten.com",
  "burnermail.io",
]);

// Obvious keyboard mash / fake prefix patterns
const GARBAGE_EMAIL_PATTERNS = [
  /^asdf/i,
  /^test@test/i,
  /^qwer/i,
  /^1234/i,
  /^abcd/i,
  /^xyz@/i,
  /^a@a/i,
  /^admin@/i,
  /^fake@/i,
  /^none@/i,
  /^noemail@/i,
];

export interface EmailValidationResult {
  isValid: boolean;
  error?: string;
}

export function validateEmail(email: string): EmailValidationResult {
  const trimmed = email.trim().toLowerCase();

  if (!trimmed) {
    return { isValid: false, error: "Email address is required." };
  }

  // Strict regex for valid email format with realistic TLD
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(trimmed)) {
    return { isValid: false, error: "Please enter a valid email format (e.g. name@domain.com)." };
  }

  const [localPart, domain] = trimmed.split("@");

  if (!localPart || localPart.length < 2) {
    return { isValid: false, error: "Email username is too short." };
  }

  // Check garbage patterns
  for (const pattern of GARBAGE_EMAIL_PATTERNS) {
    if (pattern.test(trimmed)) {
      return {
        isValid: false,
        error: "Please enter your genuine email address so your Miro board & surprise can reach you.",
      };
    }
  }

  // Check disposable domains
  if (DISPOSABLE_EMAIL_DOMAINS.has(domain)) {
    return {
      isValid: false,
      error: "Temporary / disposable emails are not supported. Please use a permanent email.",
    };
  }

  // Check domain has valid dot
  if (!domain.includes(".") || domain.endsWith(".")) {
    return { isValid: false, error: "Please provide a valid email domain (e.g. gmail.com)." };
  }

  return { isValid: true };
}

// Vague / Low-effort answer patterns
const VAGUE_KEYWORDS = new Set([
  "idk",
  "i don't know",
  "dont know",
  "dunno",
  "nothing",
  "good",
  "fine",
  "ok",
  "okay",
  "money",
  "paisa",
  "rich",
  "richer",
  "car",
  "cars",
  "house",
  "chill",
  "sleep",
  "happy",
  "success",
  "same",
  "none",
  "cool",
  "yes",
  "no",
]);

export interface VagueCheckResult {
  isVague: boolean;
  message?: string;
  suggestions?: string[];
}

export function checkVagueAnswer(text: string, contextType: "pride2026" | "pride2027" | "movieScene"): VagueCheckResult {
  const clean = text.trim().toLowerCase();

  if (!clean) {
    return { isVague: false };
  }

  // Very short or single-word answers
  if (clean.length < 8 || clean.split(/\s+/).length <= 2) {
    if (VAGUE_KEYWORDS.has(clean) || clean.length < 6) {
      if (contextType === "pride2026") {
        return {
          isVague: true,
          message: "A little more detail helps Hero hold space for your true story:",
          suggestions: [
            "Overcoming personal burnout and finding peace",
            "Launching an independent project against the odds",
            "Learning to say no and protecting my creative energy",
          ],
        };
      } else if (contextType === "pride2027") {
        return {
          isVague: true,
          message: "Close the audacity gap! What does that look like in daily reality?",
          suggestions: [
            "Leading my own studio with creative freedom and quiet coastal mornings",
            "Publishing my first book and speaking to communities who care",
            "Financial sovereignty without sacrificing my inner peace and health",
          ],
        };
      } else {
        return {
          isVague: true,
          message: "Picture it like a cinema screen. What are you doing with your hands?",
          suggestions: [
            "Drafting blueprints in an airy sunlight-filled studio",
            "Walking onto a stage, holding the mic, smiling at familiar faces",
            "Sitting on a quiet porch at sunset, sipping tea, feeling unhurried",
          ],
        };
      }
    }
  }

  return { isVague: false };
}
