"""
Session Emotional Arc & Trajectory Engine
Tracks the human emotional transformation across the 7 ceremonial stages:
- Historical emotional trajectory mapping
- Baseline vs Breakthrough state detection
- Stage 6 Sacred Mirror Transformation Monologue Generation
"""
from typing import Dict, Any, List, Optional

class EmotionalArcEngine:
    def __init__(self):
        self.stage_records: Dict[int, Dict[str, Any]] = {}

    def record_turn(self, stage: int, emotion_meta: Dict[str, Any], prosody_meta: Dict[str, Any], user_text: str):
        """Record emotional fingerprint for a specific ceremonial stage."""
        self.stage_records[stage] = {
            "stage": stage,
            "emotion": emotion_meta.get("primary_emotion", "neutral_reflective"),
            "emotion_label": emotion_meta.get("label", "Reflective"),
            "polarity": emotion_meta.get("polarity", 0.0),
            "color": emotion_meta.get("color", "#a78bfa"),
            "wpm": prosody_meta.get("wpm", 135.0),
            "tension_state": prosody_meta.get("tension_state", "balanced_resonance"),
            "disfluency_score": prosody_meta.get("disfluency_score", 0.0),
            "text_snippet": user_text[:60]
        }

    def get_trajectory_summary(self) -> List[Dict[str, Any]]:
        """Return chronological emotional journey for UI graph rendering."""
        return [self.stage_records[s] for s in sorted(self.stage_records.keys())]

    def generate_mirror_breakthrough_reflection(self) -> str:
        """
        Synthesize the profound emotional transformation arc for Stage 6 (The Mirror).
        Reflects how the user shifted from their initial baseline into their sovereign 2027 state.
        """
        # Baseline emotion (from stage 1 or 2)
        baseline = self.stage_records.get(2) or self.stage_records.get(1)
        # Vision emotion (from stage 3 or 4)
        vision = self.stage_records.get(3) or self.stage_records.get(4)
        # Grounding emotion (from stage 5)
        grounding = self.stage_records.get(5)

        base_label = baseline["emotion_label"] if baseline else "quiet introspection"
        vision_label = vision["emotion_label"] if vision else "bold clarity"

        if baseline and baseline["polarity"] < 0.2:
            shift_phrase = (
                f"When you first stepped into this call, we felt a quiet {base_label.lower()} in your words. "
                f"Yet as you spoke your 2027 out loud, notice how your energy rose into {vision_label.lower()}. "
            )
        else:
            shift_phrase = (
                f"From the very first moment you spoke of 2026, there was genuine depth. "
                f"And watching you step into your {vision_label.lower()} showed us who you really are. "
            )

        climax_reflection = (
            f"{shift_phrase}"
            "Listen to the certainty in your voice right now. "
            "You are not someone trying to figure it out—you are the sovereign creator who has already arrived."
        )

        return climax_reflection
