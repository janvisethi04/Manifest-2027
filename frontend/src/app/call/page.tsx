"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Mic, MicOff, PhoneOff, Sparkles, Volume2, ArrowRight, Shield, Layers, AlertCircle, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { loadQuestionnaire, synthesizeProfile } from "@/lib/storage";
import { QuestionnaireData } from "@/types/questionnaire";

interface TranscriptTurn {
  speaker: "hero" | "user";
  text: string;
  stage?: number;
}

export default function CallPage() {
  const router = useRouter();
  const [questionnaire, setQuestionnaire] = useState<QuestionnaireData | null>(null);
  const [callStatus, setCallStatus] = useState<"idle" | "connecting" | "active" | "completed" | "error">("idle");
  const [heroState, setHeroState] = useState<"listening" | "thinking" | "speaking">("listening");
  const [currentStage, setCurrentStage] = useState(1);
  const [callDuration, setCallDuration] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [transcript, setTranscript] = useState<TranscriptTurn[]>([]);
  const [currentUserUtterance, setCurrentUserUtterance] = useState("");
  const [statusMessage, setStatusMessage] = useState("Hero Custom Voice Sanctuary standing by.");

  const recognitionRef = useRef<any>(null);
  const activeAudioRef = useRef<HTMLAudioElement | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const silenceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const wasInterruptedRef = useRef(false);

  useEffect(() => {
    const q = loadQuestionnaire();
    setQuestionnaire(q);

    return () => {
      cleanupSession();
    };
  }, []);

  const cleanupSession = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);
    if (activeAudioRef.current) {
      activeAudioRef.current.pause();
      activeAudioRef.current = null;
    }
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {}
      recognitionRef.current = null;
    }
  };

  // 1. START CEREMONIAL CALL
  const startCall = async () => {
    try {
      setCallStatus("connecting");
      setStatusMessage("Requesting microphone permissions with acoustic echo cancellation...");

      // Request microphone with hardware echo cancellation
      await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      // Initialize Speech Recognition (Chrome/Edge/Safari Web Speech API)
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (!SpeechRecognition) {
        throw new Error("Web Speech Recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
      }

      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = questionnaire?.preferredLanguage?.includes("Hindi") ? "en-IN" : "en-US";

      // BARGE-IN & SPEECH DETECTION
      recognition.onresult = (event: any) => {
        let interimText = "";
        let finalText = "";

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const transcriptChunk = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalText += transcriptChunk;
          } else {
            interimText += transcriptChunk;
          }
        }

        const activeSpoken = (finalText || interimText).trim();

        if (activeSpoken) {
          setCurrentUserUtterance(activeSpoken);

          // BARGE-IN TRIGGER: If Hero is currently speaking, IMMEDIATELY KILL AUDIO
          if (activeAudioRef.current && !activeAudioRef.current.paused) {
            console.log("[Barge-In] User interrupted Hero. Stopping audio playback immediately.");
            activeAudioRef.current.pause();
            activeAudioRef.current.currentTime = 0;
            wasInterruptedRef.current = true;
            setHeroState("listening");
          }

          // Reset silence timer on new speech
          if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);

          // After 850ms of silence after speaking, dispatch user turn to Hero Brain
          silenceTimerRef.current = setTimeout(() => {
            if (activeSpoken.length > 1) {
              handleUserSpeechFinished(activeSpoken);
            }
          }, 850);
        }
      };

      recognition.onerror = (event: any) => {
        if (event.error !== "no-speech") {
          console.warn("[STT Error]", event.error);
        }
      };

      recognition.onend = () => {
        // Keep listening continuously during active call unless muted
        if (callStatus === "active" && !isMuted && recognitionRef.current) {
          try {
            recognition.start();
          } catch {}
        }
      };

      recognition.start();
      recognitionRef.current = recognition;

      setCallStatus("active");
      startTimer();

      // Trigger Stage 1 Opening Greeting
      executeHeroTurn("", 1, false);

    } catch (err: any) {
      console.error("Failed to start voice call:", err);
      setStatusMessage(err.message || "Failed to initialize audio sanctuary.");
      setCallStatus("error");
    }
  };

  // 2. DISPATCH USER UTTERANCE TO BRAIN
  const handleUserSpeechFinished = (spokenText: string) => {
    setCurrentUserUtterance("");
    setTranscript((prev) => [...prev, { speaker: "user", text: spokenText }]);
    
    // Check if was an interruption
    const wasInterrupted = wasInterruptedRef.current;
    wasInterruptedRef.current = false;

    executeHeroTurn(spokenText, currentStage, wasInterrupted);
  };

  // 3. EXECUTE HERO BRAIN TURN & PLAY TTS
  const executeHeroTurn = async (userMsg: string, stage: number, wasInterrupted: boolean) => {
    setHeroState("thinking");
    setStatusMessage("Hero is reflecting and attuning...");

    try {
      const q = questionnaire || loadQuestionnaire();

      const brainRes = await fetch("/api/voice/hero-brain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userMessage: userMsg,
          currentStage: stage,
          history: transcript,
          context: {
            user_name: q.fullName || "friend",
            preferred_language: q.preferredLanguage,
            pride2026: q.pride2026,
            pride2027: q.pride2027,
            dayInTheLife2027: q.dayInTheLife2027,
            movieScene: q.movieScene,
            coreQualities: q.coreQualities,
            pastGroundingStory: q.pastGroundingStory,
            characterNameIdea: q.characterNameIdea,
          },
          wasInterrupted,
        }),
      });

      const brainData = await brainRes.json();
      if (!brainData.success) {
        throw new Error(brainData.error || "Hero Brain turn failed");
      }

      const { heroResponse, currentStage: nextStage, isCallEnding } = brainData;
      setCurrentStage(nextStage);

      // Add to transcript
      setTranscript((prev) => [...prev, { speaker: "hero", text: heroResponse, stage: nextStage }]);

      // Generate Neural Voice with Edge-TTS
      setStatusMessage("Hero is speaking...");
      setHeroState("speaking");

      const ttsRes = await fetch("/api/voice/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: heroResponse,
          voice: q.preferredLanguage?.includes("Hindi") ? "hi-IN-MadhurNeural" : "en-US-ChristopherNeural",
        }),
      });

      if (!ttsRes.ok) {
        throw new Error("TTS generation failed");
      }

      const audioBlob = await ttsRes.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      activeAudioRef.current = audio;

      audio.onended = () => {
        setHeroState("listening");
        setStatusMessage("Hero is listening to your words...");

        if (isCallEnding) {
          handleCeremonyCompleted();
        }
      };

      await audio.play();

    } catch (err: any) {
      console.error("Hero turn error:", err);
      setStatusMessage("Hero paused. You can speak or retry.");
      setHeroState("listening");
    }
  };

  // 4. CALL DURATION TIMER (9 MIN LIMIT)
  const startTimer = () => {
    setCallDuration(0);
    timerRef.current = setInterval(() => {
      setCallDuration((prev) => {
        if (prev >= 540) { // 9 minutes strict limit
          endCall();
          return 540;
        }
        return prev + 1;
      });
    }, 1000);
  };

  const endCall = () => {
    cleanupSession();
    handleCeremonyCompleted();
  };

  const handleCeremonyCompleted = () => {
    cleanupSession();
    setCallStatus("completed");
    setStatusMessage("Ceremony Complete. 'Consider your manifestation ready. We'll come back within 15 days with a surprise.'");

    if (questionnaire) {
      synthesizeProfile(questionnaire);
    }
  };

  const formatTimer = (seconds: number) => {
    const mins = String(Math.floor(seconds / 60)).padStart(2, "0");
    const secs = String(seconds % 60).padStart(2, "0");
    return `${mins}:${secs}`;
  };

  return (
    <div className="min-h-[85vh] py-10 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto flex flex-col items-center justify-center space-y-6">
      {/* Header Info */}
      <div className="text-center space-y-2">
        <Badge variant="gold" className="mx-auto">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Manifest 2027 Custom Voice Engine (Zero-Cost Local Pipeline)</span>
        </Badge>
        <h1 className="font-serif text-3xl sm:text-5xl font-bold" style={{ color: "var(--color-text)" }}>
          Hero Voice Sanctuary
        </h1>
        <p className="text-xs sm:text-sm" style={{ color: "var(--color-muted)" }}>
          Speaking with <span className="font-semibold" style={{ color: "var(--color-text)" }}>{questionnaire?.fullName || "Friend"}</span> • 7-Stage Projection & Grounding Ceremony
        </p>
      </div>

      {/* Main Calling Room Card */}
      <Card variant="default" className="w-full p-6 sm:p-10 shadow-dreamy-lg flex flex-col items-center relative overflow-hidden">
        
        {/* Dynamic Glow Halo */}
        <div
          className={`absolute inset-0 blur-3xl -z-10 transition-all duration-700 ${
            heroState === "speaking"
              ? "scale-125 opacity-90 animate-pulse"
              : heroState === "thinking"
              ? "scale-105 opacity-60"
              : "scale-95 opacity-40"
          }`}
          style={{ background: "radial-gradient(circle, var(--color-glow) 0%, transparent 70%)" }}
        />

        {/* The Audio-Reactive Hero Orb */}
        <div className="relative w-52 h-52 sm:w-60 sm:h-60 flex items-center justify-center my-4">
          <div
            className={`absolute inset-0 rounded-full blur-2xl transition-all duration-500 ${
              heroState === "speaking" ? "scale-125 opacity-100" : "scale-100 opacity-60"
            }`}
            style={{ background: "var(--color-glow)" }}
          />

          <div
            className={`relative w-40 h-40 sm:w-44 sm:h-44 rounded-full border-2 border-white/60 shadow-glow flex flex-col items-center justify-center transition-all duration-300 ${
              heroState === "speaking"
                ? "scale-110 shadow-2xl"
                : heroState === "thinking"
                ? "scale-105 animate-pulse"
                : "scale-100"
            }`}
            style={{ background: "var(--color-card)", borderColor: "var(--color-accent)" }}
          >
            <Sparkles className="w-8 h-8 mb-1" style={{ color: "var(--color-accent)" }} />
            <span className="font-serif text-2xl font-bold leading-none" style={{ color: "var(--color-text)" }}>Hero</span>
            <span className="text-[10px] tracking-widest uppercase font-semibold mt-1" style={{ color: "var(--color-muted)" }}>
              {callStatus === "active"
                ? heroState === "speaking"
                  ? "Speaking (Barge-in Active)"
                  : heroState === "thinking"
                  ? "Attuning..."
                  : "Listening to You..."
                : callStatus === "connecting"
                ? "Connecting..."
                : callStatus === "completed"
                ? "Ceremony Complete"
                : "Standing By"}
            </span>
          </div>
        </div>

        {/* 9-Minute Call Timer & Stage Badge */}
        {callStatus === "active" && (
          <div className="mb-4 flex items-center gap-3">
            <span className="px-3 py-1 rounded-full text-xs font-mono font-bold flex items-center gap-1.5" style={{ background: "rgba(0,0,0,0.3)", border: "1px solid var(--color-border)", color: "var(--color-text)" }}>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>{formatTimer(callDuration)} / 09:00</span>
            </span>

            <span className="px-3 py-1 rounded-full text-xs font-semibold" style={{ background: "rgba(204,164,86,0.15)", border: "1px solid var(--color-accent)", color: "var(--color-accent)" }}>
              Stage {Math.min(currentStage, 7)} of 7
            </span>
          </div>
        )}

        {/* Status Prompt Text */}
        <p className="text-center text-xs sm:text-sm max-w-md mb-6 font-medium" style={{ color: "var(--color-muted)" }}>
          {statusMessage}
        </p>

        {/* Real-Time User Speech Bubble (Shows what user is saying in real time) */}
        {currentUserUtterance && callStatus === "active" && (
          <div className="w-full max-w-md p-3 mb-4 rounded-xl bg-purple-500/10 border border-purple-500/30 text-xs text-purple-200 text-center animate-pulse">
            You: &quot;{currentUserUtterance}&quot;
          </div>
        )}

        {/* Call Action Controls */}
        <div className="flex flex-wrap items-center justify-center gap-4">
          {callStatus === "idle" && (
            <Button size="lg" variant="primary" onClick={startCall} className="shadow-lg">
              <Mic className="w-5 h-5 mr-2" />
              <span>Begin Voice Ceremony (Speak with Hero)</span>
            </Button>
          )}

          {callStatus === "connecting" && (
            <Button size="lg" variant="primary" disabled isLoading>
              <span>Connecting Custom Engine...</span>
            </Button>
          )}

          {callStatus === "active" && (
            <>
              <Button
                variant="outline"
                size="md"
                onClick={() => setIsMuted(!isMuted)}
                className="rounded-full"
              >
                {isMuted ? <MicOff className="w-4 h-4 mr-1.5 text-rose-400" /> : <Mic className="w-4 h-4 mr-1.5" />}
                <span>{isMuted ? "Unmute Mic" : "Mute Mic"}</span>
              </Button>

              <Button
                variant="primary"
                size="md"
                onClick={endCall}
                className="bg-rose-600 hover:bg-rose-700 from-rose-600 to-rose-700 rounded-full shadow-md"
              >
                <PhoneOff className="w-4 h-4 mr-1.5" />
                <span>End Ceremony</span>
              </Button>
            </>
          )}

          {callStatus === "completed" && (
            <Button
              size="lg"
              variant="gold"
              onClick={() => router.push("/board")}
              className="shadow-gold-glow"
            >
              <Layers className="w-5 h-5 mr-2" />
              <span>Generate & View Miro Manifestation Board</span>
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          )}

          {callStatus === "error" && (
            <Button size="md" variant="primary" onClick={startCall}>
              <RefreshCw className="w-4 h-4 mr-1.5" />
              <span>Retry Voice Call</span>
            </Button>
          )}
        </div>

        {/* Live Conversation Transcript History */}
        {transcript.length > 0 && (
          <div className="w-full mt-8 pt-6 border-t space-y-3 max-h-48 overflow-y-auto text-xs" style={{ borderColor: "var(--color-border)" }}>
            <p className="font-semibold uppercase tracking-wider text-[11px]" style={{ color: "var(--color-accent)" }}>
              Live Ceremony Dialogue
            </p>
            {transcript.map((t, idx) => (
              <div
                key={idx}
                className={`p-2.5 rounded-xl ${
                  t.speaker === "hero"
                    ? "bg-purple-950/40 border border-purple-800/40 text-purple-200"
                    : "bg-white/5 border border-white/10 text-white/90 text-right"
                }`}
              >
                <span className="font-bold uppercase text-[10px] block opacity-70 mb-0.5">
                  {t.speaker === "hero" ? "Hero" : questionnaire?.fullName || "You"}
                </span>
                <span>{t.text}</span>
              </div>
            ))}
          </div>
        )}

        {/* Bottom Ceremonial Seal */}
        <div className="mt-8 pt-4 border-t w-full text-center" style={{ borderColor: "var(--color-border)" }}>
          <p className="font-serif text-xs italic" style={{ color: "var(--color-muted)" }}>
            &quot;Consider your manifestation ready. We&apos;ll come back to you within the next 15 days with a surprise.&quot;
          </p>
        </div>
      </Card>
    </div>
  );
}
