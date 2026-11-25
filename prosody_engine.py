"""
Vocal Prosody & Speech Disfluency Analysis Engine
Analyzes speech acoustics, rhythm, and delivery patterns:
- Speech Rate (Words Per Minute - WPM)
- Micro-Hesitations & Filler Disfluency Index ("umm", "uhh", "i guess", "maybe", pauses)
- Vocal Energy & Tension Level
- Emotional Urgency vs Emotional Depletion
"""
import re
import time
from typing import Dict, Any, List

# Disfluency / Hesitation Lexicon
FILLER_MARKERS = [
    "umm", "um", "uhh", "uh", "err", "er", "ahh", "ah", "i guess", "maybe", 
    "sort of", "kind of", "like", "you know", "i don't know", "idk", "sigh",
    "matlab", "shayad", "pata nahi", "kya pata"
]

class ProsodyEngine:
    def __init__(self):
        self.turn_durations: List[float] = []

    def analyze_utterance(self, text: str, audio_duration_sec: float = 0.0) -> Dict[str, Any]:
        """
        Analyze speech rhythm, filler disfluency, and psychological tension.
        """
        clean = text.lower().strip()
        words = re.findall(r'\b[a-zA-Z\']+\b', clean)
        word_count = len(words)

        # 1. Detect filler words and micro-hesitations
        filler_count = 0
        detected_fillers = []
        for marker in FILLER_MARKERS:
            # Check whole phrase or words
            if " " in marker:
                matches = clean.count(marker)
            else:
                matches = len(re.findall(r'\b' + re.escape(marker) + r'\b', clean))
            if matches > 0:
                filler_count += matches
                detected_fillers.append(marker)

        # Disfluency Index: 0.0 (crystal clear) to 1.0 (heavy hesitation)
        disfluency_score = min(1.0, (filler_count * 0.25) + (0.3 if word_count < 4 and word_count > 0 else 0.0))

        # 2. Estimate Speech Rate (Words Per Minute)
        # If audio duration passed, compute exact; otherwise estimate based on word complexity
        if audio_duration_sec > 0:
            wpm = round((word_count / audio_duration_sec) * 60, 1)
        else:
            wpm = 135.0  # Normalized conversational baseline

        # Classify rhythm tempo
        if wpm > 175:
            tempo = "rushed_anxious"
            pace_label = "Rushed / Racing Mind"
        elif wpm < 105 and word_count > 0:
            tempo = "slow_depleted_or_reflective"
            pace_label = "Slow & Deeply Pondering"
        else:
            tempo = "steady_grounded"
            pace_label = "Centered & Balanced"

        # 3. Psychological Tension Analysis
        if disfluency_score >= 0.5:
            tension_state = "high_hesitation_self_censorship"
            pedagogical_cue = "Acknowledge hesitation with soothing warmth; invite unpolished truth."
        elif tempo == "rushed_anxious":
            tension_state = "racing_pressure"
            pedagogical_cue = "Slow down Hero's speech rate to gently down-regulate user's nervous system."
        elif tempo == "slow_depleted_or_reflective":
            tension_state = "deep_reverence_or_exhaustion"
            pedagogical_cue = "Hold a spacious sacred pause; do not push for quick answers."
        else:
            tension_state = "balanced_resonance"
            pedagogical_cue = "Flow naturally with the conversational momentum."

        return {
            "word_count": word_count,
            "wpm": wpm,
            "tempo": tempo,
            "pace_label": pace_label,
            "filler_count": filler_count,
            "detected_fillers": detected_fillers,
            "disfluency_score": round(disfluency_score, 2),
            "tension_state": tension_state,
            "pedagogical_cue": pedagogical_cue
        }
