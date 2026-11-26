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
from collections import defaultdict, deque
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
RATE_LIMIT_BUCKETS: Dict[str, deque] = defaultdict(deque)
APP_METRICS: Dict[str, Any] = {
    "total_turns": 0,
    "source_counts": {"ceremonial": 0, "claude": 0, "groq": 0, "fallback": 0},
    "tts_errors": 0,
    "rate_limited_requests": 0,
    "total_latency_ms": 0.0,
    "recent_errors": deque(maxlen=10),
}


def _get_client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _check_rate_limit(request: Request, scope: str, max_requests: int = 30, window_sec: int = 60) -> Optional[JSONResponse]:
    """Sliding-window per-IP rate limiter to protect LLM/TTS quotas."""
    ip = _get_client_ip(request)
    key = f"{scope}:{ip}"
    now = time.time()
    q = RATE_LIMIT_BUCKETS[key]
    while q and now - q[0] > window_sec:
        q.popleft()
    if len(q) >= max_requests:
        APP_METRICS["rate_limited_requests"] += 1
        return JSONResponse(
            {"success": False, "error": "Too many requests. Please wait a moment."},
            status_code=429,
            headers={"Retry-After": str(window_sec)},
        )
    q.append(now)
    return None


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
            "rate_limited_requests": APP_METRICS["rate_limited_requests"],
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
        "rate_limited_requests": APP_METRICS["rate_limited_requests"],
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

@app.post("/api/stt")
async def transcribe_whisper(request: Request):
    """Transcribe recorded browser audio via Groq Whisper API (supports Indian English & Hinglish)."""
    limited = _check_rate_limit(request, "stt", max_requests=30, window_sec=60)
    if limited:
        return limited
    if not GROQ_API_KEY:
        return JSONResponse({"success": False, "error": "GROQ_API_KEY not configured"}, status_code=503)

    audio_bytes = await request.body()
    if not audio_bytes or len(audio_bytes) < 800:
        return JSONResponse({"success": True, "text": ""})

    content_type = request.headers.get("content-type", "audio/webm")
    ext = "mp4" if "mp4" in content_type else ("ogg" if "ogg" in content_type else "webm")

    form = aiohttp.FormData()
    form.add_field("file", audio_bytes, filename=f"speech.{ext}", content_type=content_type)
    form.add_field("model", GROQ_WHISPER_MODEL)
    form.add_field("response_format", "json")
    form.add_field("prompt", "Manifest 2027, Janvi, The Sovereign, calmly, sunlit terrace, Hinglish, kuch nahi.")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                data=form,
                timeout=aiohttp.ClientTimeout(total=12.0)
            ) as resp:
                if resp.status != 200:
                    err_txt = await resp.text()
                    return JSONResponse({"success": False, "error": err_txt}, status_code=resp.status)
                data = await resp.json()
                text = (data.get("text") or "").strip()
                return JSONResponse({"success": True, "text": text})
    except Exception as e:
        print(f"[Whisper STT Error] {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

async def synthesize_tts_bytes(text: str, voice_name: str, rate_val: str, pitch_val: str) -> Optional[bytes]:
    """Synthesize MP3 bytes with in-memory cache."""
    if not text or not text.strip():
        return None
    cache_key = f"{voice_name}_{rate_val}_{pitch_val}_{text.strip()}"
    if cache_key in TTS_CACHE:
        return TTS_CACHE[cache_key]
    try:
        communicate = edge_tts.Communicate(text, voice_name, rate=rate_val, pitch=pitch_val)
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

@app.post("/api/chat")
async def process_chat_turn(req: ChatRequest, request: Request):
    """Process conversation turn with full isolated per-user session memory and inline TTS."""
    limited = _check_rate_limit(request, "chat", max_requests=30, window_sec=60)
    if limited:
        return limited

    t0 = time.perf_counter()
    import uuid
    sess_id = req.session_id
    if not sess_id or sess_id.strip() in ["", "default"]:
        sess_id = f"sess_{uuid.uuid4().hex[:12]}"

    safe_user_message = (req.user_message or "")[:2000]
    
    # Isolate session: if starting at stage 1 without an explicit user name, generate fresh brain
    if req.current_stage == 1 and not (req.context and req.context.get("user_name")):
        brain = HeroBrain(context=req.context or {})
        SESSION_STORE[sess_id] = brain
    elif sess_id not in SESSION_STORE:
        brain = HeroBrain(context=req.context or {})
        SESSION_STORE[sess_id] = brain
    else:
        brain = SESSION_STORE[sess_id]
        if req.context:
            brain.context.update(req.context)
            
    brain.current_stage = req.current_stage
    
    turn_result = await asyncio.to_thread(
        brain.process_turn,
        user_message=safe_user_message,
        was_interrupted=req.was_interrupted,
        audio_duration_sec=req.audio_duration_sec or 0.0
    )
    
    # Generate TTS audio inline in the same serverless invocation to eliminate second HTTP round-trip
    emotion = turn_result.get("emotion", {})
    voice_name = req.voice or DEFAULT_VOICE
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

    return JSONResponse({
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
    })

@app.get("/api/tts")
async def generate_tts(
    request: Request,
    text: str, 
    voice: Optional[str] = DEFAULT_VOICE,
    rate: Optional[str] = "+0%",
    pitch: Optional[str] = "+0Hz"
):
    """Synthesize text into complete in-memory MP3 bytes with Content-Length to prevent browser cutoff."""
    limited = _check_rate_limit(request, "tts", max_requests=45, window_sec=60)
    if limited:
        return limited
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
        communicate = edge_tts.Communicate(text, voice_name, rate=rate_val, pitch=pitch_val)
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
