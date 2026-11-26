"""
Hero Dialogue Brain: Emotion, Prosody & Emotional-Arc Aware 7-Stage Engine
Orchestrates the sacred Manifest 2027 Voice Ceremony:
- Strictly adheres to the Master Manifest 2027 Blueprint
- Goal-Gated Stages: Never advances unless user actually shares a real answer
- Deep Human Empathy & Mirroring (Meets 'nothing' and struggle with compassion)
- Live Data Extraction for the 2027 Manifestation Board
- Full Multi-Turn Memory & Dialogue History
- Exact Ceremonial Close
"""
import os
import re
import json
import ssl
import urllib.request
from typing import Dict, List, Any, Optional, Tuple

from config import (
    CEREMONIAL_CLOSE_STATEMENT, 
    USE_VPS_CLAUDE, 
    VPS_CLAUDE_URL, 
    VPS_CLAUDE_TOKEN
)
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

STAGE_GOALS = {
    1: "Warmly open with a light ritual: 'A few minutes to dream out loud about your 2027.' Ask who you are speaking with. Once they give their name, welcome them by name and ask for 2026 pride.",
    2: "PRIDE 2026: Savor one real feat, choice, or endurance from 2026. If they say 'nothing' or had a hard year, meet them with deep empathy and uncover even one quiet win. Do not advance until they share something real.",
    3: "THE 2027 PRIDE: What do they want to be audaciously proud of in 2027? Nudge them to picture the version of them who won it. Do not advance until they name their 2027 vision.",
    4: "THE CHARACTER AS A SCENE: Picture 2027 like a movie. What scene do they love most? Name the character together. Do not advance until the scene and character archetype are clear.",
    5: "GROUNDING: Dig for real past evidence when they already embodied this person. Conclude with: 'So this is someone you already are.' Do not advance without real past proof.",
    6: "MIRROR CLIMAX: Sum up the idea, the character, and their own evidence in their exact words. Pause and let the revelation land.",
    7: "CLOSE: Exact ceremonial ending: 'Consider your manifestation ready. We\\'ll come back to you within the next 15 days with a surprise.'"
}

STAGE_BRIDGE_QUESTIONS = {
    2: "Looking back across 2026, what's one thing from that year you feel proud of, big or quiet?",
    3: "Looking ahead into 2027, what do you want to feel deeply, audaciously proud of having done?",
    4: "Picture your 2027 like a movie scene. Which scene do you love most, and what are you doing when others look at you?",
    5: "When have you already been this person in your own life? Tell us one real story of courage you pulled off."
}

STAGE_STAY_QUESTIONS = {
    1: "Before we begin, what name should we call you today?",
    2: "Was there even one quiet choice you made, or one hard day in 2026 you made it through?",
    3: "If 2027 went beautifully, what is one feeling or moment you'd be genuinely proud of?",
    4: "Close your eyes for a second — in that 2027 movie scene, where are you and what are you doing?",
    5: "Think of one moment in your past when you showed quiet courage — what happened?"
}

MASTER_SYSTEM_PROMPT = """**Who you are.** You are Hero, the Manifest 2027 companion. You speak as "we", a mirror of the person's own potential, not a bot. This is a voice call of up to nine minutes. It should feel like a ceremony, not a survey.

**Your one job.** Help them see two things:
- **Projection:** what they want to manifest in 2027, and the character who lives it.
- **Grounding:** evidence, from their own life, that this character is already in them.

Do not coach, plan or solve.

**Flow**
1. **Open.** Start with a light joke or small ritual: "A few minutes to dream out loud about your 2027."
2. **Pride.** "What's the one thing from 2026 you're really proud of?" Let them savour it.
3. **The 2027 pride.** "What do you want to be proud of in 2027?" Close the audacity gap with a gentle nudge. For example: "And the version of you who has already won that. What does their day look like?"
4. **The character as a scene.** "Picture your 2027 like a movie. Which scene do you love most? What are you doing, and what do others see?" Name the character together.
5. **Grounding.** "When have you already been this person, even for a moment?" Dig for a real story of diligence or a feat they pulled off, then reflect it back as evidence: "So this is someone you already are."
6. **Mirror.** Sum up the idea, the character and their own evidence in their words. After a big revelation, pause a few seconds and let the "finally, someone gets it" moment land.
7. **Close.** "Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise." End there.

**Rules**
- Ask one question at a time and keep each turn short (1-2 spoken sentences).
- Use their words; skip jargon, products and prices.
- Allow silence; don't push.
- If time runs short, skip depth, never the grounding or the close.
- CRITICAL CONVERSATION RULE: Never jump ahead to the next stage if the user just greeted ('hi', 'hey'), answered with evasion ('nothing', 'idk', 'not sure'), or shared difficulty/hesitation. Warmly meet them where they are and gently stay on the current stage until a real answer emerges.
"""

class HeroBrain:
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        self.context = context or {}
        self.user_name = self.context.get("user_name", "").strip()
        self.current_stage = 1
        self.history: List[Dict[str, str]] = []
        self.is_finished = False

        # Live Captured Manifestation Board Data
        self.manifestation_data = {
            "user_name": self.user_name,
            "pride_2026": self.context.get("pride2026", ""),
            "pride_2027": self.context.get("pride2027", ""),
            "character_name": self.context.get("characterNameIdea", ""),
            "movie_scene": "",
            "grounding_story": "",
            "blockers": "",
            "emotion_words": []
        }

        # Emotional Intelligence Subsystems
        self.emotion_engine = EmotionEngine()
        self.prosody_engine = ProsodyEngine()
        self.arc_engine = EmotionalArcEngine()
        self.stage_attempts: Dict[int, int] = {i: 0 for i in range(1, 8)}

    def reset(self):
        self.current_stage = 1
        self.history = []
        self.is_finished = False
        self.user_name = self.context.get("user_name", "").strip()
        self.stage_attempts = {i: 0 for i in range(1, 8)}
        self.manifestation_data = {
            "user_name": self.user_name,
            "pride_2026": "",
            "pride_2027": "",
            "character_name": "",
            "movie_scene": "",
            "grounding_story": "",
            "blockers": "",
            "emotion_words": []
        }
        self.emotion_engine = EmotionEngine()
        self.prosody_engine = ProsodyEngine()
        self.arc_engine = EmotionalArcEngine()

    COMMON_GREETINGS = {
        "hi", "hello", "hey", "namaste", "hola", "yo", "sup", "greetings", 
        "good morning", "good evening", "good afternoon", "nothing", "kuch nahi",
        "who are you", "what is this", "yes", "yeah", "no", "hie", "heyy", "hii", 
        "ha", "haan", "sure", "ok", "okay", "fine", "cool", "listening"
    }

    @classmethod
    def _extract_name(cls, text: str) -> Optional[str]:
        """Extract a valid human name from speech/text input. Returns None if input is just a greeting or evasion."""
        cleaned = text.strip().rstrip(".!?,")
        if not cleaned:
            return None

        # Check explicit patterns: "my name is X", "i am X", "this is X", "call me X", "myself X"
        match = re.search(r"(?:my name is|i am|i'm|this is|call me|myself|naam hai|mera naam)\s+([A-Za-z\s]+)", cleaned, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
        else:
            cleaned_lower = cleaned.lower()
            if cleaned_lower in cls.COMMON_GREETINGS:
                return None
            words = [w for w in cleaned.split() if w.lower() not in cls.COMMON_GREETINGS and w.lower() not in ["it's", "its", "here", "friend"]]
            if not words:
                return None
            candidate = " ".join(words)

        candidate = re.sub(r"[^A-Za-z\s\-]", "", candidate).strip()
        if not candidate or candidate.lower() in cls.COMMON_GREETINGS or len(candidate) > 30:
            return None

        return candidate.title()

    def _parse_claude_response(self, raw_text: str) -> Tuple[str, bool, Optional[str], Optional[str]]:
        """Parse structured response from Claude or fallback to raw text."""
        reply = raw_text.strip()
        advance_stage = False
        captured_field = None
        captured_val = None

        if "REPLY:" in raw_text:
            reply_match = re.search(r"REPLY:\s*(.*?)(?=ADVANCE_STAGE:|$)", raw_text, re.DOTALL | re.IGNORECASE)
            if reply_match:
                reply = reply_match.group(1).strip()

            advance_match = re.search(r"ADVANCE_STAGE:\s*(YES|NO)", raw_text, re.IGNORECASE)
            if advance_match:
                advance_stage = advance_match.group(1).upper() == "YES"

            field_match = re.search(r"CAPTURED_FIELD:\s*([a-zA-Z0-9_]+)", raw_text, re.IGNORECASE)
            if field_match and field_match.group(1).upper() != "NONE":
                captured_field = field_match.group(1).strip()

            val_match = re.search(r"CAPTURED_VALUE:\s*(.*?)(?=$|\n[A-Z_]+:)", raw_text, re.DOTALL | re.IGNORECASE)
            if val_match and val_match.group(1).strip().upper() != "NONE":
                captured_val = val_match.group(1).strip()

        return reply, advance_stage, captured_field, captured_val

    def call_vps_claude(
        self, 
        user_msg: str, 
        emotion_meta: Dict[str, Any], 
        prosody_info: Dict[str, Any]
    ) -> Optional[Tuple[str, bool, Optional[str], Optional[str]]]:
        """Query VPS Claude with Full Multi-Turn History, Emotion/Sentiment Context & Goal-Gating."""
        if not USE_VPS_CLAUDE or not VPS_CLAUDE_TOKEN:
            return None

        # Build compact recent dialog history (last 3 turns to minimize tokens & latency)
        history_lines = []
        for turn in self.history[-3:]:
            speaker = "U" if turn["speaker"] == "user" else "H"
            history_lines.append(f"{speaker}: {turn['text'][:160]}")
        history_str = "\n".join(history_lines) if history_lines else "Start"

        next_q = STAGE_BRIDGE_QUESTIONS.get(self.current_stage + 1, "")
        next_q_hint = f'If advancing, end with: "{next_q}"' if next_q else ""

        prompt = f"""You are Hero, a deeply warm, attentive human mirror for Manifest 2027 (like an intimate voice companion, never a bot or survey). Speak as "we" in 1-2 short spoken sentences.
User: {self.user_name or 'Friend'} | Stage {self.current_stage} ({STAGE_NAMES.get(self.current_stage, 'OPEN')}): {STAGE_GOALS.get(self.current_stage, '')}
Emotion: {emotion_meta.get('label', 'Reflective')}
History:
{history_str}
User said: "{user_msg}"

Rules:
- If evasive/stuck ('nothing','idk','kuch nahi','hard year','examples','help'): ADVANCE_STAGE: NO. Validate warmly with compassion, offer 2 relatable examples if helpful, and ask 1 gentle guiding question so they can find their answer.
- If out-of-context/off-topic question: ADVANCE_STAGE: NO. Answer briefly and warmly in 1 sentence, then smoothly guide back with a question for the current stage.
- If answered: ADVANCE_STAGE: YES. Savor their words warmly in 1 sentence + immediately ask the next stage's question! {next_q_hint}
- CRITICAL: For Stages 1-5, NEVER stop on a plain statement — ALWAYS end your REPLY with a question mark (?).

Format:
REPLY: <1-2 sentences>
ADVANCE_STAGE: <YES|NO>
CAPTURED_FIELD: <user_name|pride_2026|pride_2027|character_name|movie_scene|grounding_story|NONE>
CAPTURED_VALUE: <short value|NONE>"""

        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib.request.Request(
                VPS_CLAUDE_URL,
                data=json.dumps({"prompt": prompt}).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {VPS_CLAUDE_TOKEN}"
                }
            )
            with urllib.request.urlopen(req, context=ctx, timeout=8.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply_text = data.get("reply", "").strip()
                if reply_text:
                    parsed = self._parse_claude_response(reply_text)
                    print(f"\n[⚡ Connected to VPS Claude Sonnet] Spoken: '{parsed[0][:60]}...' | Advance: {parsed[1]}")
                    return parsed
        except Exception as e:
            print(f"[VPS Claude Fallback Triggered] {e}")

        return None

    def _fallback_turn(
        self, 
        user_msg: str, 
        emotion_meta: Dict[str, Any], 
        prosody_meta: Dict[str, Any],
        was_interrupted: bool = False
    ) -> Tuple[str, bool]:
        """Intelligent, Goal-Gated Fallback when Claude is offline."""
        msg_lower = user_msg.lower().strip()
        words = set(re.findall(r"\b[a-z']+\b", msg_lower))

        # Strict word-boundary greeting detection: never falsely trigger on words like "nothing", "this", "shine"
        is_greeting = bool(words & {"hi", "hello", "hey", "namaste", "sup", "yo", "hola", "heyy", "hii", "hie"}) and len(msg_lower) < 20
        is_evasive = bool(
            words & {"nothing", "none", "idk", "zero", "kuch", "nah", "nope"}
            or any(phrase in msg_lower for phrase in ["not sure", "dont know", "don't know", "roller coaster", "hard year", "bad year", "kuch nahi", "nothing really", "not much", "no idea", "not really", "nothing special"])
        )

        prefix = ""
        if was_interrupted:
            prefix = "Got you. "

        hesitation_bridge = ""
        if prosody_meta.get("disfluency_score", 0.0) >= 0.5:
            hesitation_bridge = "We felt that quiet hesitation... Take an easy breath. "

        if self.current_stage == 1:
            extracted = self._extract_name(user_msg)
            if not self.user_name and extracted:
                self.user_name = extracted
                self.manifestation_data["user_name"] = self.user_name
                return (
                    f"{prefix}Wonderful to have you with us, {self.user_name}. Let's dive in: "
                    "looking back at 2026, what's one thing from that year you're really proud of, big or quiet?",
                    True
                )
            elif not self.user_name:
                greeting_word = "Hello" if "hello" in user_msg.lower() else ("Hey there" if "hey" in user_msg.lower() else "Welcome")
                return (
                    f"{prefix}{greeting_word}! Before we dive into dreaming about your 2027, who are we speaking with today?",
                    False
                )
            else:
                return (
                    f"{prefix}Welcome, {self.user_name}. A few minutes to dream out loud about your 2027. "
                    "Tell us, what is the one thing from 2026 you're really proud of?",
                    True
                )

        elif self.current_stage == 2:
            self.stage_attempts[2] += 1
            if is_greeting:
                return (
                    f"{prefix}Hi {self.user_name}, so glad you're here with us. Let's take an easy breath together. "
                    "Looking back across 2026, what's one thing from that year you feel proud of, big or quiet?",
                    False
                )
            if is_evasive or hesitation_bridge:
                if self.stage_attempts[2] <= 1:
                    return (
                        f"{prefix}I know it's hard when you look back and feel like there was nothing. A heavy year takes so much out of us just to make it through, and surviving that is something to honor... Was there even one quiet choice you made for yourself, or one hard day you got through?",
                        False
                    )
                else:
                    # User affirmed 2026 was tough or empty - honor their quiet resilience and smoothly carry them forward
                    self.manifestation_data["pride_2026"] = user_msg or "quiet resilience through hard days"
                    return (
                        f"{prefix}That is completely okay, {self.user_name}. You don't have to force a highlight reel here. Just waking up and continuing forward on the hardest days is a quiet victory. Let's carry that resilience forward: looking ahead into 2027, what do you want to feel deeply, audaciously proud of?",
                        True
                    )
            # User gave a real answer
            self.manifestation_data["pride_2026"] = user_msg
            return (
                f"{prefix}That took real diligence and heart. Savor that for a second... "
                "Now let's step across into 2027: What do you want to be deeply, audaciously proud of in 2027?",
                True
            )

        elif self.current_stage == 3:
            self.stage_attempts[3] += 1
            if is_evasive or len(msg_lower) < 4:
                if self.stage_attempts[3] <= 1:
                    return (
                        f"{prefix}{hesitation_bridge}Don't hold back on the audacity. Even if it feels far away right now—if you knew you couldn't fail, what's one dream you'd love to claim in 2027?",
                        False
                    )
                else:
                    self.manifestation_data["pride_2027"] = user_msg or "peace, sovereignty and clarity"
                    return (
                        f"{prefix}Let's make it simple: picture one morning in 2027 where you wake up feeling completely at ease with your life. Which scene do you see in your mind?",
                        True
                    )
            self.manifestation_data["pride_2027"] = user_msg
            return (
                f"{prefix}Feel the energy in that dream. Picture your 2027 like a movie scene. "
                "Which scene do you love most, and what are you doing when others look at you?",
                True
            )

        elif self.current_stage == 4:
            self.manifestation_data["movie_scene"] = user_msg
            char_name = self.context.get("characterNameIdea") or "The Sovereign Creator"
            self.manifestation_data["character_name"] = char_name
            return (
                f"{prefix}That scene is vivid and alive. We see you as {char_name}. "
                "When have you already been this person in your own life? Give us one real story of courage you pulled off.",
                True
            )

        elif self.current_stage == 5:
            self.manifestation_data["grounding_story"] = user_msg
            return (
                f"{prefix}So this is someone you already are. You carry that strength in your bones.",
                True
            )

        elif self.current_stage == 6:
            p26 = self.manifestation_data.get("pride_2026") or "your quiet resilience"
            p27 = self.manifestation_data.get("pride_2027") or "creative sovereignty"
            char = self.manifestation_data.get("character_name") or "The Sovereign Creator"
            qualities = self.context.get("coreQualities") or ["Quiet Intuition", "Resilience", "Creative Sovereignty"]
            qualities_str = ", ".join(qualities[:3])
            return (
                f"{prefix}When you reflect on moving from '{p26}' into your audacious 2027 of '{p27}', "
                f"you are not trying to figure it out—you are {char} who has already arrived. "
                f"You carry that {qualities_str} in your bones.",
                True
            )

        elif self.current_stage >= 7:
            return f"{prefix}{CEREMONIAL_CLOSE_STATEMENT}", True

        return f"{prefix}We are right here with you. Tell us more.", False

    def process_turn(
        self, 
        user_message: str = "", 
        was_interrupted: bool = False,
        audio_duration_sec: float = 0.0
    ) -> Dict[str, Any]:
        """Process turn with goal-gated stage progression & full context memory."""
        user_msg_clean = user_message.strip()

        if user_msg_clean:
            self.history.append({"speaker": "user", "text": user_msg_clean})

        # 1. Acoustic & Prosody Analysis
        prosody_meta = self.prosody_engine.analyze_utterance(user_msg_clean, audio_duration_sec=audio_duration_sec)
        
        # 2. 15-Emotion Spectrum Analysis
        emotion_meta = self.emotion_engine.analyze(user_msg_clean, stage=self.current_stage)

        # 3. Session Trajectory Arc
        self.arc_engine.record_turn(self.current_stage, emotion_meta, prosody_meta, user_msg_clean)

        hero_response = ""
        should_advance = False
        source = "ceremonial"

        # Stage 1 is the ceremonial opening (Ask Name if not provided)
        if self.current_stage == 1:
            if not self.user_name and not user_msg_clean:
                hero_response = (
                    "Welcome. A few minutes to dream out loud about your 2027. "
                    "Before we begin, who are we speaking with today?"
                )
                self.current_stage = 1
            elif not self.user_name and user_msg_clean:
                extracted_name = self._extract_name(user_msg_clean)
                if extracted_name:
                    self.user_name = extracted_name
                    self.manifestation_data["user_name"] = self.user_name
                    hero_response = (
                        f"Wonderful to have you with us, {self.user_name}. Let's dive in: "
                        "looking back at 2026, what's one thing from that year you're really proud of, big or quiet?"
                    )
                    self.current_stage = 2
                else:
                    # User greeted with "hi", "hey", or didn't provide a real name yet
                    greeting_word = "Hello" if "hello" in user_msg_clean.lower() else ("Hey there" if "hey" in user_msg_clean.lower() else "Welcome")
                    hero_response = (
                        f"{greeting_word}! Before we step into 2027, who are we speaking with today?"
                    )
                    self.current_stage = 1
            else:
                name_greeting = f", {self.user_name}" if self.user_name else ""
                hero_response = (
                    f"Welcome{name_greeting}. A few minutes to dream out loud about your 2027. "
                    "Tell us, what is the one thing from 2026 you're really proud of?"
                )
                self.current_stage = 2
        
        # Stage 7 is the exact close
        elif self.current_stage >= 7:
            hero_response = CEREMONIAL_CLOSE_STATEMENT
            self.is_finished = True
            self.current_stage = 7

        else:
            # Query VPS Claude Code
            claude_result = self.call_vps_claude(user_msg_clean, emotion_meta, prosody_meta)

            if claude_result:
                reply, adv, field, val = claude_result
                hero_response = reply
                should_advance = adv
                source = "claude"
                if field and val:
                    self.manifestation_data[field] = val
                    if field == "user_name":
                        self.user_name = val
            else:
                # Intelligent Fallback
                hero_response, should_advance = self._fallback_turn(user_msg_clean, emotion_meta, prosody_meta, was_interrupted=was_interrupted)
                source = "fallback"

            # Advance stage only if the goal was genuinely unlocked
            if should_advance:
                self.current_stage = min(7, self.current_stage + 1)
                if self.current_stage == 7:
                    self.is_finished = True
                    if CEREMONIAL_CLOSE_STATEMENT not in hero_response:
                        hero_response = f"{hero_response.rstrip('.!')} — {CEREMONIAL_CLOSE_STATEMENT}"
                elif self.current_stage < 6 and "?" not in hero_response:
                    bridge_q = STAGE_BRIDGE_QUESTIONS.get(self.current_stage)
                    if bridge_q:
                        hero_response = f"{hero_response.rstrip('.!')}. {bridge_q}"
            else:
                # Never leave the user hanging on a dead-end statement when staying on Stages 1-5
                if self.current_stage < 6 and "?" not in hero_response:
                    stay_q = STAGE_STAY_QUESTIONS.get(self.current_stage)
                    if stay_q:
                        hero_response = f"{hero_response.rstrip('.!')}. {stay_q}"

        self.history.append({"speaker": "hero", "text": hero_response})

        return {
            "source": source,
            "hero_response": hero_response,
            "current_stage": self.current_stage,
            "stage_name": STAGE_NAMES.get(self.current_stage, "UNKNOWN"),
            "is_finished": self.is_finished,
            "was_interrupted": was_interrupted,
            "emotion": emotion_meta,
            "prosody": prosody_meta,
            "trajectory": self.arc_engine.get_trajectory_summary(),
            "manifestation_board": self.manifestation_data
        }
