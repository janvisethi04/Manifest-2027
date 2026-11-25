"""
Hero Voice Agent: Manifest 2027 Main Runner
Usage:
    python main.py                # Full voice mode (Microphone + Speaker)
    python main.py --mode text    # Hybrid mode (Keyboard input + Speaker voice)
    python main.py --voice hindi  # Use Hindi/Hinglish neural voice
    python main.py --test         # Run automated 7-stage & barge-in test suite
"""
import sys
import argparse
from agent import HeroVoiceAgent
from config import DEFAULT_VOICE, HINDI_VOICE, FEMALE_VOICE

def parse_args():
    parser = argparse.ArgumentParser(description="Hero: Manifest 2027 Ceremonial Voice Agent")
    parser.add_argument(
        "--mode",
        choices=["voice", "text", "test"],
        default="voice",
        help="Interaction mode: 'voice' (mic + speaker), 'text' (type + speaker), or 'test'"
    )
    parser.add_argument(
        "--voice",
        choices=["default", "hindi", "female"],
        default="default",
        help="Neural voice selection: default (Christopher), hindi (Madhur), female (Ava)"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Janvi",
        help="User name for personalization"
    )
    return parser.parse_args()

def run_tests():
    """Run verification tests."""
    import test_agent
    test_agent.run_all_tests()

def main():
    args = parse_args()

    if args.mode == "test":
        run_tests()
        return

    # Select voice
    voice_map = {
        "default": DEFAULT_VOICE,
        "hindi": HINDI_VOICE,
        "female": FEMALE_VOICE
    }
    selected_voice = voice_map.get(args.voice, DEFAULT_VOICE)

    context = {
        "user_name": args.name,
        "preferred_language": "English / Hinglish",
        "coreQualities": ["Quiet Intuition", "Resilience", "Creative Sovereignty"],
        "characterNameIdea": "The Sovereign Creator"
    }

    agent = HeroVoiceAgent(context=context, voice=selected_voice)

    if args.mode == "voice":
        print("\n[INFO] Starting in Voice Mode. Please ensure your microphone and speakers are connected.")
        agent.stt.calibrate(duration=1.0)

    try:
        agent.start_conversation(mode=args.mode)
    except KeyboardInterrupt:
        print("\n[Exiting Hero Voice Agent. Goodbye.]")

if __name__ == "__main__":
    main()
