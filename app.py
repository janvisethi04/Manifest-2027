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
import time
import json
import base64
import asyncio
import tempfile
import webbrowser
from collections import deque
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse, Response
from pydantic import BaseModel
import uvicorn
import edge_tts
import aiohttp

from brain import HeroBrain
from config import DEFAULT_VOICE, HINDI_VOICE, FEMALE_VOICE, USE_VPS_CLAUDE, GROQ_API_KEY, GROQ_WHISPER_MODEL

app = FastAPI(title="Manifest 2027 Voice Agent")

APP_START_TIME = time.time()
APP_METRICS: Dict[str, Any] = {
    "total_turns": 0,
    "source_counts": {"ceremonial": 0, "claude": 0, "groq": 0, "fallback": 0},
    "tts_errors": 0,
    "total_latency_ms": 0.0,
    "recent_errors": deque(maxlen=10),
}


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

SESSION_STORE: Dict[str, HeroBrain] = {}
TTS_CACHE: Dict[str, bytes] = {}

class ChatRequest(BaseModel):
    user_message: str = ""
    was_interrupted: bool = False
    current_stage: int = 1
    voice: Optional[str] = DEFAULT_VOICE
    context: Optional[Dict[str, Any]] = None
    audio_duration_sec: Optional[float] = 0.0
    session_id: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def serve_agent_ui():
    """Serve the Manifest 2027 Mirror Chamber UI."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Voice Agent UI file not found</h1>", status_code=404)

@app.get("/api/health")
async def health_check():
    """Health & readiness check for uptime monitors."""
    turns = APP_METRICS["total_turns"]
    avg_ms = round(APP_METRICS["total_latency_ms"] / turns, 1) if turns > 0 else 0.0
    return JSONResponse({
        "status": "ok",
        "service": "manifest-2027",
        "uptime_sec": round(time.time() - APP_START_TIME, 1),
        "checks": {
            "vps_claude_enabled": USE_VPS_CLAUDE,
            "groq_configured": bool(GROQ_API_KEY),
            "active_sessions": len(SESSION_STORE),
            "tts_cache_size": len(TTS_CACHE),
        },
        "metrics": {
            "total_turns": turns,
            "avg_turn_latency_ms": avg_ms,
            "source_counts": APP_METRICS["source_counts"],
            "tts_errors": APP_METRICS["tts_errors"],
        },
    })


@app.get("/api/metrics")
async def get_metrics():
    """Structured telemetry & recent non-sensitive errors."""
    turns = APP_METRICS["total_turns"]
    return JSONResponse({
        "total_turns": turns,
        "avg_turn_latency_ms": round(APP_METRICS["total_latency_ms"] / turns, 1) if turns > 0 else 0.0,
        "source_counts": APP_METRICS["source_counts"],
        "tts_errors": APP_METRICS["tts_errors"],
        "recent_errors": list(APP_METRICS["recent_errors"]),
    })


@app.post("/api/reset")
async def reset_session(request: Request):
    """Explicitly wipe session memory for fresh user ceremony."""
    try:
        body = await request.json()
        sess_id = body.get("session_id")
        if sess_id and sess_id in SESSION_STORE:
            del SESSION_STORE[sess_id]
    except Exception:
        pass
    return JSONResponse({"success": True, "message": "Session reset cleanly"})

@app.get("/api/stt/status")
async def stt_status():
    """Report whether server-side Groq Whisper STT is configured."""
    return JSONResponse({
        "whisper_enabled": bool(GROQ_API_KEY),
        "provider": "groq-whisper" if GROQ_API_KEY else "web-speech-en-IN",
        "model": GROQ_WHISPER_MODEL if GROQ_API_KEY else None
    })

async def _transcribe_whisper_bytes(audio_bytes: bytes, content_type: str = "audio/webm") -> str:
    """Transcribe raw audio bytes via Groq whisper-large-v3-turbo."""
    if not GROQ_API_KEY or not audio_bytes or len(audio_bytes) < 800:
        return ""
    ext = "mp4" if "mp4" in content_type else ("ogg" if "ogg" in content_type else "webm")
    form = aiohttp.FormData()
    form.add_field("file", audio_bytes, filename=f"speech.{ext}", content_type=content_type)
    form.add_field("model", GROQ_WHISPER_MODEL)
    form.add_field("response_format", "json")
    form.add_field("prompt", "Manifest 2027, Janvi, The Sovereign, calmly, sunlit terrace, Hinglish, kuch nahi.")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            data=form,
            timeout=aiohttp.ClientTimeout(total=10.0)
        ) as resp:
            if resp.status != 200:
                err_txt = await resp.text()
                raise RuntimeError(f"Groq Whisper HTTP {resp.status}: {err_txt[:150]}")
            data = await resp.json()
            return (data.get("text") or "").strip()


@app.post("/api/stt")
async def transcribe_whisper(request: Request):
    """Transcribe recorded browser audio via Groq Whisper API (supports Indian English & Hinglish)."""
    if not GROQ_API_KEY:
        return JSONResponse({"success": False, "error": "GROQ_API_KEY not configured"}, status_code=503)

    audio_bytes = await request.body()
    if not audio_bytes or len(audio_bytes) < 800:
        return JSONResponse({"success": True, "text": ""})

    content_type = request.headers.get("content-type", "audio/webm")
    try:
        text = await _transcribe_whisper_bytes(audio_bytes, content_type)
        return JSONResponse({"success": True, "text": text})
    except Exception as e:
        print(f"[Whisper STT Error] {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

def _naturalize_prosody(rate_val: str, pitch_val: str) -> tuple[str, str]:
    """Keep Edge-TTS rate & pitch subtle so emotional modulation sounds warm, never robotic."""
    try:
        r = int(str(rate_val).replace("%", "").replace("+", ""))
        r = max(-6, min(4, r))
        rate_clean = f"{r:+d}%"
    except Exception:
        rate_clean = "-2%"
    try:
        p = int(str(pitch_val).lower().replace("hz", "").replace("+", ""))
        p = max(-2, min(2, p))
        pitch_clean = f"{p:+d}Hz"
    except Exception:
        pitch_clean = "+0Hz"
    return rate_clean, pitch_clean


async def synthesize_tts_bytes(text: str, voice_name: str, rate_val: str, pitch_val: str) -> Optional[bytes]:
    """Synthesize MP3 bytes with in-memory cache and natural emotional prosody."""
    if not text or not text.strip():
        return None
    is_multilingual = "Multilingual" in (voice_name or "")
    rate_clean, pitch_clean = ("+0%", "+0Hz") if is_multilingual else _naturalize_prosody(rate_val, pitch_val)
    cache_key = f"{voice_name}_{rate_clean}_{pitch_clean}_{text.strip()}"
    if cache_key in TTS_CACHE:
        return TTS_CACHE[cache_key]
    try:
        communicate = (
            edge_tts.Communicate(text, voice_name)
            if is_multilingual
            else edge_tts.Communicate(text, voice_name, rate=rate_clean, pitch=pitch_clean)
        )
        chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        audio_bytes = b"".join(chunks)
        if audio_bytes and len(TTS_CACHE) < 200:
            TTS_CACHE[cache_key] = audio_bytes
        return audio_bytes or None
    except Exception as e:
        APP_METRICS["tts_errors"] += 1
        APP_METRICS["recent_errors"].append({"type": "tts_inline", "error": str(e)[:120], "ts": int(time.time())})
        print(f"[TTS Inline Error] {e}")
        return None

async def _execute_chat_turn(
    user_message: str,
    was_interrupted: bool,
    current_stage: int,
    voice: Optional[str],
    context: Optional[Dict[str, Any]],
    audio_duration_sec: float,
    session_id: Optional[str],
    extra_fields: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    """Shared turn execution + inline TTS + metrics logging for /api/chat and /api/voice-turn."""
    t0 = time.perf_counter()
    import uuid
    sess_id = session_id
    if not sess_id or sess_id.strip() in ["", "default"]:
        sess_id = f"sess_{uuid.uuid4().hex[:12]}"

    safe_user_message = (user_message or "")[:2000]

    if current_stage == 1 and not (context and context.get("user_name")):
        brain = HeroBrain(context=context or {})
        SESSION_STORE[sess_id] = brain
    elif sess_id not in SESSION_STORE:
        brain = HeroBrain(context=context or {})
        SESSION_STORE[sess_id] = brain
    else:
        brain = SESSION_STORE[sess_id]
        if context:
            brain.context.update(context)

    brain.current_stage = current_stage

    turn_result = await asyncio.to_thread(
        brain.process_turn,
        user_message=safe_user_message,
        was_interrupted=was_interrupted,
        audio_duration_sec=audio_duration_sec or 0.0
    )

    emotion = turn_result.get("emotion", {})
    voice_name = voice or DEFAULT_VOICE
    rate_val = emotion.get("voice_rate", "+0%")
    pitch_val = emotion.get("voice_pitch", "+0Hz")
    audio_bytes = await synthesize_tts_bytes(turn_result["hero_response"], voice_name, rate_val, pitch_val)
    audio_b64 = base64.b64encode(audio_bytes).decode("ascii") if audio_bytes else None

    src = turn_result.get("source", "fallback")
    latency_ms = round((time.perf_counter() - t0) * 1000, 1)
    APP_METRICS["total_turns"] += 1
    APP_METRICS["total_latency_ms"] += latency_ms
    APP_METRICS["source_counts"][src] = APP_METRICS["source_counts"].get(src, 0) + 1
    print(json.dumps({
        "event": "chat_turn",
        "stage": turn_result["current_stage"],
        "stage_name": turn_result["stage_name"],
        "source": src,
        "latency_ms": latency_ms,
        "audio_bytes": len(audio_bytes) if audio_bytes else 0,
    }))

    payload = {
        "success": True,
        "session_id": sess_id,
        "source": src,
        "hero_response": turn_result["hero_response"],
        "audio_base64": audio_b64,
        "current_stage": turn_result["current_stage"],
        "stage_name": turn_result["stage_name"],
        "is_finished": turn_result["is_finished"],
        "was_interrupted": turn_result["was_interrupted"],
        "user_name": turn_result.get("manifestation_board", {}).get("user_name") or brain.user_name,
        "emotion": emotion,
        "prosody": turn_result.get("prosody", {}),
        "trajectory": turn_result.get("trajectory", []),
        "manifestation_board": turn_result.get("manifestation_board", {})
    }
    if extra_fields:
        payload.update(extra_fields)
    return JSONResponse(payload)


@app.post("/api/chat")
async def process_chat_turn(req: ChatRequest):
    """Process text conversation turn with full isolated per-user session memory and inline TTS."""
    return await _execute_chat_turn(
        user_message=req.user_message,
        was_interrupted=req.was_interrupted,
        current_stage=req.current_stage,
        voice=req.voice,
        context=req.context,
        audio_duration_sec=req.audio_duration_sec or 0.0,
        session_id=req.session_id,
    )


@app.post("/api/voice-turn")
async def process_voice_turn(
    request: Request,
    session_id: Optional[str] = None,
    current_stage: int = 1,
    voice: Optional[str] = DEFAULT_VOICE,
    audio_duration_sec: float = 0.0,
    user_name: Optional[str] = "",
):
    """Single-hop voice turn: Groq Whisper STT -> Brain -> Inline Edge-TTS."""
    if not GROQ_API_KEY:
        return JSONResponse({"success": False, "error": "GROQ_API_KEY not configured"}, status_code=503)

    audio_bytes = await request.body()
    content_type = request.headers.get("content-type", "audio/webm")
    t_stt = time.perf_counter()
    try:
        transcript = await _transcribe_whisper_bytes(audio_bytes, content_type)
    except Exception as e:
        APP_METRICS["recent_errors"].append({"type": "whisper_voice_turn", "error": str(e)[:120], "ts": int(time.time())})
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

    stt_ms = round((time.perf_counter() - t_stt) * 1000, 1)
    # Ignore empty or non-word background noise clips
    if not transcript or len(transcript.strip()) < 2 or not any(c.isalpha() for c in transcript):
        return JSONResponse({"success": True, "empty_speech": True, "stt_ms": stt_ms})

    ctx = {"user_name": user_name} if user_name else {}
    return await _execute_chat_turn(
        user_message=transcript,
        was_interrupted=False,
        current_stage=current_stage,
        voice=voice,
        context=ctx,
        audio_duration_sec=audio_duration_sec,
        session_id=session_id,
        extra_fields={"empty_speech": False, "user_transcript": transcript, "stt_ms": stt_ms},
    )

@app.get("/api/tts")
async def generate_tts(
    text: str, 
    voice: Optional[str] = DEFAULT_VOICE,
    rate: Optional[str] = "+0%",
    pitch: Optional[str] = "+0Hz"
):
    """Synthesize text into complete in-memory MP3 bytes with Content-Length to prevent browser cutoff."""
    if not text or not text.strip():
        return JSONResponse({"error": "Empty text"}, status_code=400)
    
    voice_name = voice or DEFAULT_VOICE
    rate_val = rate or "+0%"
    pitch_val = pitch or "+0Hz"
    
    cache_key = f"{voice_name}_{rate_val}_{pitch_val}_{text.strip()}"
    if cache_key in TTS_CACHE:
        cached_bytes = TTS_CACHE[cache_key]
        return Response(
            content=cached_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Length": str(len(cached_bytes)),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=86400",
                "X-TTS-Cache": "HIT"
            }
        )
    
    try:
        is_multilingual = "Multilingual" in (voice_name or "")
        communicate = (
            edge_tts.Communicate(text, voice_name)
            if is_multilingual
            else edge_tts.Communicate(text, voice_name, rate=rate_val, pitch=pitch_val)
        )
        chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        audio_bytes = b"".join(chunks)
        if len(audio_bytes) > 0 and len(TTS_CACHE) < 200:
            TTS_CACHE[cache_key] = audio_bytes
        
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Length": str(len(audio_bytes)),
                "Accept-Ranges": "bytes",
                "Cache-Control": "no-cache",
                "Content-Disposition": "inline; filename=speech.mp3"
            }
        )
    except Exception as e:
        print(f"[TTS Stream Error] {e}")
        try:
            fallback = edge_tts.Communicate(text, voice_name)
            chunks = []
            async for chunk in fallback.stream():
                if chunk["type"] == "audio":
                    chunks.append(chunk["data"])
            fallback_bytes = b"".join(chunks)
            return Response(
                content=fallback_bytes,
                media_type="audio/mpeg",
                headers={
                    "Content-Length": str(len(fallback_bytes)),
                    "Accept-Ranges": "bytes",
                    "Cache-Control": "no-cache"
                }
            )
        except Exception as e2:
            print(f"[TTS Fallback Error] {e2}")
            return JSONResponse({"error": str(e2)}, status_code=500)

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
