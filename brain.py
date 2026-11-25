"""
Hero Dialogue Brain: 7-Stage Ceremonial Dialogue Engine
Implements the exact Manifest 2027 Master System Prompt with:
- 7 Ceremonial Stages
- Real-time Interruption (Barge-in) Handling
- Vague Answer Gentle Elicitation
- Zero-drift Exact Close Statement
"""
from typing import Dict, List, Any, Optional
from config import CEREMONIAL_CLOSE_STATEMENT

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
        """
        Initialize the Hero Brain with user context.
        context keys:
            - user_name: str
            - preferred_language: str
            - pride2026: str
            - pride2027: str
            - dayInTheLife2027: str
            - movieScene: str
            - coreQualities: list of str
            - pastGroundingStory: str
            - characterNameIdea: str
        """
        self.context = context or {}
        self.user_name = self.context.get("user_name", "friend")
        self.current_stage = 1
        self.history: List[Dict[str, str]] = []
        self.is_finished = False

    def reset(self):
        """Reset conversation state."""
        self.current_stage = 1
        self.history = []
        self.is_finished = False

    def process_turn(self, user_message: str = "", was_interrupted: bool = False) -> Dict[str, Any]:
        """
        Process a conversation turn based on user input, current stage, and barge-in state.
        Returns:
            {
                "hero_response": str,
                "current_stage": int,
                "stage_name": str,
                "is_finished": bool,
                "was_interrupted": bool
            }
        """
        user_msg_clean = user_message.strip()
        user_msg_lower = user_msg_clean.lower()

        if user_msg_clean:
            self.history.append({"speaker": "user", "text": user_msg_clean})

        # Interruption / Barge-in acknowledgment
        prefix = ""
        if was_interrupted:
            acknowledgments = ["Got you. ", "Understood. ", "I hear you. "]
            prefix = acknowledgments[len(self.history) % len(acknowledgments)]

        # Check for brief / vague responses
        is_brief = len(user_msg_lower) > 0 and len(user_msg_lower) < 10 and not any(
            w in user_msg_lower for w in ["yes", "no", "ready", "okay", "sure"]
        )

        hero_response = ""
        next_stage = self.current_stage

        if self.current_stage == 1:
            # Stage 1: OPEN
            hero_response = (
                f"Welcome, {self.user_name}. A few minutes to dream out loud about your 2027. "
                "We are here as a mirror of your own potential. "
                "Tell us, what is the one thing from 2026 you're really proud of?"
            )
            next_stage = 2

        elif self.current_stage == 2:
            # Stage 2: PRIDE 2026 (Savouring)
            if not user_msg_clean and self.context.get("pride2026"):
                hero_response = (
                    f"{prefix}Looking at what you noted about 2026—\"{self.context['pride2026']}\"—"
                    "let yourself really savour that. What did that feat teach you about your strength?"
                )
            elif is_brief:
                hero_response = (
                    f"{prefix}Even a quiet moment counts. Take a breath with us. "
                    "What is one thing, big or quiet, that you did in 2026 that made you feel proud?"
                )
            else:
                hero_response = (
                    f"{prefix}Let yourself really feel that. That took genuine diligence. "
                    "Now, let's step across the threshold into 2027. "
                    "What do you want to be deeply proud of in 2027?"
                )
                next_stage = 3

        elif self.current_stage == 3:
            # Stage 3: THE 2027 PRIDE (Audacity gap & Day in the life)
            if is_brief:
                hero_response = (
                    f"{prefix}Don't hold back on the audacity. "
                    "If nothing held you back, what does that 2027 victory feel like?"
                )
            else:
                hero_response = (
                    f"{prefix}And the version of you who has already won that... "
                    "what does their morning look like? What are they doing when the sun comes up?"
                )
                next_stage = 4

        elif self.current_stage == 4:
            # Stage 4: THE CHARACTER AS A SCENE (Movie Scene & Naming)
            char_idea = self.context.get("characterNameIdea")
            if not char_idea and "creator" not in user_msg_lower and "builder" not in user_msg_lower:
                hero_response = (
                    f"{prefix}Picture your 2027 like a movie. Which scene do you love most? "
                    "What are you doing with your hands, and what do others see in your eyes? "
                    "Let's name this character together."
                )
            else:
                char_name = char_idea or "The Sovereign Creator"
                hero_response = (
                    f"{prefix}That scene is so vivid. We see you as {char_name}. "
                    "How does that name feel when you speak it out loud?"
                )
            next_stage = 5

        elif self.current_stage == 5:
            # Stage 5: GROUNDING (Real past story of diligence)
            past_story = self.context.get("pastGroundingStory")
            if past_story and not user_msg_clean:
                hero_response = (
                    f"{prefix}When you look back at when you pulled off \"{past_story}\", "
                    "when have you already been this person, even for a moment?"
                )
            else:
                hero_response = (
                    f"{prefix}When have you already been this person in your own life? "
                    "Give us one real story where you showed that same courage or diligence."
                )
            next_stage = 6

        elif self.current_stage == 6:
            # Stage 6: MIRROR (Summary of Idea, Character & Evidence + Intentional Pause)
            qualities = self.context.get("coreQualities") or ["quiet intuition", "resilience", "unwavering focus"]
            qualities_str = ", ".join(qualities[:3])
            hero_response = (
                f"{prefix}So this is someone you already are. "
                "The character who lives your 2027 isn't an imaginary stranger. "
                f"You already carry that {qualities_str} in your bones. "
                "Look at what you've walked through to get here."
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
            "was_interrupted": was_interrupted
        }
