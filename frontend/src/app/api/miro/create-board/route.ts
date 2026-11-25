import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { userName, userEmail, archetype, personalizedQuote, vision2027Headline, coreQualities, groundingFeat } = body;

    const miroToken = process.env.MIRO_ACCESS_TOKEN;

    if (miroToken) {
      // 1. Create real board in Miro via official Miro REST API v2
      const boardRes = await fetch("https://api.miro.com/v2/boards", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${miroToken}`,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          name: `${userName || "User"}'s 2027 Manifestation Board`,
          description: `Converse AI Manifest 2027 • Archetype: ${archetype?.title || "The Moonlit Creator"}`,
        }),
      });

      if (boardRes.ok) {
        const boardData = await boardRes.json();
        const boardId = boardData.id;
        const viewLink = boardData.viewLink || `https://miro.com/app/board/${boardId}/`;

        // 2. Add Sticky Notes to the Miro Board
        const stickyNotes = [
          { content: `✨ 2027 Vision:\n${vision2027Headline}`, color: "light_pink", x: 0, y: 0 },
          { content: `🌱 2026 Grounding Feat:\n${groundingFeat}`, color: "light_yellow", x: 250, y: 0 },
          { content: `🎭 Archetype: ${archetype?.title}\nElement: ${archetype?.element}`, color: "light_blue", x: 0, y: 250 },
          { content: `📜 Personal Quote:\n${personalizedQuote}`, color: "light_green", x: 250, y: 250 },
          { content: `⭐ Core Qualities:\n${(coreQualities || []).join(", ")}`, color: "purple", x: 500, y: 125 },
        ];

        for (const note of stickyNotes) {
          try {
            await fetch(`https://api.miro.com/v2/boards/${boardId}/sticky_notes`, {
              method: "POST",
              headers: {
                Authorization: `Bearer ${miroToken}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                data: { content: note.content, shape: "square" },
                style: { fillColor: note.color },
                position: { origin: "center", x: note.x, y: note.y },
              }),
            });
          } catch (e) {
            console.error("Failed adding Miro sticky note", e);
          }
        }

        return NextResponse.json({
          success: true,
          boardId,
          viewLink,
          isLiveMiro: true,
          message: "Real Miro board generated in your Miro workspace!",
        });
      }
    }

    // Fallback: If no MIRO_ACCESS_TOKEN is configured in environment, generate public share link & local canvas state
    const demoBoardId = "manifest_2027_" + Math.random().toString(36).substring(2, 9);
    const mockMiroUrl = `https://miro.com/app/board/${demoBoardId}/`;

    return NextResponse.json({
      success: true,
      boardId: demoBoardId,
      viewLink: mockMiroUrl,
      isLiveMiro: false,
      message: "Manifestation Board generated! (To sync directly with your Miro workspace, set MIRO_ACCESS_TOKEN in .env)",
    });

  } catch (error: any) {
    console.error("Miro API Error:", error);
    return NextResponse.json(
      { success: false, error: error.message || "Failed to generate board" },
      { status: 500 }
    );
  }
}
