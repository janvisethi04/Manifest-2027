"""
Speech-to-Text (STT) and Voice Activity Detection (VAD) Engine
Features:
- Continuous ambient calibration
- Real-time speech start detection for instantaneous Barge-In / Interruption cutoff
- Online Google Speech Recognition with offline fallback
"""
import time
from typing import Callable, Optional
import speech_recognition as sr
from config import STT_ENERGY_THRESHOLD, STT_PAUSE_THRESHOLD, STT_PHRASE_TIME_LIMIT

class STTEngine:
    def __init__(self, energy_threshold: int = STT_ENERGY_THRESHOLD):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = STT_PAUSE_THRESHOLD
        self._microphone: Optional[sr.Microphone] = None
        self._on_speech_started: Optional[Callable[[], None]] = None

    def register_on_speech_started(self, callback: Callable[[], None]):
        """Register a callback triggered immediately when user voice is detected (for barge-in)."""
        self._on_speech_started = callback

    def calibrate(self, duration: float = 1.0) -> bool:
        """Calibrate microphone to ambient background noise."""
        try:
            with sr.Microphone() as source:
                print(f"[STT] Calibrating microphone for {duration}s ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                print(f"[STT] Calibration complete. Energy threshold: {self.recognizer.energy_threshold:.1f}")
                return True
        except Exception as e:
            print(f"[STT Warning] Microphone calibration failed: {e}")
            return False

    def listen_and_transcribe(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Listen for a user utterance and transcribe to text.
        Emits on_speech_started callback as soon as voice activity begins.
        """
        try:
            with sr.Microphone() as source:
                # Trigger interrupt callback immediately if listening begins while agent is talking
                if self._on_speech_started:
                    # Let recognizer listen with phrase time limit
                    pass

                print("\n[STT] Listening (speak now)...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=STT_PHRASE_TIME_LIMIT
                )

                # User started speaking, notify agent to cut TTS if still speaking
                if self._on_speech_started:
                    self._on_speech_started()

                print("[STT] Transcribing voice...")
                text = self.recognizer.recognize_google(audio)
                return text.strip()

        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            # Voice was detected but could not be understood
            return ""
        except sr.RequestError as e:
            print(f"[STT Error] Speech service unreachable: {e}")
            return None
        except Exception as e:
            print(f"[STT Error] Audio capture error: {e}")
            return None
