"""
Hero Voice Agent: Orchestrator for Manifest 2027
Coordinates:
- Speech Recognition (STT)
- Dialogue Brain (7 Ceremonial Stages)
- Edge-TTS Neural Voice (TTS)
- Zero-latency Interruption / Barge-in Handler
"""
import time
import threading
from typing import Dict, Any, Optional

from brain import HeroBrain
from tts import TTSEngine
from stt import STTEngine
from config import DEFAULT_VOICE, BARGE_IN_ENABLED

class HeroVoiceAgent:
    def __init__(self, context: Optional[Dict[str, Any]] = None, voice: str = DEFAULT_VOICE):
        self.context = context or {}
        self.brain = HeroBrain(self.context)
        self.tts = TTSEngine(voice=voice)
        self.stt = STTEngine()
        self.was_interrupted = False
        self._is_running = False

        # Register barge-in trigger: cut TTS playback instantly when user talks
        if BARGE_IN_ENABLED:
            self.stt.register_on_speech_started(self.on_user_interrupt)

    def on_user_interrupt(self):
        """Called immediately when speech activity is detected while Hero is talking."""
        if self.tts.is_speaking():
            print("\n[⚡ BARGE-IN DETECTED] User spoke while Hero was talking. Audio cut immediately (<10ms).")
            self.tts.stop()
            self.was_interrupted = True

    def start_conversation(self, mode: str = "voice"):
        """
        Start full ceremonial conversation.
        Modes:
            - 'voice': Live mic listening + Edge-TTS speech output
            - 'text': Terminal typing + Edge-TTS speech output (hybrid)
            - 'simulation': Headless automatic flow verification
        """
        self._is_running = True
        self.brain.reset()
        print("\n" + "=" * 65)
        print("🕯️  HERO: MANIFEST 2027 CEREMONIAL VOICE AGENT")
        print(f"👤  User: {self.brain.user_name}")
        print(f"🎙️  Voice Model: {self.tts.voice}")
        print(f"⚡  Barge-In Interruption: {'Active' if BARGE_IN_ENABLED else 'Disabled'}")
        print("=" * 65 + "\n")

        # Stage 1: Hero Opens
        first_turn = self.brain.process_turn("", was_interrupted=False)
        self._deliver_response(first_turn["hero_response"])

        # Main dialogue loop
        while self._is_running and not self.brain.is_finished:
            user_input = ""
            was_cut = self.was_interrupted
            self.was_interrupted = False  # Reset for this turn

            if mode == "voice":
                # Listen to user via microphone
                spoken_text = self.stt.listen_and_transcribe(timeout=15)
                if spoken_text is None:
                    # Timeout with silence: gently prompt
                    print("[Silence detected] Gently inviting user...")
                    user_input = ""
                else:
                    user_input = spoken_text
                    print(f"🗣️ You said: \"{user_input}\"")

            elif mode == "text":
                # User types input, Hero speaks response
                try:
                    user_input = input("\n🗣️ You (type or press Enter): ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n[Session ended by user]")
                    break

            # Process turn through 7-stage dialogue brain
            turn_result = self.brain.process_turn(user_input, was_interrupted=was_cut)
            stage_name = turn_result["stage_name"]
            hero_text = turn_result["hero_response"]

            print(f"\n[Stage {turn_result['currentStage'] if 'currentStage' in turn_result else self.brain.current_stage}: {stage_name}]")
            self._deliver_response(hero_text)

            if turn_result["is_finished"]:
                print("\n✨ Manifestation ceremony complete. Connection closed gracefully.\n")
                break

        self.tts.cleanup()

    def _deliver_response(self, text: str):
        """Deliver Hero's response through console and studio neural voice."""
        print(f"✨ Hero: \"{text}\"")
        completed = self.tts.speak(text, blocking=True)
        if not completed:
            # Playback was interrupted by barge-in
            self.was_interrupted = True

    def process_direct_message(self, text: str, was_interrupted: bool = False) -> Dict[str, Any]:
        """Direct method for programmatic and API calls."""
        return self.brain.process_turn(text, was_interrupted=was_interrupted)
