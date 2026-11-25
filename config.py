"""
Configuration for Hero: Manifest 2027 Voice Agent
"""
import os

# Voice Configuration (Zero cost, high-definition Edge-TTS neural models)
DEFAULT_VOICE = "en-US-ChristopherNeural"      # Deep, calm, reflective masculine voice
HINDI_VOICE = "hi-IN-MadhurNeural"              # Natural Hindi/Hinglish voice
FEMALE_VOICE = "en-US-AvaNeural"                # Warm, empathetic feminine voice

# Speech-To-Text Configuration
STT_ENERGY_THRESHOLD = 300                      # Microphone sensitivity threshold
STT_PAUSE_THRESHOLD = 0.8                       # Seconds of silence indicating end of utterance
STT_PHRASE_TIME_LIMIT = 15                      # Max length of a single utterance in seconds

# Barge-In / Interruption Configuration
BARGE_IN_ENABLED = True                         # Cut speech immediately when user talks
BARGE_IN_DEBOUNCE_MS = 250                      # Avoid false trigger from ambient noise/clicks

# Audio Output Configuration
SAMPLE_RATE = 24000
CHANNELS = 1

# Master Prompt & Ceremonial Close
CEREMONIAL_CLOSE_STATEMENT = (
    "Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."
)

# Helper to load .env safely without third-party dependencies
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

# VPS Claude Code Bridge Configuration (Secured via .env)
USE_VPS_CLAUDE = os.getenv("USE_VPS_CLAUDE", "False").lower() in ["true", "1", "yes"]
VPS_CLAUDE_URL = os.getenv("VPS_CLAUDE_URL", "http://127.0.0.1:5001/chat")
VPS_CLAUDE_TOKEN = os.getenv("VPS_CLAUDE_TOKEN", "")

