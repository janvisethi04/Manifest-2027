"""
Hero Dialogue Brain: Emotion, Prosody & Emotional-Arc Aware 7-Stage Engine
Orchestrates:
- 15-Emotion Psychological Spectrum
- Vocal Prosody & Hesitation Disfluency Detection
- Session Emotional Arc & Trajectory Tracking
- Sacred Vagus Nerve Breath Regulation
- Stage 6 Emotional Transformation Mirror Climax
- Exact Ceremonial Close
"""
from typing import Dict, List, Any, Optional
from config import CEREMONIAL_CLOSE_STATEMENT
from emotion_engine import EmotionEngine, EMOTION_BRIDGES
from prosody_engine import ProsodyEngine
from emotional_arc import EmotionalArcEngine

STAGE_NAMES = {
    1: "OPEN",
    2: "PRIDE_2026",
    3: "PRIDE_2027",
    4: "MOVIE_SCENE_AND_CHARACTER",
    5: "GROUNDING",
    6: "MIRROR",
    7: "CLOSE"
}

class HeroBrain:
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        self.context = context or {}
        self.user_name = self.context.get("user_name", "friend")
        self.current_stage = 1
        self.history: List[Dict[str, str]] = []
        self.is_finished = False

        # Emotional Intelligence Subsystems
        self.emotion_engine = EmotionEngine()
        self.prosody_engine = ProsodyEngine()
        self.arc_engine = EmotionalArcEngine()

    def reset(self):
        self.current_stage = 1
        self.history = []
        self.is_finished = False
        self.emotion_engine = EmotionEngine()
        self.prosody_engine = ProsodyEngine()
        self.arc_engine = EmotionalArcEngine()

    def process_turn(
        self, 
        user_message: str = "", 
        was_interrupted: bool = False,
        audio_duration_sec: float = 0.0
    ) -> Dict[str, Any]:
        """
        Process conversation turn with full acoustic, emotional, and trajectory awareness.
        """
        user_msg_clean = user_message.strip()
        user_msg_lower = user_msg_clean.lower()

        if user_msg_clean:
            self.history.append({"speaker": "user", "text": user_msg_clean})

        # 1. Prosody & Disfluency Analysis
        prosody_meta = self.prosody_engine.analyze_utterance(user_msg_clean, audio_duration_sec=audio_duration_sec)
        
        # 2. 15-Emotion Psychological Analysis
        emotion_meta = self.emotion_engine.analyze(user_msg_clean, stage=self.current_stage)
        primary_emotion = emotion_meta["primary_emotion"]

        # 3. Record in Session Emotional Arc
        self.arc_engine.record_turn(self.current_stage, emotion_meta, prosody_meta, user_msg_clean)

        # 4. Interruption acknowledgment prefix
        prefix = ""
        if was_interrupted:
            acknowledgments = ["Got you. ", "Understood. ", "I hear you clearly. "]
            prefix = acknowledgments[len(self.history) % len(acknowledgments)]

        # 5. Hesitation & Vagus Nerve Pacing Pre-Bridge
        hesitation_bridge = ""
        if prosody_meta["disfluency_score"] >= 0.5:
            hesitation_bridge = "We felt that quiet hesitation... Take an easy breath. There is no need for a polished answer here. "
        elif prosody_meta["tempo"] == "rushed_anxious":
            hesitation_bridge = "Exhale slowly with us. We have all the time in the world. "

        # 6. Emotion Bridge
        emotion_bridge = EMOTION_BRIDGES.get(primary_emotion, "")

        is_brief = len(user_msg_lower) > 0 and len(user_msg_lower) < 10 and not any(
            w in user_msg_lower for w in ["yes", "no", "ready", "okay", "sure"]
        )

        hero_response = ""
        next_stage = self.current_stage

        if self.current_stage == 1:
            # Stage 1: OPEN
            hero_response = (
                f"Welcome, {self.user_name}. A few minutes to dream out loud about your 2027. "
                "We are here as a mirror of your own potential, holding this sacred ceremonial space for you. "
                "Tell us, what is the one thing from 2026 you're really proud of?"
            )
            next_stage = 2

        elif self.current_stage == 2:
            # Stage 2: PRIDE 2026 (Savouring & Emotional Baseline)
            if not user_msg_clean and self.context.get("pride2026"):
                hero_response = (
                    f"{prefix}Looking at what you noted about 2026—\"{self.context['pride2026']}\"—"
                    "let yourself really feel that feat. What did that experience reveal about the strength already inside you?"
                )
            elif is_brief:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}Even a quiet, unspoken moment counts. "
                    "What is one thing, big or subtle, that you did in 2026 that made your spirit feel proud?"
                )
            else:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}That took real diligence and dedication. "
                    "Now, let's step across the threshold into 2027. "
                    "What do you want to be deeply, audaciously proud of in 2027?"
                )
                next_stage = 3

        elif self.current_stage == 3:
            # Stage 3: THE 2027 PRIDE (Audacity gap & Morning visualization)
            if is_brief:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}Don't hold back on the audacity. "
                    "If nothing held you back, what does that 2027 freedom feel like?"
                )
            else:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}And the version of you who has already stepped into that victory... "
                    "what does their morning look like? What are they doing with their hands when the sun comes up?"
                )
                next_stage = 4

        elif self.current_stage == 4:
            # Stage 4: THE CHARACTER AS A SCENE (Movie Scene & Naming)
            char_idea = self.context.get("characterNameIdea")
            if not char_idea and "creator" not in user_msg_lower and "builder" not in user_msg_lower and "sovereign" not in user_msg_lower:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}Picture your 2027 like a scene in a cinematic film. "
                    "Which scene do you love most? What are you doing, and what do others see in your eyes? "
                    "Let's name this character together."
                )
            else:
                char_name = char_idea or "The Sovereign Creator"
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}That scene is so vivid and alive. We see you as {char_name}. "
                    "How does that name resonate when you speak it out loud?"
                )
            next_stage = 5

        elif self.current_stage == 5:
            # Stage 5: GROUNDING (Real past story of diligence)
            past_story = self.context.get("pastGroundingStory")
            if past_story and not user_msg_clean:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}When you look back at when you pulled off \"{past_story}\", "
                    "when have you already been this person in your own life?"
                )
            else:
                hero_response = (
                    f"{prefix}{hesitation_bridge}{emotion_bridge}When have you already embodied this person in your own life? "
                    "Give us one real story where you showed that exact diligence or courage."
                )
            next_stage = 6

        elif self.current_stage == 6:
            # Stage 6: MIRROR CLIMAX (Emotional Transformation Reflection + Sacred Pause)
            qualities = self.context.get("coreQualities") or ["quiet intuition", "resilience", "unwavering sovereignty"]
            qualities_str = ", ".join(qualities[:3])
            
            # Synthesize live journey reflection
            arc_reflection = self.arc_engine.generate_mirror_breakthrough_reflection()

            hero_response = (
                f"{prefix}{arc_reflection} "
                f"So this is someone you already are. You carry that {qualities_str} in your bones. "
                "Look at what you have walked through to stand here today."
            )
            next_stage = 7

        elif self.current_stage >= 7:
            # Stage 7: CLOSE (Exact Closing Statement)
            hero_response = CEREMONIAL_CLOSE_STATEMENT
            self.is_finished = True
            next_stage = 7

        self.current_stage = next_stage
        self.history.append({"speaker": "hero", "text": hero_response})

        return {
            "hero_response": hero_response,
            "current_stage": self.current_stage,
            "stage_name": STAGE_NAMES.get(self.current_stage, "UNKNOWN"),
            "is_finished": self.is_finished,
            "was_interrupted": was_interrupted,
            "emotion": emotion_meta,
            "prosody": prosody_meta,
            "trajectory": self.arc_engine.get_trajectory_summary()
        }
