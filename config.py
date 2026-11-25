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

# VPS Claude Code Bridge Configuration
USE_VPS_CLAUDE = False                          # Set True to use VPS Claude Code
VPS_CLAUDE_URL = "http://127.0.0.1:5001/chat"   # Tunnels via SSH (or VPS Public IP)
VPS_CLAUDE_TOKEN = ""                           # Read from bridge_token.txt

