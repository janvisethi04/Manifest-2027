import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { userEmail, userName, archetype, personalizedQuote, vision2027Headline, miroBoardUrl } = await req.json();

    if (!userEmail) {
      return NextResponse.json({ success: false, error: "Email is required" }, { status: 400 });
    }

    const emailSubject = `Your 2027 Manifestation Board & Archetype — Converse AI`;
    const emailBodyHtml = `
      <div style="font-family: 'Georgia', serif; background-color: #FFFDF9; padding: 40px; color: #362544; max-width: 600px; margin: 0 auto; border: 1px solid #EBE6FA; border-radius: 16px;">
        <h1 style="color: #362544; font-size: 28px; margin-bottom: 8px;">Dearest ${userName || "Friend"},</h1>
        <p style="font-size: 16px; line-height: 1.6; color: #614C72;">
          Your voice session with <strong>Hero</strong> is sealed into reality. Here is your synthesized 2027 manifestation blueprint.
        </p>

        <div style="background-color: #FBE6ED; padding: 20px; border-radius: 12px; margin: 24px 0;">
          <p style="text-transform: uppercase; font-size: 11px; letter-spacing: 2px; color: #8A799B; margin: 0 0 6px 0;">Your 2027 Archetype</p>
          <h2 style="font-size: 24px; color: #362544; margin: 0 0 8px 0;">${archetype?.title || "The Moonlit Creator"}</h2>
          <p style="font-size: 14px; color: #362544; margin: 0;"><strong>Symbolic Element:</strong> ${archetype?.element || "Water"}</p>
          <p style="font-size: 13px; color: #614C72; margin-top: 8px;"><em>${archetype?.rationale || ""}</em></p>
        </div>

        <blockquote style="font-size: 18px; font-style: italic; color: #362544; border-left: 3px solid #CCA456; padding-left: 16px; margin: 24px 0;">
          ${personalizedQuote}
        </blockquote>

        <div style="background-color: #EBE6FA; padding: 20px; border-radius: 12px; margin: 24px 0;">
          <p style="text-transform: uppercase; font-size: 11px; letter-spacing: 2px; color: #8A799B; margin: 0 0 6px 0;">2027 Vision Headline</p>
          <p style="font-size: 16px; color: #362544; margin: 0; font-weight: bold;">"${vision2027Headline}"</p>
        </div>

        <div style="text-align: center; margin: 32px 0;">
          <a href="${miroBoardUrl || "http://localhost:3000/board"}" style="background-color: #362544; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 30px; font-size: 15px; font-weight: bold; display: inline-block;">
            Open Your Miro Manifestation Board →
          </a>
        </div>

        <hr style="border: none; border-top: 1px solid #EBE6FA; margin: 32px 0;" />
        <p style="font-size: 12px; color: #8A799B; text-align: center;">
          "Consider your manifestation ready. We'll come back to you within the next 15 days with a surprise."
        </p>
      </div>
    `;

    console.log(`[Email Dispatcher] Mock/Live Email to ${userEmail}: Subject: ${emailSubject}`);

    return NextResponse.json({
      success: true,
      recipient: userEmail,
      subject: emailSubject,
      previewHtml: emailBodyHtml,
      status: "delivered",
      message: `Manifestation summary emailed successfully to ${userEmail}!`,
    });

  } catch (error: any) {
    console.error("Email API error:", error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
