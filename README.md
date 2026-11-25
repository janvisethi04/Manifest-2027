# 🕯️ Hero: Manifest 2027 AI Voice Agent

> A pure Python conversational voice agent and ceremonial studio for **Manifest 2027**.  
> Features the **Living Celestial Mirror Core**, **15-spectrum human psychological emotion & sentiment awareness**, continuous microphone listening, instant **barge-in / interruption handling (<10ms latency)**, and studio-grade neural voice synthesis—with **zero third-party subscription costs**.

---

## 📸 The Celestial Mirror Chamber

```
┌─────────────────────────────────────────────────────────────┬────────────────────────────────────┐
│ [M] MANIFEST 2027  [Stage: 1. Welcome Ritual ●○○○○○○]       │ 🎙️ Christopher   👤 Profile   📊 Telemetry│
├─────────────────────────────────────────────────────────────┼────────────────────────────────────┤
│                                                             │                                    │
│                 [ ✦ Ready to Begin Ceremony ]               │   ✦ The 2027 Mirror Call           │
│                                                             │   Hero senses your emotional       │
│                     ╭──────────────╮                        │   cadence, vulnerability, and      │
│                  ╭──│  ORBITAL     │──╮                     │   audacity—attuning reflection.    │
│                  │  │  LIVING CORE │  │                     │                                    │
│                  ╰──│  CELESTIAL   │──╯                     │   HERO [Stage 1: OPEN]             │
│                     ╰──────────────╯                        │   "Welcome, Janvi. A few minutes   │
│                       📞 (Call/End)                         │    to dream out loud..."           │
│                                                             │                                    │
│             [ 🎙️ Mute | ⚡ Barge-in: <10ms ]                │ ┌────────────────────────────────┐ │
│                                                             │ │ Speak or whisper your thought..│ │
│                                                             │ └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┴────────────────────────────────────┘
```

---

## 🧠 15-Spectrum Emotion & Sentiment Awareness Engine

Hero listens not just to words, but to the **emotional frequency** of the human voice:

| Emotion Archetype | Human Trigger & Feeling | Hero's Adaptive Response | Core Aura | Voice Modulation |
|---|---|---|---|---|
| **1. Grief & Loss** | Bereavement, heartbreak, tears, pain | Honors the loss before speaking of the future | 🌌 Deep Indigo | Slow & reverent (`-12% rate`) |
| **2. Frustration & Anger** | Betrayal, unfairness, feeling stuck, anger | Validates the fire; channels tension into sovereignty | 🔴 Crimson Fire | Firm & grounding |
| **3. Impostor & Shame** | "I'm a fraud, not good enough, failure" | Grounds strictly in factual past diligence | 🔮 Amethyst | Reassuring & steady |
| **4. Loneliness & Isolation** | "Doing it alone, nobody understands" | *"We are standing right here as your mirror"* | 🌌 Twilight Cobalt | Warm companionship |
| **5. Skeptical & Guarded** | "Is manifestation real, or fake/gimmick" | Does not convince; invites scrutiny of their own feats | 🔘 Slate Silver | Neutral & respectful |
| **6. Confused & Crossroads** | Foggy mind, indecision, directionless | Focuses attention on the single next breath | 🌊 Teal Cyan | Clear & calming |
| **7. Vulnerable & Tender** | Raw truth, fear, insecurities, exposed | Mirrors honesty as genuine courage | 💜 Soft Lavender | Gentle & soft (`-8% rate`) |
| **8. Overwhelmed & Burnout** | Chaos, exhausted, running on empty | Guides into slow unhurried exhale; removes pressure | 💠 Sky Blue | Peaceful pause (`-10% rate`) |
| **9. Hopeful & Yearning** | Quiet wish, longing, dreaming | Protects and expands that tender flame | 🌸 Rose Quartz | Soft & hopeful |
| **10. Determined & Grit** | Relentless, hustle, never giving up | Mirrors unyielding backbone and battle-tested diligence | 🩸 Ruby Core | Solid & resolute |
| **11. Proud & Accomplished** | Earned feats, milestones, hard work | Helps savour victory without rushing | 🌟 Amber Gold | Warm celebration |
| **12. Audacious & Sovereign** | Empire, fearless, massive scale | Matches bold sovereignty and regal command | 🔥 Solar Ember | High energy (`+3% rate`) |
| **13. Joyful & Playful** | Exuberance, laughing, lighthearted | Celebrates lightness and childlike vitality | ☀️ Radiant Sun | Upbeat (`+4% rate`) |
| **14. Gratitude & Reverence** | Blessed, deeply thankful, sacred awe | Holds reverent silence; expands grace | 🍯 Golden Honey | Sacred pause |
| **15. Peaceful & Grounded** | Morning tea, ocean, quiet stillness | Maintains tranquil, unhurried ease | 🍃 Emerald Sage | Unhurried ease (`-6% rate`) |

---

## 🌟 Core System Highlights

- **Dynamic SSML Voice Modulation**: When the user sounds vulnerable or exhausted, Edge-TTS dynamically reduces speaking rate (`-8%` to `-12%`) and lowers pitch to soothe. When the user speaks with bold audacity, the voice accelerates with resonant command.
- **Dynamic Visual Aura**: The Celestial Orb's aura and orbital rings shift color in real-time according to the detected emotion.
- **Zero-Latency Barge-In (<10ms)**: If you speak or type while Hero is talking, audio cuts immediately and Hero seamlessly integrates your interruption (`"Got you"`, `"Understood"`).
- **7-Stage Ceremonial Dialogue Engine**:
  1. **Open**: Welcome ritual to dream out loud.
  2. **Pride 2026**: Savouring what was achieved in 2026.
  3. **Pride 2027 (Audacity Gap)**: Morning day-in-the-life vision.
  4. **Movie Scene & Character Archetype**: Naming the character and the pivotal cinematic scene.
  5. **Grounding**: Uncovering real past proof of diligence.
  6. **Mirror Revelation**: Sacred pause and reflection of core qualities.
  7. **Exact Ceremonial Close**:
     > *"Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."*
- **Zero Subscription Cost**: Powered by Edge-TTS neural models (`en-US-ChristopherNeural`, `hi-IN-MadhurNeural`, `en-US-AvaNeural`).

---

## 🚀 Quickstart Guide

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
*Opens `http://localhost:8000` with the living Celestial Chamber UI.*

### 3. Run in Terminal CLI Mode (Optional)
```bash
# Microphone + Speaker in terminal
python main.py --cli

# Keyboard + Speaker in terminal
python main.py --cli --text

# Hindi / Hinglish Neural Voice Model
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
├── app.py                # FastAPI server (Chat turns, dynamic SSML TTS, WebSockets)
├── static/
│   └── index.html        # Celestial Mirror Chamber UI (Orb, Aura, Stage Stepper)
├── emotion_engine.py     # 15-spectrum human psychological emotion engine
├── brain.py              # 7-stage dialogue state machine with emotion bridges
├── stt.py                # Microphone capture & Voice Activity Detection (VAD)
├── tts.py                # Edge-TTS synthesizer with instant <10ms stop latency
├── config.py             # Voice choices, STT thresholds, and ceremonial close text
├── main.py               # Main CLI runner (launches UI or terminal agent)
├── test_agent.py         # Automated test suite for all 15 emotions & 7 stages
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🛡️ License

MIT License. Crafted with reverence for Manifest 2027.
