# Converse AI – Manifest 2027
### Personalized Voice Sanctuary & Manifestation Platform

An intimate, emotionally intelligent manifestation experience where users reflect on their journey, schedule a ceremonial voice session with **Hero** (an AI companion mirroring their potential), and receive a bespoke **Miro Manifestation Board** based on their genuine words.

---

## 🌟 Key Architecture & Capabilities

1. **Custom Real-Time Voice Engine (Zero-Cost Local Pipeline)**:
   - **Continuous STT:** Low-latency real-time microphone stream with hardware-level Acoustic Echo Cancellation (AEC) and noise suppression.
   - **Barge-In / Interruption Engine:** Instant audio cutoff (<10ms) when the user speaks while Hero is talking, with seamless turn recovery.
   - **Hero Ceremonial Brain:** Strict 7-stage dialogue state machine following the Master System Prompt:
     1. *Open* (Light ritual & dream out loud)
     2. *Pride* (2026 savouring)
     3. *The 2027 Pride* (Closing the audacity gap)
     4. *The Character as a Scene* (Movie scene & naming)
     5. *Grounding* (Evidence of past feats)
     6. *Mirror* (Revelation & reflection)
     7. *Exact Close:* *"Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."*
   - **TTS:** Studio-grade natural neural voice synthesis via Edge-TTS.

2. **ElevenLabs Agent Integration**:
   - Production-ready configuration for ElevenLabs Conversational AI (`agent_1401m86ep0mnewcs2x1wth46mmy9`).
   - Dynamic variable injection: `{{user_name}}`, `{{preferred_language}}`, `{{pre_call_context}}`, `{{user_qualities}}`.
   - Automated 1-click Python provisioning script (`setup_agent.py`).

3. **Dynamic Celestial Dark Theming**:
   - Deep Midnight Obsidian default aesthetic (`#0B0813`, `#161124`, Starlight Gold `#CCA456`, Soft Lavender `#A78BFA`).
   - Live color-shifting UI that adapts based on user questionnaire answers & elements:
     - 🔥 **Midnight Phoenix (Fire):** Charcoal & Amber Rose
     - 🌊 **Abyssal Moonlit (Water):** Deep Navy & Starlight Cyan
     - 🌿 **Forest Moss & Stone (Earth):** Emerald Pine & Champagne Gold
     - 🌌 **Starlight Horizon (Air):** Twilight Indigo & Stardust

4. **Input Quality & Anti-Abuse Safeguards**:
   - **Strict Email Verification:** Rejects disposable/burner domains (`tempmail`, `mailinator`, etc.) and keyboard-mash patterns (`asdf@asdf`, `test@test`).
   - **Vague Answer Helper:** Detects short/generic inputs ("idk", "money", "nothing") and offers instant clickable thought-starter prompts.

5. **Appointment Booking Sanctuary (`/booking`)**:
   - 15-minute slot reservation across morning, afternoon, and evening slots.
   - Automatic local timezone detection (`Intl.DateTimeFormat`).
   - Double-booking prevention and booking confirmation dispatch.

6. **Miro Board Manifestation Engine & Email Delivery**:
   - Generates personalized Miro board containing 5 color-coded sticky notes (2027 Vision, 2026 Grounding Feat, Archetype Card, Quote, and Qualities).
   - Instant in-app interactive scrapbook canvas with PNG/PDF export.
   - Dispatches confirmation emails with private board access.

---

## 🚀 Quick Start

### Prerequisites
- Node.js v18+ or v20+
- Python 3.10+ (for Edge-TTS neural voice synthesis)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Install Python Voice Engine Dependencies
```bash
pip install edge-tts
```

### 3. Run Development Server
```bash
npm run dev
```

Visit **http://localhost:3000** in your browser.

---

## 📂 Project Structure

```
converse-ai-manifest-2027/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx               # Landing Page
│   │   │   ├── questionnaire/page.tsx # 6-Step Reflective Questionnaire
│   │   │   ├── booking/page.tsx       # Appointment Slot Booking
│   │   │   ├── call/page.tsx          # Real-Time Voice Sanctuary with Hero
│   │   │   ├── board/page.tsx         # Miro & Canvas Manifestation Board
│   │   │   └── api/
│   │   │       ├── voice/hero-brain/  # 7-Stage Ceremonial Dialogue Engine
│   │   │       ├── voice/tts/         # Edge-TTS Neural Voice Generator
│   │   │       ├── miro/create-board/ # Miro REST API Board Builder
│   │   │       └── email/send-manifestation/ # Email Dispatcher
│   │   ├── context/ThemeContext.tsx   # Dynamic Theme Controller
│   │   ├── lib/validation.ts          # Strict Email & Vague Answer Engine
│   │   └── types/                     # TypeScript Interfaces
├── hero-agent/
│   ├── hero_system_prompt.txt         # Master 7-Stage System Prompt
│   ├── elevenlabs_agent_config.json   # ElevenLabs Agent Blueprint
│   ├── setup_agent.py                 # Automated Agent Provisioner
│   └── hero_voice_tester.html         # Standalone Voice Tester
├── test_hero_conversation.py          # Automated Multi-Turn Test Suite
└── README.md
```

---

## 🔒 Privacy & Ethical AI Standards

- Zero unauthorized selling or sharing of personal reflection data.
- Hero strictly preserves emotional boundaries, never claiming to be a therapist.
- User retains full ownership of their manifestation boards and data.
