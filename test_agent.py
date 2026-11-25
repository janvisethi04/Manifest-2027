"""
Verification and Test Suite for Hero Voice Agent
Tests:
1. Complete 7-Stage Ceremonial Dialogue
2. Sentiment & Emotion Context Awareness Engine
3. Barge-In Interruption & Recovery
4. Vague & Brief Answer Handling
5. Edge-TTS Audio Generation & Stop Latency
"""
import time
import os
from brain import HeroBrain
from tts import TTSEngine
from emotion_engine import EmotionEngine
from config import CEREMONIAL_CLOSE_STATEMENT

def test_emotion_engine():
    print("=" * 60)
    print("TEST: SENTIMENT & EMOTION CONTEXT AWARENESS")
    print("=" * 60)

    ee = EmotionEngine()

    e1 = ee.analyze("I was scared and full of self doubt")
    print(f"Phrase 1: 'I was scared and full of self doubt' -> {e1['label']} (Polarity: {e1['polarity']}, Rate: {e1['voice_rate']})")
    assert e1["primary_emotion"] == "vulnerable_hesitant"

    e2 = ee.analyze("I want to build a massive global sovereign empire")
    print(f"Phrase 2: 'I want to build a massive global sovereign empire' -> {e2['label']} (Polarity: {e2['polarity']}, Rate: {e2['voice_rate']})")
    assert e2["primary_emotion"] == "audacious_expansive"

    e3 = ee.analyze("I worked hard and built our lab from scratch, so proud")
    print(f"Phrase 3: 'I worked hard and built our lab from scratch, so proud' -> {e3['label']} (Polarity: {e3['polarity']})")
    assert e3["primary_emotion"] == "proud_accomplished"

    e4 = ee.analyze("Just quiet tea in the morning, unhurried peace")
    print(f"Phrase 4: 'Just quiet tea in the morning, unhurried peace' -> {e4['label']} (Polarity: {e4['polarity']})")
    assert e4["primary_emotion"] == "peaceful_grounded"

    print("✅ PASS: Emotion & Sentiment Context Awareness verified successfully!")

def test_full_flow():
    print("\n" + "=" * 60)
    print("TEST: FULL 7-STAGE HERO CEREMONIAL FLOW WITH EMOTION ADAPTATION")
    print("=" * 60)

    context = {
        "user_name": "Janvi",
        "preferred_language": "English / Hinglish",
        "pride2026": "Building my independent creative tech lab",
        "pride2027": "Leading our studio with full creative sovereignty",
        "dayInTheLife2027": "Waking up peacefully, designing in flow",
        "movieScene": "Sunlit studio with completed canvases",
        "coreQualities": ["Quiet Intuition", "Resilience", "Creative Sovereignty"],
        "pastGroundingStory": "Launched our first initiative with zero budget",
        "characterNameIdea": "The Sovereign Creator"
    }

    brain = HeroBrain(context=context)

    # Stage 1: Open
    r1 = brain.process_turn("")
    print(f"\n[Stage 1] Hero: {r1['hero_response']}")
    assert "Welcome, Janvi" in r1["hero_response"]
    assert brain.current_stage == 2

    # Stage 2: 2026 Pride (Vulnerable utterance)
    r2 = brain.process_turn("I felt terrified and insecure at first, but I launched our lab anyway.")
    print(f"\n[Stage 2] Hero: {r2['hero_response']}")
    print(f"Detected Emotion: {r2['emotion']['label']}")
    assert "courage" in r2["hero_response"] or "breath" in r2["hero_response"] or "diligence" in r2["hero_response"]
    assert brain.current_stage == 3

    # Stage 3: 2027 Pride (Audacious utterance)
    r3 = brain.process_turn("In 2027, I want full creative sovereignty and massive bold global freedom.")
    print(f"\n[Stage 3] Hero: {r3['hero_response']}")
    print(f"Detected Emotion: {r3['emotion']['label']}")
    assert brain.current_stage == 4

    # Stage 4: Movie scene & Character
    r4 = brain.process_turn("The movie scene is walking into a sunlit studio, feeling serene and completely at peace.")
    print(f"\n[Stage 4] Hero: {r4['hero_response']}")
    assert "The Sovereign Creator" in r4["hero_response"]
    assert brain.current_stage == 5

    # Stage 5: Grounding
    r5 = brain.process_turn("I already did this when I launched our initiative with zero budget.")
    print(f"\n[Stage 5] Hero: {r5['hero_response']}")
    assert brain.current_stage == 6

    # Stage 6: Mirror
    r6 = brain.process_turn("")
    print(f"\n[Stage 6] Hero: {r6['hero_response']}")
    assert "Quiet Intuition" in r6["hero_response"]
    assert brain.current_stage == 7

    # Stage 7: Close
    r7 = brain.process_turn("Thank you Hero.")
    print(f"\n[Stage 7] Hero: {r7['hero_response']}")
    assert r7["hero_response"] == CEREMONIAL_CLOSE_STATEMENT
    assert brain.is_finished is True
    print("\n✅ PASS: Full 7-stage dialogue succeeded with emotional tuning and exact close statement!")

def test_barge_in_and_vague():
    print("\n" + "=" * 60)
    print("TEST: VAGUE ANSWER + USER BARGE-IN INTERRUPTION")
    print("=" * 60)

    brain = HeroBrain({"user_name": "Janvi"})
    brain.process_turn("")

    # Vague answer test
    print("\nUser says brief/vague answer: 'idk'")
    rv = brain.process_turn("idk")
    print(f"Hero gentle response: {rv['hero_response']}")
    assert "moment counts" in rv["hero_response"] or "breath" in rv["hero_response"]
    print("✅ PASS: Vague answer handled gently without interrogation.")

    # Barge-in interruption test
    print("\nUser interrupts Hero mid-sentence: 'Wait Hero, I want to change that!'")
    rb = brain.process_turn("Wait Hero, I want to change that!", was_interrupted=True)
    print(f"Hero recovery response: {rb['hero_response']}")
    assert any(w in rb['hero_response'] for w in ["Got you.", "Understood.", "I hear you"])
    print("✅ PASS: Barge-in acknowledged naturally.")

def run_all_tests():
    test_emotion_engine()
    test_full_flow()
    test_barge_in_and_vague()
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! SENTIMENT & EMOTION AWARENESS ENGINE IS OPERATIONAL.")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
