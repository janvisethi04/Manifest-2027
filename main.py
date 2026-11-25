"""
Hero Voice Agent: Manifest 2027 Main Entry Point
Usage:
    python main.py              # Launch the ElevenLabs-style Living Voice Agent UI (Default)
    python main.py --cli        # Run in terminal voice mode (Mic + Speaker)
    python main.py --cli --text # Run in terminal text mode (Keyboard + Speaker)
    python main.py --test       # Run automated test suite
"""
import sys
import argparse
import webbrowser

def parse_args():
    parser = argparse.ArgumentParser(description="Hero: Manifest 2027 Ceremonial Voice Agent")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in terminal CLI mode instead of launching the Agent UI"
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Use keyboard input instead of microphone in CLI mode"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the Voice Agent Studio UI (default: 8000)"
    )
    parser.add_argument(
        "--voice",
        choices=["default", "hindi", "female"],
        default="default",
        help="Neural voice selection: default (Christopher), hindi (Madhur), female (Ava)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run automated test suite"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    if args.test:
        import test_agent
        test_agent.run_all_tests()
        return

    if args.cli:
        from agent import HeroVoiceAgent
        from config import DEFAULT_VOICE, HINDI_VOICE, FEMALE_VOICE
        
        voice_map = {
            "default": DEFAULT_VOICE,
            "hindi": HINDI_VOICE,
            "female": FEMALE_VOICE
        }
        selected_voice = voice_map.get(args.voice, DEFAULT_VOICE)
        context = {
            "user_name": "Janvi",
            "preferred_language": "English / Hinglish",
            "coreQualities": ["Quiet Intuition", "Resilience", "Creative Sovereignty"],
            "characterNameIdea": "The Sovereign Creator"
        }
        agent = HeroVoiceAgent(context=context, voice=selected_voice)
        mode = "text" if args.text else "voice"
        if mode == "voice":
            agent.stt.calibrate(duration=1.0)
        try:
            agent.start_conversation(mode=mode)
        except KeyboardInterrupt:
            print("\n[Exiting CLI mode]")
    else:
        # Launch Agent Studio Web App
        from app import run_app
        run_app(port=args.port, open_browser=True)

if __name__ == "__main__":
    main()
