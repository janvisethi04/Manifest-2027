import { NextRequest, NextResponse } from "next/server";
import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs";
import path from "path";
import os from "os";

const execAsync = promisify(exec);

export async function POST(req: NextRequest) {
  try {
    const { text, voice } = await req.json();

    if (!text || typeof text !== "string") {
      return NextResponse.json({ error: "Text is required" }, { status: 400 });
    }

    // Default voice: Christopher (warm, deep, reflective human tone)
    const selectedVoice = voice || "en-US-ChristopherNeural";

    // Create temp file for output mp3
    const tempFileName = `hero_tts_${Date.now()}_${Math.random().toString(36).substring(2, 7)}.mp3`;
    const tempFilePath = path.join(os.tmpdir(), tempFileName);

    // Clean text of quotes and special characters for command line safety
    const sanitizedText = text
      .replace(/"/g, "'")
      .replace(/[\r\n]+/g, " ")
      .trim();

    // Call edge-tts Python module
    const command = `python -m edge_tts --voice "${selectedVoice}" --text "${sanitizedText}" --write-media "${tempFilePath}"`;
    await execAsync(command);

    if (!fs.existsSync(tempFilePath)) {
      throw new Error("TTS failed to generate audio file");
    }

    const audioBuffer = fs.readFileSync(tempFilePath);

    // Clean up temp file
    try {
      fs.unlinkSync(tempFilePath);
    } catch {}

    return new NextResponse(audioBuffer, {
      status: 200,
      headers: {
        "Content-Type": "audio/mpeg",
        "Content-Length": audioBuffer.length.toString(),
        "Cache-Control": "no-cache",
      },
    });

  } catch (error: any) {
    console.error("TTS Generation Error:", error);
    return NextResponse.json({ error: error.message || "Failed to generate speech" }, { status: 500 });
  }
}
