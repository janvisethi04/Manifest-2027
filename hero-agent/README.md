# HERO — ELEVENLABS CONVERSATIONAL AI AGENT (MANIFEST 2027)

This directory contains the production-ready **Hero Voice Agent** configuration for ElevenLabs Conversational AI, built strictly according to the **Hero Master System Prompt**.

---

## 1. Files in this Directory

- **`hero_system_prompt.txt`**: The exact Master System Prompt (preserving the 7-stage conversation structure, emotional grounding, mirror reflection, and exact closing statement).
- **`elevenlabs_agent_config.json`**: Complete agent configuration payload (Prompt, First Message, Dynamic Variables, Voice settings `eleven_turbo_v2_5`, 9-minute duration cutoff, turn-taking, and post-call data extraction schema).
- **`setup_agent.py`**: Zero-dependency Python script to automatically create/provision this agent in your ElevenLabs account via API.
- **`hero_voice_tester.html`**: A standalone, beautiful voice-tester web app using the official `@elevenlabs/client` SDK. Open in any browser to speak directly to Hero with your microphone.

---

## 2. How to Set Up the Hero Agent in ElevenLabs

You can choose either **Option A (Automated Script)** or **Option B (ElevenLabs Dashboard)**:

### Option A: 1-Click Python Automation Script
Run the setup script with your ElevenLabs API Key (`xi-api-key`):

```bash
cd "C:\Users\JANVI\.gemini\antigravity\scratch\converse-ai-manifest-2027\hero-agent"
python setup_agent.py <YOUR_ELEVENLABS_API_KEY>
```

This will:
1. Connect to ElevenLabs Conversational AI API (`POST /v1/convai/agents/create`).
2. Register the complete 7-stage Hero system prompt, dynamic variables, voice settings, and post-call analysis schema.
3. Print your new **Agent ID** (e.g. `agent_7a8b9c...`) and save it to `hero_agent_credentials.json`.

---

### Option B: Manual Setup in ElevenLabs Dashboard
1. Go to [ElevenLabs Conversational AI Dashboard](https://elevenlabs.io/app/conversational-ai).
2. Click **Create Agent** -> **Blank Template**.
3. Name: `Hero – Manifest 2027`.
4. Paste the content of `hero_system_prompt.txt` into the **System Prompt**.
5. Set **First Message**:
   ```
   Welcome, {{user_name}}. A few minutes to dream out loud about your 2027. How does it feel to step into this space with us today?
   ```
6. Set **Voice**: Select **George** (`JBFqnCBsd6RMkjVDRZzb`) or **Rachel** (`21m00Tcm4TlvDq8ikWAM`).
7. Model: **Eleven Turbo v2.5** (recommended for lowest latency).
8. Under **Conversation Settings**:
   - Max Duration: `540` seconds (9 minutes).
9. Under **Dynamic Variables**, add:
   - `user_name` (Default: `Friend`)
   - `preferred_language` (Default: `English / Hinglish`)
   - `pre_call_context` (Default: `Ready for 2027 manifestation reflection`)
   - `user_qualities` (Default: `Curious, thoughtful, resilient`)

---

## 3. How to Test & Talk with Hero Right Now

1. Double click or open [`hero_voice_tester.html`](file:///C:/Users/JANVI/.gemini/antigravity/scratch/converse-ai-manifest-2027/hero-agent/hero_voice_tester.html) in your Google Chrome or Microsoft Edge browser.
2. Enter your **Agent ID**.
3. Enter your Name.
4. Click **"Connect with Hero"** and grant microphone permissions.
5. Speak naturally! Hero will:
   - Greet you warmly by name.
   - Lead you through the 7-stage ceremony.
   - Listen to your 2026 pride, bridge the audacity gap for 2027, imagine your character's movie scene, ground it in a real past achievement, mirror it back, and close with the exact promise:
     *"Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."*
