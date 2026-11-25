"""
Emotion & Sentiment Context Awareness Engine for Manifest 2027
Analyzes:
- Emotional State (Vulnerable, Anxious, Proud, Audacious, Grounded, Neutral)
- Sentiment Polarity (-1.0 to +1.0) & Intensity
- Emotional Trajectory across the 7 ceremonial stages
- Adaptive Conversational Cadence & Voice Modulation
"""
import re
from typing import Dict, Any, List

# Core Manifestation Emotion Categories
EMOTION_VULNERABLE = "vulnerable_hesitant"
EMOTION_OVERWHELMED = "overwhelmed_anxious"
EMOTION_PROUD = "proud_accomplished"
EMOTION_AUDACIOUS = "audacious_expansive"
EMOTION_GROUNDED = "peaceful_grounded"
EMOTION_NEUTRAL = "neutral_reflective"

# Lexical Emotion Markers
LEXICON = {
    EMOTION_VULNERABLE: [
        "scared", "afraid", "doubt", "fear", "hesitant", "not sure", "idk", "maybe", 
        "impostor", "fail", "failed", "unworthy", "nervous", "shy", "vulnerable",
        "hard to say", "can i really", "insecurities", "weak", "struggle", "lonely"
    ],
    EMOTION_OVERWHELMED: [
        "overwhelmed", "exhausted", "tired", "burnout", "too much", "busy", "stress",
        "stressed", "anxiety", "anxious", "hectic", "pressure", "suffocating", "stuck",
        "drowning", "running out of time", "chaos", "racing"
    ],
    EMOTION_PROUD: [
        "proud", "achieved", "built", "launched", "finally", "pulled off", "won", 
        "accomplished", "happy", "strength", "survived", "diligence", "created", 
        "worked hard", "grateful", "success", "milestone", "made it", "helped"
    ],
    EMOTION_AUDACIOUS: [
        "audacious", "bold", "huge", "massive", "sovereign", "empire", "lead", 
        "leader", "unlimited", "dominate", "freedom", "wild", "dream", "million", 
        "global", "power", "unapologetic", "revolutionary", "fearless", "sovereignty"
    ],
    EMOTION_GROUNDED: [
        "peace", "calm", "morning", "quiet", "ocean", "nature", "breath", "breathe",
        "grounded", "tea", "sunlight", "slow", "flow", "serene", "aligned", "stillness",
        "ease", "unhurried", "content", "presence"
    ]
}

class EmotionEngine:
    def __init__(self):
        self.history_emotions: List[Dict[str, Any]] = []

    def analyze(self, text: str, stage: int = 1) -> Dict[str, Any]:
        """
        Analyze user utterance for emotional nuances, sentiment polarity, and conversational cues.
        """
        clean_text = text.lower().strip()
        if not clean_text:
            return {
                "primary_emotion": EMOTION_NEUTRAL,
                "label": "Open & Receptive",
                "polarity": 0.0,
                "intensity": "gentle",
                "color": "#8b5cf6",  # Violet
                "cadence": "reverent_pause",
                "voice_rate": "-2%",
                "guidance_cue": "Hold sacred space and invite organic reflection."
            }

        scores = {cat: 0.0 for cat in LEXICON}
        
        # Word and phrase matching
        for cat, keywords in LEXICON.items():
            for kw in keywords:
                if kw in clean_text:
                    scores[cat] += 1.5 if len(kw.split()) > 1 else 1.0

        # Sentiment polarity calculation
        pos_score = scores[EMOTION_PROUD] * 1.2 + scores[EMOTION_AUDACIOUS] * 1.3 + scores[EMOTION_GROUNDED] * 1.0
        neg_score = scores[EMOTION_VULNERABLE] * 1.2 + scores[EMOTION_OVERWHELMED] * 1.4

        total_emotional_hits = sum(scores.values())
        if total_emotional_hits > 0:
            polarity = max(-1.0, min(1.0, (pos_score - neg_score) / (pos_score + neg_score + 0.1)))
        else:
            polarity = 0.0

        # Determine dominant emotion
        primary = max(scores, key=scores.get)
        if scores[primary] == 0.0:
            primary = EMOTION_NEUTRAL

        # Emotion profile definition
        profiles = {
            EMOTION_VULNERABLE: {
                "label": "Vulnerable & Tender",
                "color": "#c084fc",  # Soft Violet
                "cadence": "deep_empathy_slow",
                "voice_rate": "-8%",
                "voice_pitch": "-1Hz",
                "guidance_cue": "Slow down speech. Offer gentle reassurance; honour their honesty as courage."
            },
            EMOTION_OVERWHELMED: {
                "label": "Overwhelmed & Seeking Peace",
                "color": "#38bdf8",  # Calming Sky Blue
                "cadence": "grounding_breath",
                "voice_rate": "-10%",
                "voice_pitch": "-2Hz",
                "guidance_cue": "Guide them to exhale. Strip complexity; remind them that 2027 begins with rest."
            },
            EMOTION_PROUD: {
                "label": "Grounded & Fulfilled",
                "color": "#fbbf24",  # Warm Amber Gold
                "cadence": "resonant_celebration",
                "voice_rate": "-2%",
                "voice_pitch": "+0Hz",
                "guidance_cue": "Help them savour the feat without rushing. Anchor that diligence into their core."
            },
            EMOTION_AUDACIOUS: {
                "label": "Audacious & Sovereign",
                "color": "#f97316",  # Solar Ember
                "cadence": "expansive_commanding",
                "voice_rate": "+3%",
                "voice_pitch": "+1Hz",
                "guidance_cue": "Match their bold resonance. Reflect the Sovereign Leader back to them."
            },
            EMOTION_GROUNDED: {
                "label": "Serene & Still",
                "color": "#34d399",  # Emerald Sage
                "cadence": "gentle_unhurried",
                "voice_rate": "-6%",
                "voice_pitch": "-1Hz",
                "guidance_cue": "Maintain the peaceful morning rhythm. Emphasize unhurried ease."
            },
            EMOTION_NEUTRAL: {
                "label": "Reflective & Introspective",
                "color": "#a78bfa",  # Celestial Lavender
                "cadence": "steady_mirror",
                "voice_rate": "-3%",
                "voice_pitch": "+0Hz",
                "guidance_cue": "Curious and attentive. Act as a crystal clear mirror."
            }
        }

        profile = profiles[primary]
        primary_score = scores.get(primary, 0.0)
        result = {
            "primary_emotion": primary,
            "label": profile["label"],
            "polarity": round(polarity, 2),
            "intensity": "high" if primary_score >= 2 else ("moderate" if primary_score == 1 else "subtle"),
            "color": profile["color"],
            "cadence": profile["cadence"],
            "voice_rate": profile["voice_rate"],
            "voice_pitch": profile.get("voice_pitch", "+0Hz"),
            "guidance_cue": profile["guidance_cue"],
            "stage": stage
        }

        self.history_emotions.append(result)
        return result
