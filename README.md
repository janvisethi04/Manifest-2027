# 🕯️ Hero: Manifest 2027 AI Voice Agent

> A pure Python conversational voice agent designed as a sacred mirror of potential for **Manifest 2027**.  
> Features studio-quality neural voices, continuous microphone listening, dynamic voice activity detection (VAD), and **real-time barge-in / interruption handling (<10ms latency)** with zero third-party platform lock-in (no ElevenLabs subscription needed).

---

## 🌟 Key Highlights

- **Pure Python Voice Agent**: No web frameworks or unnecessary frontends—engineered from the ground up as an interactive voice agent (`main.py`).
- **Real-Time Barge-In (<10ms)**: When you speak while Hero is speaking, Hero cuts audio playback instantly, acknowledges the interruption naturally (`"Got you"`, `"Understood"`), and seamlessly adapts the conversation flow.
- **7-Stage Ceremonial Brain**: Strictly executes the sacred Manifest 2027 dialogue progression with gentle guidance, never interrogating, and ends on the exact ceremonial statement.
- **Studio-Quality Neural Voices**: Powered by Edge-TTS neural models (`en-US-ChristopherNeural`, `hi-IN-MadhurNeural`, `en-US-AvaNeural`) with zero cost and zero API keys.
- **Continuous STT & VAD**: Uses adaptive ambient noise calibration, microphone streaming, and voice activity detection.

---

## 🏛️ Architecture Flow

```
   ┌─────────────────────────────────────────────────────────┐
   │                  Microphone Input                       │
   └─────────────────────────┬───────────────────────────────┘
                             │
                             ▼
   ┌─────────────────────────────────────────────────────────┐
   │                 STT & VAD Engine                        │
   │  (Ambient Calibration, Speech Detection & Transcribe)   │
   └─────────────┬───────────────────────────┬───────────────┘
                 │                           │
          [Voice Detected]              [Transcript]
                 │                           │
                 ▼                           ▼
   ┌──────────────────────────┐    ┌─────────────────────────┐
   │ Instant Barge-in Cutoff  │    │     7-Stage Brain       │
   │  (Stops TTS in <10ms)    │    │ (Projection & Grounding)│
   └──────────────────────────┘    └─────────┬───────────────┘
                                             │
                                       [Hero Response]
                                             │
                                             ▼
                                   ┌─────────────────────────┐
                                   │     Edge-TTS Engine     │
                                   │ (Studio Neural Playback)│
                                   └─────────────────────────┘
```

---

## 📜 The 7 Ceremonial Stages

1. **Open**: Light ritual greeting to dream out loud about 2027.
2. **Pride 2026**: Savouring what you achieved in 2026.
3. **Pride 2027 (Audacity Gap)**: Expanding the vision into what you want to be deeply proud of in 2027, including day-in-the-life morning visualization.
4. **Movie Scene & Character**: Naming the character archetype and visualizing the pivotal scene.
5. **Grounding**: Uncovering past real-life proof and evidence of diligence from your own journey.
6. **Mirror Revelation**: Reflecting your core qualities and evidence back to you with a sacred pause.
7. **Exact Close**:
   > *"Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."*

---

## 🚀 Quickstart Guide

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/janvisethi04/Manifest-2027.git
cd Manifest-2027

# Install Python requirements
pip install -r requirements.txt
```

### 2. Run in Live Voice Mode (Microphone + Speaker)

Put on your headphones or use your speakers/mic, and start:

```bash
python main.py
```
*Hero will calibrate to your room's ambient noise, speak the welcome ritual, and listen for your voice.*

### 3. Run in Hybrid Mode (Keyboard + Speaker)

If you don't have a microphone handy or want to test via keyboard:

```bash
python main.py --mode text
```
*You type your responses; Hero speaks back aloud in high-definition voice.*

### 4. Hindi / Hinglish Voice

To experience the ceremony in a natural Hindi/Hinglish tone:

```bash
python main.py --voice hindi
```

### 5. Run Verification Test Suite

Run the automated integration tests verifying all 7 stages, barge-in recovery, vague answer handling, and TTS latency:

```bash
python main.py --test
# or
python test_agent.py
```

---

## 📁 Repository Structure

```
.
├── config.py             # Voice choices, STT thresholds, timeouts, and closing text
├── brain.py              # 7-stage dialogue state machine, context, and recovery logic
├── stt.py                # Speech-to-Text & real-time Voice Activity Detection (VAD)
├── tts.py                # Edge-TTS synthesizer with instant <10ms stop playback
├── agent.py              # Central orchestrator handling the audio loop & barge-in
├── main.py               # Command-line entry point with CLI options
├── test_agent.py         # Automated test suite (Stages, Barge-in, TTS latency)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚡ Real-Time Barge-In Details

In real human conversations, people interrupt or interject naturally. Hero mirrors this behavior:

1. While Hero is speaking, `STTEngine` listens via non-blocking audio detection.
2. The moment voice energy is registered from the user, an interrupt event fires immediately.
3. `TTSEngine.stop()` cuts Pygame mixer audio within **<10ms**.
4. Hero listens to the user's interjection and sets `was_interrupted = True`.
5. Hero's Brain resumes with natural conversational prefixes (`"Got you."`, `"Understood."`, `"I hear you."`), seamlessly progressing without broken state.

---

## 🛡️ License

MIT License. Designed with care for Manifest 2027.
