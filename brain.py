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
    VPS_CLAUDE_TOKEN,
    GROQ_API_KEY,
    GROQ_LLM_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL
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

_FILLER_RE = re.compile(
    r"\b(?:h+m+|u+h+m*|u+m+|e+r{2,}|e+r+m+|a+h+|m{2,}|uh-huh|mm-hmm)\b",
    re.IGNORECASE,
)


def strip_speech_fillers(text: str) -> str:
    """Remove standalone vocal hesitation fillers (hmm, uhhh, umm) while keeping real words intact."""
    if not text:
        return ""
    cleaned = _FILLER_RE.sub("", text)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    cleaned = re.sub(r"^[\s,.\-]+", "", cleaned).strip()
    if not any(c.isalnum() for c in cleaned):
        return ""
    return cleaned

STAGE_GOALS = {
    1: "Warmly welcome the user like a friend: 'Hey, welcome! We have a few minutes to dream a little about your 2027.' Ask what name they'd like to be called. Once they share their name, greet them warmly by name and ask about one thing from 2026 they feel proud of.",
    2: "PRIDE 2026: Ask about one thing from 2026 they feel good or proud about — big or small. If they say 'nothing' or 'I don't know', be kind and offer 2 simple options (like getting through a tough week, learning something new, or helping someone). Never repeat the exact same question.",
    3: "THE 2027 PRIDE: Ask what they'd love to feel proud of in 2027. If they aren't sure, offer 2 easy angles (like work/learning, health/confidence, or peace of mind). Never dismiss small or personal goals.",
    4: "MOVIE SCENE & NAME: Ask them to picture one happy scene from their 2027 — where are they, and what are they doing? Also ask what fun or fitting nickname they'd give that future version of themselves. If they already shared both, set ADVANCE_STAGE: YES.",
    5: "GROUNDING: Ask for one real moment from their past when they already showed that same strength or feeling. If they can't think of one, offer an easy prompt (like a time at school, work, or with family). End the stage with: 'So this is someone you already are.'",
    6: "MIRROR: Reflect back their 2027 dream, their nickname, and their real past story in simple warm words. Once they agree or say yes/yeah/true, IMMEDIATELY set ADVANCE_STAGE: YES to close.",
    7: "CLOSE: Exact ending line: 'Consider your manifestation ready. We\\'ll come back to you within the next 15 days with a surprise.'"
}

STAGE_BRIDGE_QUESTIONS = {
    2: "Looking back at 2026, what's one thing from that year you feel proud of — big or small?",
    3: "Now looking ahead to 2027, what's one thing you'd really love to feel proud of doing?",
    4: "If 2027 were a short movie scene, what moment would you love to see yourself in, and what nickname would you give that version of you?",
    5: "When in your life have you already been a little bit like that person — even in a small moment?",
    6: "Hearing all of that together, does that feel like the real you?"
}

STAGE_STAY_QUESTIONS = {
    1: "Before we start, what name should we call you today?",
    2: "It doesn't have to be huge — maybe a tough day you got through, or a choice you made for yourself in 2026?",
    3: "If you're not sure, think of one area — work, health, or just how you feel day to day. What would make 2027 feel good?",
    4: "Just picture a normal happy day in 2027 — where are you, and what are you doing?",
    5: "Think of a time at school, work, or with friends when you surprised yourself — what happened?"
}

STAGE_STAY_OPTIONS = {
    1: [
        "Before we start, what name should we call you today?",
        "What would you like us to call you? You can also say skip if you'd rather jump right in."
    ],
    2: [
        "It doesn't have to be huge — maybe a tough week you got through, or a habit you stuck with in 2026?",
        "No pressure at all. Could it be something small, like helping someone out or saying no when you needed to? Or say 'skip' to move to 2027."
    ],
    3: [
        "If nothing jumps out right away, think about three simple areas: your work, your health, or your confidence. Which one feels closest for 2027?",
        "No rush — even one small wish for how you want 2027 to feel is enough. Or you can say 'skip' if you'd like to move to the next part."
    ],
    4: [
        "Let's keep it simple: imagine a really good day in 2027. Are you somewhere quiet, or out with people?",
        "If a nickname feels tricky, what's one word that describes that future you — like 'calm', 'bold', or 'steady'? Or say 'skip' anytime."
    ],
    5: [
        "Think of an everyday moment — maybe at school, at work, or with family — when you handled something well. What comes to mind?",
        "Even a small time you didn't give up counts. Can you think of one, or would you like to skip to the wrap-up?"
    ]
}

MASTER_SYSTEM_PROMPT = """You are Hero, the Manifest 2027 companion—a warm, friendly, down-to-earth human mirror speaking as "we". You are NOT a robot, survey, therapist, or life coach.

LANGUAGE & TONE (CRITICAL):
- ALWAYS speak in simple, everyday, friendly English ONLY. Never switch to Hindi or Hinglish.
- Use simple words a friend would use in casual conversation. NEVER use heavy, poetic, or complex words like "audaciously", "sovereign", "profound", "endurance", "embodied", "ceremonial", or "electric".
- Write 2-3 warm, natural spoken sentences per reply (not one-line robotic replies, and not long essays). Use contractions ("we're", "you've", "it's").
- AVOID fake clichés ("That's beautiful/amazing/powerful", "I love that", "Absolutely", "What a wonderful answer"). React to the actual detail they shared.

ADAPTIVE RULES:
- NEVER repeat a question you already asked or ask about something they already told you.
- If they say "I don't know" or "nothing", be warm and offer 2 simple, concrete options they can pick from, or remind them they can say "skip".
- If they want to skip, respect it immediately and move forward cleanly.
- Understand messy speech-to-text typos without pointing them out. Accept corrections immediately.
- On Stages 1-5, end with ONE clear, easy question (?). On Stage 6 (MIRROR), summarize simply and ask if it feels true. On Stage 7 (CLOSE), use the exact line: "Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise." Ask no questions after."""

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

    NON_NAME_WORDS = {
        "what", "how", "why", "when", "where", "who", "which", "can", "could",
        "would", "should", "will", "tell", "give", "show", "help", "explain",
        "you", "me", "my", "your", "we", "they", "it", "this", "that", "about",
        "please", "do", "does", "did", "is", "are", "was", "were", "am", "im",
        "he", "she", "i", "the", "a", "an", "name", "recipe", "weather", "time",
        "meaning", "ceremony", "manifest", "not", "know", "hai", "hoon", "hu", "hun"
    }

    @classmethod
    def _extract_name(cls, text: str) -> Optional[str]:
        """Extract a valid human name from speech/text input. Returns None for greetings, questions, or sentences."""
        if "?" in text:
            return None
        cleaned = text.strip().rstrip(".!?,")
        if not cleaned:
            return None

        # Check explicit patterns: "my name is X", "i am X", "am X", "this is X", "call me X", "myself X"
        match = re.search(r"(?:my name is|i am|i'm|\bim\b|\bam\b|this is|call me|myself|naam hai|mera naam)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)", cleaned, re.IGNORECASE)
        if match:
            # Stop before any question/non-name words (e.g. "my name is Imansu who are you")
            name_parts = []
            for w in match.group(1).strip().split():
                if w.lower() in cls.NON_NAME_WORDS or w.lower() in cls.COMMON_GREETINGS:
                    break
                name_parts.append(w)
            candidate = " ".join(name_parts)
        else:
            cleaned_lower = cleaned.lower()
            if cleaned_lower in cls.COMMON_GREETINGS:
                return None
            raw_words = [w for w in cleaned.split() if w.lower() not in cls.COMMON_GREETINGS and w.lower() not in ["it's", "its", "here", "friend"]]
            # A bare name without intro phrasing should be 1-3 words and contain no question/sentence words
            if not raw_words or len(raw_words) > 3:
                return None
            if any(w.lower().strip(".,!?") in cls.NON_NAME_WORDS for w in raw_words):
                return None
            candidate = " ".join(raw_words)

        candidate = re.sub(r"[^A-Za-z\s\-]", "", candidate).strip()
        if not candidate or candidate.lower() in cls.COMMON_GREETINGS or len(candidate) > 30:
            return None
        if any(w.lower() in cls.NON_NAME_WORDS for w in candidate.split()):
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

        prompt = self._build_llm_prompt(user_msg, emotion_meta, include_system=True)

    def _build_llm_prompt(self, user_msg: str, emotion_meta: Dict[str, Any], include_system: bool = False) -> str:
        """Build compact, high-empathy prompt covering full conversation intelligence."""
        history_lines = []
        for turn in self.history[-5:]:
            speaker = "U" if turn["speaker"] == "user" else "H"
            history_lines.append(f"{speaker}: {turn['text'][:160]}")
        history_str = "\n".join(history_lines) if history_lines else "Start"

        captured_parts = []
        for k in ("pride_2026", "pride_2027", "movie_scene", "character_name", "grounding_story"):
            v = self.manifestation_data.get(k)
            if v:
                captured_parts.append(f"{k}={v[:80]}")
        captured_str = " | ".join(captured_parts) if captured_parts else "None yet"

        sys_block = f"{MASTER_SYSTEM_PROMPT}\n\n" if include_system else ""
        return f"""{sys_block}CONTEXT:
User: {self.user_name or 'Friend'} | Stage: {self.current_stage} ({STAGE_NAMES.get(self.current_stage, 'OPEN')})
Stage Goal: {STAGE_GOALS.get(self.current_stage, '')}
Captured so far (DO NOT re-ask these): {captured_str}
Emotion signal (tentative): {emotion_meta.get('label', 'Reflective')}
Recent conversation:
{history_str}
Latest user message: "{user_msg}"

RULES:
- Reply in simple, warm, everyday English ONLY (2-3 friendly spoken sentences, easy to understand, zero complex words).
- Never repeat a question already in Recent conversation.
- If the user has no answer ("I don't know", "nothing", etc.), give 2 simple options to choose from, or mention they can say "skip".
- For Stages 1-5, end with ONE simple question (?). For Stage 7 (CLOSE), use the exact closing statement and ask NO questions.

FORMAT (strict):
REPLY: <natural spoken response>
ADVANCE_STAGE: <YES|NO>
CAPTURED_FIELD: <user_name|pride_2026|pride_2027|character_name|movie_scene|grounding_story|NONE>
CAPTURED_VALUE: <short accurate value|NONE>
TRANSITION_REASON: <STAY|EXPLORE|ADVANCE|PAUSE|CLOSE>"""

    def call_groq_llm(
        self,
        user_msg: str,
        emotion_meta: Dict[str, Any],
        prosody_info: Dict[str, Any]
    ) -> Optional[Tuple[str, bool, Optional[str], Optional[str]]]:
        """Ultra-fast (~0.4-0.8s) Groq Llama 3.3 70B brain."""
        if not GROQ_API_KEY:
            return None

        prompt = self._build_llm_prompt(user_msg, emotion_meta, include_system=True)
        try:
            payload = {
                "model": GROQ_LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.65,
                "max_tokens": 350
            }
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "User-Agent": "Manifest2027-Hero/1.0"
                }
            )
            with urllib.request.urlopen(req, timeout=6.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply_text = data["choices"][0]["message"]["content"].strip()
                if reply_text:
                    parsed = self._parse_claude_response(reply_text)
                    print(f"\n[⚡ Groq {GROQ_LLM_MODEL}] Spoken: '{parsed[0][:60]}...' | Advance: {parsed[1]}")
                    return parsed
        except Exception as e:
            print(f"[Groq LLM Fallback Triggered] {e}")
        return None

    def call_gemini_llm(
        self,
        user_msg: str,
        emotion_meta: Dict[str, Any],
        prosody_info: Dict[str, Any]
    ) -> Optional[Tuple[str, bool, Optional[str], Optional[str]]]:
        """Direct Gemini Flash brain with MASTER_SYSTEM_PROMPT instruction + fast fallback."""
        if not GEMINI_API_KEY:
            return None

        prompt = self._build_llm_prompt(user_msg, emotion_meta, include_system=True)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        try:
            payload = {
                "systemInstruction": {"parts": [{"text": MASTER_SYSTEM_PROMPT}]},
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.65,
                    "maxOutputTokens": 250,
                    "thinkingConfig": {"thinkingBudget": 0}
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=6.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if reply_text:
                    parsed = self._parse_claude_response(reply_text)
                    print(f"\n[⚡ Gemini {GEMINI_MODEL}] Spoken: '{parsed[0][:60]}...' | Advance: {parsed[1]}")
                    return parsed
        except Exception as e:
            print(f"[Gemini LLM Fallback Triggered] {e}")
        return None

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
        raw_msg = user_message.strip()
        user_msg_clean = strip_speech_fillers(raw_msg) if raw_msg else ""

        # If the user sent only vocal hesitation fillers ("hmm", "uhhh", "umm") on text/chat,
        # pause gently without advancing stage or polluting history.
        if raw_msg and not user_msg_clean:
            return {
                "source": "filler_pause",
                "hero_response": "Take your time, we're right here whenever you're ready.",
                "current_stage": self.current_stage,
                "stage_name": STAGE_NAMES.get(self.current_stage, "OPEN"),
                "is_finished": self.is_finished,
                "was_interrupted": was_interrupted,
                "emotion": self.emotion_engine.analyze(raw_msg, stage=self.current_stage),
                "prosody": self.prosody_engine.analyze_utterance(raw_msg, audio_duration_sec=audio_duration_sec),
                "trajectory": self.arc_engine.get_trajectory_summary(),
                "manifestation_board": self.manifestation_data
            }

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

        # Universal Skip Handler (Stages 1-6): let user skip any step cleanly
        msg_lower_skip = re.sub(r"[^\w\s']", " ", user_msg_clean.lower()).strip()
        skip_exact = {"skip", "pass", "next", "skip it", "skip this", "next question", "next step", "move on", "skip question"}
        skip_phrases = ("skip this", "skip the question", "next question", "move on", "don't want to answer", "dont want to answer", "let's skip", "lets skip")
        is_skip = (msg_lower_skip in skip_exact) or any(p in msg_lower_skip for p in skip_phrases)

        if is_skip and 1 <= self.current_stage < 7:
            self.current_stage = min(7, self.current_stage + 1)
            source = "skip"
            if self.current_stage == 7:
                self.is_finished = True
                hero_response = f"No problem at all, we can leave that one aside. {CEREMONIAL_CLOSE_STATEMENT}"
            else:
                bridge_q = STAGE_BRIDGE_QUESTIONS.get(self.current_stage, "")
                hero_response = f"Totally fine, we can skip that one and keep going. {bridge_q}".strip()

        # Stage 1 is the ceremonial opening (Ask Name if not provided)
        elif self.current_stage == 1:
            if not self.user_name and not user_msg_clean:
                hero_response = (
                    "Hey, welcome! We have a few minutes to chat and dream a little about your 2027 — no pressure at all. "
                    "Before we start, what name should we call you?"
                )
                self.current_stage = 1
            elif not self.user_name and user_msg_clean:
                extracted_name = self._extract_name(user_msg_clean)
                if extracted_name:
                    self.user_name = extracted_name
                    self.manifestation_data["user_name"] = self.user_name
                    hero_response = (
                        f"So nice to have you here, {self.user_name}! Let's take this nice and easy. "
                        "Looking back at 2026, what's one thing from that year you feel proud of — big or small?"
                    )
                    self.current_stage = 2
                else:
                    # Try fast Groq LLM first (then VPS Claude) for natural phrases / name extraction / questions
                    is_pure_greeting = msg_lower_skip in self.COMMON_GREETINGS
                    if not is_pure_greeting:
                        llm_result = self.call_groq_llm(user_msg_clean, emotion_meta, prosody_meta)
                        src_name = "groq"
                        if not (llm_result and llm_result[0]):
                            llm_result = self.call_vps_claude(user_msg_clean, emotion_meta, prosody_meta)
                            src_name = "claude"

                        if llm_result and llm_result[0]:
                            hero_response, adv, field, val = llm_result
                            source = src_name
                            if field == "user_name" and val and val.upper() != "NONE":
                                self.user_name = val.strip().title()
                                self.manifestation_data["user_name"] = self.user_name
                            if adv or self.user_name:
                                self.current_stage = 2
                                if "?" not in hero_response:
                                    hero_response = f"{hero_response.rstrip('.!')}. {STAGE_BRIDGE_QUESTIONS[2]}"
                            else:
                                self.current_stage = 1
                                if "?" not in hero_response:
                                    hero_response = f"{hero_response.rstrip('.!')}. {STAGE_STAY_OPTIONS[1][0]}"
                        else:
                            hero_response = f"Good question — we're just here to dream a little about your 2027 together! {STAGE_STAY_OPTIONS[1][0]}"
                            self.current_stage = 1
                    else:
                        greeting_word = "Hey there" if "hey" in user_msg_clean.lower() else ("Hello" if "hello" in user_msg_clean.lower() else "Welcome")
                        hero_response = (
                            f"{greeting_word}! We're glad you're here. Before we jump into 2027, what name should we call you today?"
                        )
                        self.current_stage = 1
            else:
                name_greeting = f", {self.user_name}" if self.user_name else ""
                hero_response = (
                    f"Hey{name_greeting}! We have a few minutes to dream a little about your 2027. "
                    "Looking back at 2026, what's one thing from that year you feel proud of — big or small?"
                )
                self.current_stage = 2
        
        # Stage 7 is the exact close
        elif self.current_stage >= 7:
            hero_response = CEREMONIAL_CLOSE_STATEMENT
            self.is_finished = True
            self.current_stage = 7

        else:
            # Query fast Groq LLM first (~0.7-1.5s), then VPS Claude Sonnet fallback (skip slow 6s Gemini timeout)
            groq_result = self.call_groq_llm(user_msg_clean, emotion_meta, prosody_meta)
            if groq_result:
                reply, adv, field, val = groq_result
                hero_response = reply
                should_advance = adv
                source = "groq"
                if field and val:
                    self.manifestation_data[field] = val
                    if field == "user_name":
                        self.user_name = val
            else:
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

            # Deterministic Stage 6 Mirror -> Close safety net on user affirmation
            if self.current_stage == 6 and not should_advance:
                msg_l = user_msg_clean.lower()
                affirm_words = {"yes", "yeah", "yep", "true", "haan", "ha", "ji", "done", "finish"}
                affirm_phrases = ["feel that", "this is it", "feels true", "so true", "completely true", "resonates", "hits home", "finish it"]
                if (set(re.findall(r"\b[a-z]+\b", msg_l)) & affirm_words) or any(p in msg_l for p in affirm_phrases):
                    should_advance = True

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
                # Never leave the user hanging on a dead-end statement; vary stay options so we never repeat
                if self.current_stage < 6 and "?" not in hero_response:
                    opts = STAGE_STAY_OPTIONS.get(self.current_stage)
                    if opts:
                        stay_q = opts[self.stage_attempts.get(self.current_stage, 0) % len(opts)]
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
