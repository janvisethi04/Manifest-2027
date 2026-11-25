"""
Comprehensive Emotion & Sentiment Context Awareness Engine for Manifest 2027
Covers 15 Deep Human Emotional States:
1.  VULNERABLE_TENDER       - Raw openness, exposed, fragile truth
2.  GRIEF_LOSS_REGRET       - Heartbreak, mourning, lost opportunities, pain
3.  OVERWHELMED_BURNOUT     - Exhaustion, depleted, sensory overload
4.  FRUSTRATION_ANGER       - Resentment, blocked fire, feeling trapped, boundary defense
5.  IMPOSTOR_SHAME          - Self-criticism, unworthiness, feeling like a fraud
6.  LONELINESS_ISOLATION    - Solitary struggle, feeling unseen or misunderstood
7.  SKEPTICAL_GUARDED       - Cynicism, doubt, protective hesitation
8.  CONFUSED_CROSSROADS     - Mental fog, indecision, split paths
9.  HOPEFUL_YEARNING        - Tender longing, wanting better, quiet wish
10. DETERMINED_GRIT         - Relentless perseverance, stubborn fight, endurance
11. PROUD_ACCOMPLISHED      - Earned pride, diligence, honoured milestones
12. AUDACIOUS_SOVEREIGN     - Boldness, regal command, unbounded vision
13. EUPHORIC_PLAYFUL        - Joy, lightheartedness, exuberance, laughter
14. GRATITUDE_REVERENCE     - Deep thankfulness, sacred awe, humbled blessing
15. PEACEFUL_GROUNDED       - Stillness, morning serenity, unhurried ease
"""
import re
from typing import Dict, Any, List

# 15 Emotion Constants
EMOTION_VULNERABLE = "vulnerable_tender"
EMOTION_GRIEF = "grief_loss_regret"
EMOTION_OVERWHELMED = "overwhelmed_burnout"
EMOTION_FRUSTRATION = "frustration_anger"
EMOTION_IMPOSTOR = "impostor_shame"
EMOTION_LONELINESS = "loneliness_isolation"
EMOTION_SKEPTICAL = "skeptical_guarded"
EMOTION_CONFUSED = "confused_crossroads"
EMOTION_HOPEFUL = "hopeful_yearning"
EMOTION_DETERMINED = "determined_grit"
EMOTION_PROUD = "proud_accomplished"
EMOTION_AUDACIOUS = "audacious_sovereign"
EMOTION_EUPHORIC = "euphoric_playful"
EMOTION_GRATITUDE = "gratitude_reverence"
EMOTION_GROUNDED = "peaceful_grounded"
EMOTION_NEUTRAL = "neutral_reflective"

# Rich Multilingual & Conversational Markers
LEXICON = {
    EMOTION_VULNERABLE: [
        "vulnerable", "scared", "afraid", "nervous", "shy", "exposed", "soft", 
        "hesitant", "scary", "dar lag raha", "frightened", "trembling", "naked truth"
    ],
    EMOTION_GRIEF: [
        "grief", "loss", "lost", "heartbroken", "heartbreak", "cried", "crying", "tears",
        "regret", "mourning", "passed away", "miss them", "hurts", "pain", "sad", "sadness",
        "shattered", "broke my heart", "broke up", "breakup", "dard", "khona"
    ],
    EMOTION_OVERWHELMED: [
        "overwhelmed", "exhausted", "burnout", "burned out", "tired", "too much", "drowning",
        "suffocating", "pressure", "stress", "stressed", "hectic", "no energy", "depleted",
        "running on fumes", "can't take it", "thak gaya", "pareshan"
    ],
    EMOTION_FRUSTRATION: [
        "angry", "frustrated", "annoyed", "pissed", "furious", "unfair", "betrayed", "betrayal",
        "stuck", "fed up", "screwed", "resent", "resentment", "sick of", "hate", "gussa"
    ],
    EMOTION_IMPOSTOR: [
        "impostor", "fraud", "unworthy", "not good enough", "fail", "failure", "insecure",
        "insecurities", "ashamed", "shame", "guilt", "guilty", "don't deserve", "fake"
    ],
    EMOTION_LONELINESS: [
        "lonely", "alone", "isolated", "nobody understands", "on my own", "solitary",
        "alienated", "no support", "akela", "tanha", "nobody cares"
    ],
    EMOTION_SKEPTICAL: [
        "skeptical", "cynical", "doubt", "doubtful", "does this work", "is this real",
        "fake manifestation", "not sure if real", "bs", "gimmick", "questioning"
    ],
    EMOTION_CONFUSED: [
        "confused", "crossroads", "don't know what i want", "lost my way", "foggy", 
        "indecisive", "dilemma", "clueless", "no idea", "directionless", "kya karu"
    ],
    EMOTION_HOPEFUL: [
        "hope", "hopeful", "wish", "wishing", "yearn", "yearning", "longing", "someday",
        "aspire", "craving", "praying", "fingers crossed", "dreaming"
    ],
    EMOTION_DETERMINED: [
        "determined", "grit", "perseverance", "fight", "won't give up", "relentless", 
        "hustle", "endure", "survived", "push through", "unstoppable", "disciplined", "diligence"
    ],
    EMOTION_PROUD: [
        "proud", "achieved", "built", "launched", "pulled off", "finally did it", 
        "milestone", "accomplished", "proud of myself", "made it happen", "victory", "pride"
    ],
    EMOTION_AUDACIOUS: [
        "audacious", "bold", "massive", "huge", "sovereign", "empire", "dominate",
        "limitless", "unapologetic", "fearless", "sovereignty", "billion", "global scale"
    ],
    EMOTION_EUPHORIC: [
        "excited", "happy", "joy", "joyful", "fun", "laugh", "laughing", "amazing",
        "thrilled", "celebrating", "ecstatic", "vibrant", "khushi"
    ],
    EMOTION_GRATITUDE: [
        "grateful", "gratitude", "thankful", "blessed", "blessing", "appreciate",
        "thank god", "deeply touched", "shukriya", "dhanyawad", "reverence"
    ],
    EMOTION_GROUNDED: [
        "peace", "peaceful", "calm", "morning", "serene", "quiet", "tea", "ocean",
        "breathe", "breath", "stillness", "unhurried", "aligned", "sukoon", "ease"
    ]
}

# Emotion Archetype Metadata (Color Aura, Voice Cadence, SSML Rate/Pitch, Guidance Cue)
PROFILES = {
    EMOTION_VULNERABLE: {
        "label": "Vulnerable & Tender",
        "color": "#c084fc",  # Soft Violet
        "polarity": -0.25,
        "voice_rate": "-8%",
        "voice_pitch": "-1Hz",
        "guidance_cue": "Hold sacred space; mirror their raw honesty as genuine courage."
    },
    EMOTION_GRIEF: {
        "label": "Grieving & Honoring Loss",
        "color": "#818cf8",  # Deep Indigo
        "polarity": -0.80,
        "voice_rate": "-12%",
        "voice_pitch": "-2Hz",
        "guidance_cue": "Never bypass their pain. Honor what was lost before speaking of 2027."
    },
    EMOTION_OVERWHELMED: {
        "label": "Overwhelmed & Burned Out",
        "color": "#38bdf8",  # Sky Blue
        "polarity": -0.65,
        "voice_rate": "-10%",
        "voice_pitch": "-2Hz",
        "guidance_cue": "Slow down dramatically. Guide them into an unhurried exhale."
    },
    EMOTION_FRUSTRATION: {
        "label": "Frustrated & Fiery",
        "color": "#ef4444",  # Crimson Fire
        "polarity": -0.40,
        "voice_rate": "-2%",
        "voice_pitch": "+0Hz",
        "guidance_cue": "Acknowledge the fire without judging. Channel that tension into sovereignty."
    },
    EMOTION_IMPOSTOR: {
        "label": "Impostor Doubt & Self-Judgement",
        "color": "#a855f7",  # Amethyst
        "polarity": -0.50,
        "voice_rate": "-6%",
        "voice_pitch": "-1Hz",
        "guidance_cue": "Ground them strictly in factual past evidence of their diligence."
    },
    EMOTION_LONELINESS: {
        "label": "Solitary & Seeking Alignment",
        "color": "#6366f1",  # Twilight Cobalt
        "polarity": -0.45,
        "voice_rate": "-6%",
        "voice_pitch": "-1Hz",
        "guidance_cue": "Remind them 'we are here as a mirror'. They are not doing this alone."
    },
    EMOTION_SKEPTICAL: {
        "label": "Skeptical & Guarded",
        "color": "#94a3b8",  # Slate Silver
        "polarity": 0.0,
        "voice_rate": "-4%",
        "voice_pitch": "+0Hz",
        "guidance_cue": "Do not argue or convince. Invite them to look only at what their hands built."
    },
    EMOTION_CONFUSED: {
        "label": "Crossroads & Seeking Clarity",
        "color": "#2dd4bf",  # Teal Cyan
        "polarity": -0.10,
        "voice_rate": "-5%",
        "voice_pitch": "+0Hz",
        "guidance_cue": "Strip away the 100 choices. Bring focus back to a single morning moment."
    },
    EMOTION_HOPEFUL: {
        "label": "Hopeful & Tender Yearning",
        "color": "#f472b6",  # Rose Quartz
        "polarity": 0.60,
        "voice_rate": "-3%",
        "voice_pitch": "+0.5Hz",
        "guidance_cue": "Protect that tender flame. Gently expand what they dare to yearn for."
    },
    EMOTION_DETERMINED: {
        "label": "Determined & Relentless Grit",
        "color": "#e11d48",  # Ruby Core
        "polarity": 0.70,
        "voice_rate": "+0%",
        "voice_pitch": "+0Hz",
        "guidance_cue": "Anchor their unyielding backbone. Reflect their battle-tested diligence."
    },
    EMOTION_PROUD: {
        "label": "Grounded Pride & Fulfillment",
        "color": "#fbbf24",  # Warm Amber Gold
        "polarity": 0.85,
        "voice_rate": "-2%",
        "voice_pitch": "+0Hz",
        "guidance_cue": "Savour the milestone completely. Do not rush past their pride."
    },
    EMOTION_AUDACIOUS: {
        "label": "Audacious & Sovereign Leader",
        "color": "#f97316",  # Solar Ember
        "polarity": 0.95,
        "voice_rate": "+3%",
        "voice_pitch": "+1Hz",
        "guidance_cue": "Match their regal resonance. Reflect the leader already commanding the room."
    },
    EMOTION_EUPHORIC: {
        "label": "Joyful & Exuberant",
        "color": "#facc15",  # Radiant Sun
        "polarity": 0.90,
        "voice_rate": "+4%",
        "voice_pitch": "+1.5Hz",
        "guidance_cue": "Celebrate their lightness and childlike vitality."
    },
    EMOTION_GRATITUDE: {
        "label": "Grateful & Sacred Awe",
        "color": "#f59e0b",  # Golden Honey
        "polarity": 0.90,
        "voice_rate": "-5%",
        "voice_pitch": "-0.5Hz",
        "guidance_cue": "Hold reverent silence. Let the grace of their thankfulness expand."
    },
    EMOTION_GROUNDED: {
        "label": "Serene & Deeply Centered",
        "color": "#34d399",  # Emerald Sage
        "polarity": 0.80,
        "voice_rate": "-6%",
        "voice_pitch": "-1Hz",
        "guidance_cue": "Keep the unhurried morning rhythm alive."
    },
    EMOTION_NEUTRAL: {
        "label": "Reflective & Introspective",
        "color": "#a78bfa",  # Celestial Lavender
        "polarity": 0.0,
        "voice_rate": "-3%",
        "voice_pitch": "+0Hz",
        "guidance_cue": "Curious and attentive. Act as a crystal clear mirror."
    }
}

# Emotion-Attuned Verbal Bridges for Conversational Agent
EMOTION_BRIDGES = {
    EMOTION_VULNERABLE: "Take a breath with us. That raw vulnerability is the truest courage. ",
    EMOTION_GRIEF: "We honor that loss and the grief you carried. What you walked through carved the depth of who you are now. ",
    EMOTION_OVERWHELMED: "Exhale slowly. Strip away the chaos and the noise for a moment. You are completely safe here. ",
    EMOTION_FRUSTRATION: "We hear that fierce fire in your voice. That anger is just your power demanding to be honored. ",
    EMOTION_IMPOSTOR: "We hear the self-doubt whispering, but look at what your own hands built. You are no stranger to this strength. ",
    EMOTION_LONELINESS: "You don't have to carry the mountain alone in this room. We are standing right here as your mirror. ",
    EMOTION_SKEPTICAL: "It's healthy to be guarded. You don't need blind belief; we only look at what your own life has proven. ",
    EMOTION_CONFUSED: "When the horizon feels foggy, we don't look a mile ahead—just at the very next breath. ",
    EMOTION_HOPEFUL: "Hold that tender hope close. Let yourself dare to want what your spirit has been whispering. ",
    EMOTION_DETERMINED: "Look at that relentless grit in your spine. Nothing could break that diligence. ",
    EMOTION_PROUD: "Let yourself truly savour that victory in your bones. That took real self-honouring. ",
    EMOTION_AUDACIOUS: "Feel that bold electric sovereignty commanding the room. ",
    EMOTION_EUPHORIC: "We celebrate that pure lightness, vitality, and joy with you. ",
    EMOTION_GRATITUDE: "Let that gratitude ripple through every cell for a quiet breath. ",
    EMOTION_GROUNDED: "Notice how tranquil and unhurried that morning peace feels. ",
    EMOTION_NEUTRAL: ""
}

class EmotionEngine:
    def __init__(self):
        self.history_emotions: List[Dict[str, Any]] = []

    def analyze(self, text: str, stage: int = 1) -> Dict[str, Any]:
        """
        Analyze user utterance across the 15-spectrum human psychological model.
        """
        clean_text = text.lower().strip()
        if not clean_text:
            profile = PROFILES[EMOTION_NEUTRAL]
            return {
                "primary_emotion": EMOTION_NEUTRAL,
                "label": "Open & Receptive",
                "polarity": 0.0,
                "intensity": "gentle",
                "color": profile["color"],
                "voice_rate": profile["voice_rate"],
                "voice_pitch": profile["voice_pitch"],
                "guidance_cue": profile["guidance_cue"],
                "stage": stage
            }

        scores = {cat: 0.0 for cat in LEXICON}

        for cat, keywords in LEXICON.items():
            for kw in keywords:
                if kw in clean_text:
                    weight = 2.0 if len(kw.split()) > 1 else 1.0
                    # Exact word boundary matching for small words
                    if len(kw) <= 4:
                        if re.search(r'\b' + re.escape(kw) + r'\b', clean_text):
                            scores[cat] += weight
                    else:
                        scores[cat] += weight

        primary = max(scores, key=scores.get)
        primary_score = scores.get(primary, 0.0)

        if primary_score == 0.0:
            primary = EMOTION_NEUTRAL

        profile = PROFILES.get(primary, PROFILES[EMOTION_NEUTRAL])

        # Intensity scoring
        if primary_score >= 3:
            intensity = "very_high"
        elif primary_score >= 2:
            intensity = "high"
        elif primary_score == 1:
            intensity = "moderate"
        else:
            intensity = "subtle"

        result = {
            "primary_emotion": primary,
            "label": profile["label"],
            "polarity": profile["polarity"],
            "intensity": intensity,
            "color": profile["color"],
            "voice_rate": profile["voice_rate"],
            "voice_pitch": profile["voice_pitch"],
            "guidance_cue": profile["guidance_cue"],
            "stage": stage
        }

        self.history_emotions.append(result)
        return result
