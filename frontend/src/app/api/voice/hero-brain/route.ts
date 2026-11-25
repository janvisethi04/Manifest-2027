import { NextRequest, NextResponse } from "next/server";

interface BrainRequest {
  userMessage?: string;
  currentStage: number; // 1 to 7
  history: { speaker: "hero" | "user"; text: string }[];
  context: {
    user_name: string;
    preferred_language?: string;
    pride2026?: string;
    pride2027?: string;
    dayInTheLife2027?: string;
    movieScene?: string;
    coreQualities?: string[];
    pastGroundingStory?: string;
    characterNameIdea?: string;
  };
  wasInterrupted?: boolean;
}

export async function POST(req: NextRequest) {
  try {
    const body: BrainRequest = await req.json();
    const { userMessage = "", currentStage = 1, history = [], context, wasInterrupted = false } = body;

    const name = context.user_name || "friend";
    const userMsgClean = userMessage.trim().toLowerCase();

    let nextStage = currentStage;
    let heroResponse = "";
    let isCallEnding = false;

    // Handle Interruption / Barge-in gracefully
    let interruptionPrefix = "";
    if (wasInterrupted) {
      interruptionPrefix = "Got you. ";
    }

    // Check if user's answer is brief / vague
    const isBrief = userMsgClean.length > 0 && userMsgClean.length < 8;

    switch (currentStage) {
      // 1. OPEN
      case 1:
        heroResponse = `Welcome, ${name}. A few minutes to dream out loud about your 2027. We are here as a mirror of your own potential. Tell us, what is the one thing from 2026 you're really proud of?`;
        nextStage = 2;
        break;

      // 2. PRIDE 2026 (Savouring)
      case 2:
        if (!userMessage && context.pride2026) {
          heroResponse = `${interruptionPrefix}Looking at what you noted about 2026—"${context.pride2026}"—let yourself really savour that. What did that feat teach you about your strength?`;
        } else if (isBrief) {
          heroResponse = `${interruptionPrefix}Even a small moment counts. Take a breath with us. What is one thing, big or quiet, that you did in 2026 that made you feel proud?`;
        } else {
          heroResponse = `${interruptionPrefix}Let yourself really feel that. That took genuine diligence. Now, let's step across the threshold into 2027. What do you want to be deeply proud of in 2027?`;
          nextStage = 3;
        }
        break;

      // 3. THE 2027 PRIDE (Audacity gap & Day in the life)
      case 3:
        if (isBrief) {
          heroResponse = `${interruptionPrefix}Don't hold back on the audacity. If nothing held you back, what does that 2027 victory feel like?`;
        } else {
          heroResponse = `${interruptionPrefix}And the version of you who has already won that... what does their morning look like? What are they doing when the sun comes up?`;
          nextStage = 4;
        }
        break;

      // 4. THE CHARACTER AS A SCENE (Movie Scene & Naming)
      case 4:
        if (!context.characterNameIdea && !userMsgClean.includes("creator") && !userMsgClean.includes("builder")) {
          heroResponse = `${interruptionPrefix}Picture your 2027 like a movie. Which scene do you love most? What are you doing with your hands, and what do others see in your eyes? Let's name this character together.`;
        } else {
          const charName = context.characterNameIdea || "The Moonlit Creator";
          heroResponse = `${interruptionPrefix}That scene is so vivid. We see you as ${charName}. How does that name feel when you speak it out loud?`;
        }
        nextStage = 5;
        break;

      // 5. GROUNDING (Real past story of diligence)
      case 5:
        if (context.pastGroundingStory && !userMessage) {
          heroResponse = `${interruptionPrefix}When you look back at when you pulled off "${context.pastGroundingStory}", when have you already been this person, even for a moment?`;
        } else {
          heroResponse = `${interruptionPrefix}When have you already been this person in your own life? Give us one real story where you showed that same courage or diligence.`;
        }
        nextStage = 6;
        break;

      // 6. MIRROR (Summary of Idea, Character & Evidence + Intentional Pause)
      case 6:
        const qualitiesText = (context.coreQualities || ["quiet intuition", "resilience"]).slice(0, 3).join(", ");
        heroResponse = `${interruptionPrefix}So this is someone you already are. The character who lives your 2027 isn't an imaginary stranger. You already carry that ${qualitiesText} in your bones. Look at what you've walked through to get here.`;
        nextStage = 7;
        break;

      // 7. CLOSE (Exact Closing Statement)
      case 7:
      default:
        heroResponse = "Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise.";
        isCallEnding = true;
        break;
    }

    return NextResponse.json({
      success: true,
      heroResponse,
      currentStage: nextStage,
      isCallEnding,
    });

  } catch (error: any) {
    console.error("Hero Brain error:", error);
    return NextResponse.json(
      { success: false, error: error.message || "Brain processing error" },
      { status: 500 }
    );
  }
}
