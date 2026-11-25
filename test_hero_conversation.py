import urllib.request
import json

BASE_URL = "http://localhost:3000/api/voice/hero-brain"

def call_hero(user_message, current_stage, history, context, was_interrupted=False):
    payload = {
        "userMessage": user_message,
        "currentStage": current_stage,
        "history": history,
        "context": context,
        "wasInterrupted": was_interrupted
    }
    
    req = urllib.request.Request(
        BASE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def test_full_conversation():
    print("=" * 60)
    print("TEST 1: COMPLETE 7-STAGE HERO CEREMONIAL FLOW")
    print("=" * 60)

    context = {
        "user_name": "Janvi",
        "preferred_language": "English / Hinglish",
        "pride2026": "Building my independent creative tech lab",
        "pride2027": "Leading my own studio and living with creative sovereignty",
        "dayInTheLife2027": "Waking up without anxiety, sipping tea, designing with flow",
        "movieScene": "Walking through a sunlit studio, smiling at our team, seeing our work in the world",
        "coreQualities": ["Quiet Intuition", "Resilience", "Creative Sovereignty"],
        "pastGroundingStory": "Launched a community project alone with zero budget and saw 100 people benefit",
        "characterNameIdea": "The Moonlit Creator"
    }

    history = []
    stage = 1
    
    # 1. OPEN
    r1 = call_hero("", stage, history, context)
    print(f"\n[Stage 1 -> Next: {r1['currentStage']}]")
    print(f"Hero: {r1['heroResponse']}")
    history.append({"speaker": "hero", "text": r1['heroResponse']})
    stage = r1['currentStage']

    # 2. PRIDE 2026
    user_2026 = "In 2026, I took the leap and built our creative tech lab from scratch."
    print(f"\nUser: {user_2026}")
    history.append({"speaker": "user", "text": user_2026})
    r2 = call_hero(user_2026, stage, history, context)
    print(f"[Stage 2 -> Next: {r2['currentStage']}]")
    print(f"Hero: {r2['heroResponse']}")
    history.append({"speaker": "hero", "text": r2['heroResponse']})
    stage = r2['currentStage']

    # 3. 2027 PRIDE
    user_2027 = "In 2027, I want to lead our studio with full creative sovereignty and coastal peace."
    print(f"\nUser: {user_2027}")
    history.append({"speaker": "user", "text": user_2027})
    r3 = call_hero(user_2027, stage, history, context)
    print(f"[Stage 3 -> Next: {r3['currentStage']}]")
    print(f"Hero: {r3['heroResponse']}")
    history.append({"speaker": "hero", "text": r3['heroResponse']})
    stage = r3['currentStage']

    # 4. MOVIE SCENE & CHARACTER
    user_scene = "The movie scene is walking into a sunlit studio, surrounded by finished canvases, feeling completely unhurried."
    print(f"\nUser: {user_scene}")
    history.append({"speaker": "user", "text": user_scene})
    r4 = call_hero(user_scene, stage, history, context)
    print(f"[Stage 4 -> Next: {r4['currentStage']}]")
    print(f"Hero: {r4['heroResponse']}")
    history.append({"speaker": "hero", "text": r4['heroResponse']})
    stage = r4['currentStage']

    # 5. GROUNDING
    user_ground = "I already did this when I launched our initiative with zero budget and made it happen."
    print(f"\nUser: {user_ground}")
    history.append({"speaker": "user", "text": user_ground})
    r5 = call_hero(user_ground, stage, history, context)
    print(f"[Stage 5 -> Next: {r5['currentStage']}]")
    print(f"Hero: {r5['heroResponse']}")
    history.append({"speaker": "hero", "text": r5['heroResponse']})
    stage = r5['currentStage']

    # 6. MIRROR
    print(f"\nUser: (Listening silently)")
    r6 = call_hero("", stage, history, context)
    print(f"[Stage 6 -> Next: {r6['currentStage']}]")
    print(f"Hero: {r6['heroResponse']}")
    history.append({"speaker": "hero", "text": r6['heroResponse']})
    stage = r6['currentStage']

    # 7. CLOSE
    print(f"\nUser: (Acknowledging)")
    r7 = call_hero("Thank you Hero.", stage, history, context)
    print(f"[Stage 7 -> Next: {r7['currentStage']}]")
    print(f"Hero: {r7['heroResponse']}")
    print(f"Is Call Ending: {r7['isCallEnding']}")

def test_barge_in_and_vague():
    print("\n" + "=" * 60)
    print("TEST 2: VAGUE ANSWER + USER BARGE-IN INTERRUPTION")
    print("=" * 60)

    context = {"user_name": "Janvi"}
    history = []

    # Vague answer test
    print("\nUser says vague answer: 'idk'")
    rv = call_hero("idk", 2, history, context)
    print(f"Hero gentle elicitation: {rv['heroResponse']}")

    # Barge-in interruption test
    print("\nUser barges in: 'Wait Hero, I actually want to change my 2027 goal!' (wasInterrupted=True)")
    rb = call_hero("Wait Hero, I actually want to change my 2027 goal!", 3, history, context, was_interrupted=True)
    print(f"Hero interrupted response: {rb['heroResponse']}")

if __name__ == "__main__":
    test_full_conversation()
    test_barge_in_and_vague()
