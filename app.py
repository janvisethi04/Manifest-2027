"""
Hero Voice Agent: Full Studio Application
Serves the Manifest 2027 Mirror Chamber UI with:
- Sentiment & Emotion Context Awareness
- Emotionally Attuned 7-Stage Brain
- Dynamic SSML Voice Modulation (rate & pitch) via Edge-TTS
- Zero-latency Barge-in (<10ms)
"""
import os
import sys
import asyncio
import tempfile
import webbrowser
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import edge_tts

from brain import HeroBrain
from config import DEFAULT_VOICE, HINDI_VOICE, FEMALE_VOICE

app = FastAPI(title="Manifest 2027 Voice Agent")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

SESSION_STORE: Dict[str, HeroBrain] = {}

class ChatRequest(BaseModel):
    user_message: str = ""
    was_interrupted: bool = False
    current_stage: int = 1
    voice: Optional[str] = DEFAULT_VOICE
    context: Optional[Dict[str, Any]] = None
    audio_duration_sec: Optional[float] = 0.0
    session_id: Optional[str] = "default"

@app.get("/", response_class=HTMLResponse)
async def serve_agent_ui():
    """Serve the Manifest 2027 Mirror Chamber UI."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Voice Agent UI file not found</h1>", status_code=404)

@app.post("/api/chat")
async def process_chat_turn(req: ChatRequest):
    """Process conversation turn with full persistent session sentiment, prosody & emotional arc awareness."""
    sess_id = req.session_id or "default"
    
    # Maintain stateful session brain
    if req.current_stage == 1 or sess_id not in SESSION_STORE:
        brain = HeroBrain(context=req.context or {})
        SESSION_STORE[sess_id] = brain
    else:
        brain = SESSION_STORE[sess_id]
        if req.context:
            brain.context.update(req.context)
            
    brain.current_stage = req.current_stage
    
    turn_result = brain.process_turn(
        user_message=req.user_message,
        was_interrupted=req.was_interrupted,
        audio_duration_sec=req.audio_duration_sec or 0.0
    )
    
    return JSONResponse({
        "success": True,
        "hero_response": turn_result["hero_response"],
        "current_stage": turn_result["current_stage"],
        "stage_name": turn_result["stage_name"],
        "is_finished": turn_result["is_finished"],
        "was_interrupted": turn_result["was_interrupted"],
        "user_name": turn_result.get("manifestation_board", {}).get("user_name") or brain.user_name,
        "emotion": turn_result.get("emotion", {}),
        "prosody": turn_result.get("prosody", {}),
        "trajectory": turn_result.get("trajectory", []),
        "manifestation_board": turn_result.get("manifestation_board", {})
    })

@app.get("/api/tts")
async def generate_tts(
    text: str, 
    voice: Optional[str] = DEFAULT_VOICE,
    rate: Optional[str] = "+0%",
    pitch: Optional[str] = "+0Hz"
):
    """Synthesize text with emotional modulation (rate, pitch) streaming MP3 chunks directly for ultra-low latency."""
    if not text or not text.strip():
        return JSONResponse({"error": "Empty text"}, status_code=400)
    
    voice_name = voice or DEFAULT_VOICE
    rate_val = rate or "+0%"
    pitch_val = pitch or "+0Hz"
    
    async def audio_stream():
        try:
            communicate = edge_tts.Communicate(text, voice_name, rate=rate_val, pitch=pitch_val)
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
        except Exception as e:
            print(f"[TTS Stream Error] {e}")
            # Fallback to unmodulated stream if error occurred
            try:
                fallback = edge_tts.Communicate(text, voice_name)
                async for chunk in fallback.stream():
                    if chunk["type"] == "audio":
                        yield chunk["data"]
            except Exception as e2:
                print(f"[TTS Fallback Error] {e2}")

    return StreamingResponse(
        audio_stream(),
        media_type="audio/mpeg",
        headers={
            "Cache-Control": "no-cache",
            "Content-Disposition": "inline; filename=speech.mp3"
        }
    )

def run_app(port: int = 8000, open_browser: bool = False):
    print("=" * 65)
    print("🕯️  HERO: MANIFEST 2027 VOICE AGENT STUDIO")
    print(f"🌐  Server running at: http://localhost:{port}")
    print("🧠  Features: Sentiment & Emotion Engine | 7-Stage Brain | Edge-TTS")
    print("=" * 65)
    
    if open_browser:
        try:
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass
            
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_app(port=port)
