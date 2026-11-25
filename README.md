# 🕯️ Hero: Manifest 2027 AI Voice Agent

> An exact, self-hosted reproduction of the **ElevenLabs Conversational Voice Agent Interface** for **Manifest 2027**.  
> Features the living voice orb, real-time microphone listening, instant **barge-in / interruption handling (<10ms)**, and studio-grade neural voice synthesis—with **zero third-party subscription costs**.

---

## 📸 Interface Preview (ElevenLabs Agent Canvas)

```
┌─────────────────────────────────────────────────────────────┬────────────────────────────────────┐
│ < Back  History  Debugger    Manifest 2027 | Main           │ Voice settings  {} Vars   Architect│
├─────────────────────────────────────────────────────────────┼────────────────────────────────────┤
│                                                             │                                    │
│                     [ Ready to connect ]                    │    (💬)                            │
│                                                             │    Call or send a message to       │
│                                                             │    start a new conversation        │
│                       ●  (Living Orb)                       │                                    │
│                         📞 (Call Button)                    │                                    │
│                                                             │                                    │
│                                                             │                                    │
│                                                             │ ┌────────────────────────────────┐ │
│                     [ ⚙️  |  🎙️ Mute ]                      │ │ Send a message to start a chat ▶│ │
│                                                             │ └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┴────────────────────────────────────┘
```

---

## 🌟 Key Highlights

- **Exact ElevenLabs UI & Experience**:
  - Left Canvas: Diagonal pinstripe texture, 3D animated living voice orb, call toggle badge, and mute/settings pill.
  - Right Panel: Real-time transcript, ceremonial stage tracking (`[Stage 1: OPEN]`, `[Stage 2: PRIDE]`, etc.), and message input bar.
  - Top Bar: Quick access to `< Back`, `History`, `Debugger` (live latency & state), and `{}` `Vars` (user context editor).
- **Zero-Latency Barge-In (<10ms)**: If you speak or type while Hero is talking, playback cuts immediately and Hero recovers naturally (`"Got you"`, `"Understood"`).
- **7-Stage Ceremonial Dialogue Engine**: Executes the exact Manifest 2027 dialogue sequence, never interrogating, and closes on the sacred statement:
  > *"Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."*
- **Studio-Quality Neural Voices**: Powered by Microsoft Edge-TTS (`en-US-ChristopherNeural`, `hi-IN-MadhurNeural`, `en-US-AvaNeural`) with **zero API cost**.

---

## 🚀 Quickstart

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Launch the Voice Agent Studio (Default)
```bash
python main.py
# or
python app.py
```
*Opens `http://localhost:8000` immediately with the living Voice Agent UI.*

### 3. Run in Terminal CLI Mode (Optional)
```bash
# Microphone + Speaker in terminal
python main.py --cli

# Keyboard + Speaker in terminal
python main.py --cli --text

# Hindi / Hinglish Voice Model
python main.py --cli --voice hindi
```

### 4. Run Automated Test Suite
```bash
python main.py --test
# or
python test_agent.py
```

---

## 📁 Repository Structure

```
.
├── app.py                # FastAPI server serving the Agent UI & audio endpoints
├── static/
│   └── index.html        # Exact ElevenLabs-style living Voice Agent UI
├── main.py               # Main CLI runner (launches UI or terminal agent)
├── agent.py              # Central Voice Agent orchestrator
├── brain.py              # 7-stage ceremonial dialogue state machine
├── stt.py                # Speech-to-Text & Voice Activity Detection
├── tts.py                # Edge-TTS synthesizer with instant <10ms stop latency
├── config.py             # Voice choices, STT thresholds, and closing text
├── test_agent.py         # Automated test suite
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚡ Barge-In Architecture

1. **Detection**: Microphone listens via Web Audio / PyAudio with dynamic voice activity thresholds.
2. **Instant Cutoff**: Audio pauses and unloads in `<10ms` the moment voice energy is detected.
3. **Dialogue Recovery**: Brain tags the turn with `was_interrupted = True` and uses conversational acknowledgment before advancing smoothly.

---

## 🛡️ License

MIT License. Designed with care for Manifest 2027.
