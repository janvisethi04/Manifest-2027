#!/usr/bin/env python3
"""
Converse AI – Manifest 2027
ElevenLabs Hero Agent Provisioning Script
Creates or updates the Hero Agent in ElevenLabs using the official Conversational AI API.
Uses standard Python library (zero third-party dependencies required).
"""

import os
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://api.elevenlabs.io/v1/convai"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "elevenlabs_agent_config.json")
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "hero_agent_credentials.json")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[!] Error: Configuration file not found at {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def create_hero_agent(api_key: str):
    config = load_config()
    url = f"{API_BASE}/agents/create"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = json.dumps(config).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    print("[*] Connecting to ElevenLabs Conversational AI API...")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            agent_id = data.get("agent_id")
            print(f"[✓] Hero Agent successfully created in your ElevenLabs account!")
            print(f"[✓] Agent ID: {agent_id}")

            # Save credentials locally
            creds = {
                "agent_id": agent_id,
                "api_key": api_key,
                "created_at": str(resp.headers.get("Date"))
            }
            with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                json.dump(creds, f, indent=2)
            print(f"[✓] Saved credentials to {CREDENTIALS_FILE}")
            return agent_id

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"[!] HTTP Error {e.code}: {e.reason}")
        print(f"[!] Details: {error_body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[!] Connection Error: {e.reason}")
        sys.exit(1)

def get_agent_details(agent_id: str, api_key: str):
    url = f"{API_BASE}/agents/{agent_id}"
    req = urllib.request.Request(url, headers={"xi-api-key": api_key}, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[!] Failed to fetch agent: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("  HERO AGENT BUILDER — ELEVENLABS CONVERSATIONAL AI")
    print("=" * 60)

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        if len(sys.argv) > 1:
            api_key = sys.argv[1].strip()
        else:
            api_key = input("Enter your ElevenLabs API Key (xi-api-key): ").strip()

    if not api_key:
        print("[!] Error: ElevenLabs API Key is required.")
        sys.exit(1)

    create_hero_agent(api_key)
