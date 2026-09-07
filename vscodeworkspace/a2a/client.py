"""
A2A Protocol Demo Client
------------------------
Client only talks to Agent 1.
Agent 1 internally calls Agent 2 (true agent-to-agent communication),
then returns both responses combined.

Run agents first:
  Terminal 1: python agent1/server.py
  Terminal 2: python agent2/server.py
  Terminal 3: python client.py
"""

import os
import uuid

import httpx
from dotenv import load_dotenv

load_dotenv()

AGENT1_URL = f"http://{os.getenv('AGENT1_HOST', '127.0.0.1')}:{os.getenv('AGENT1_PORT', '8001')}"


def discover_agent(base_url: str) -> dict:
    """Fetch the Agent Card from /.well-known/agent.json."""
    response = httpx.get(f"{base_url}/.well-known/agent.json")
    response.raise_for_status()
    return response.json()


def send_message(base_url: str, text: str) -> str:
    """Send a message/send JSON-RPC 2.0 task and return the artifact text."""
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": str(uuid.uuid4()),
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": text}],
            }
        },
    }
    response = httpx.post(base_url, json=payload)
    response.raise_for_status()
    artifacts = response.json().get("result", {}).get("artifacts", [])
    if artifacts:
        parts = artifacts[0].get("parts", [])
        return next((p.get("text", "") for p in parts if p.get("kind") == "text"), "")
    return ""


def main():
    print("=" * 55)
    print("          A2A Protocol Demo")
    print("=" * 55)

    # --- Agent Discovery ---
    print("\n[1] Discovering Agent 1 via Agent Card...")
    card1 = discover_agent(AGENT1_URL)
    print(f"    Found: {card1['name']} — {card1['description']}")

    # --- Client talks only to Agent 1 ---
    # Agent 1 internally calls Agent 2 (A2A), then returns combined reply
    print("\n[2] Client → Agent 1: 'Hello!'")
    reply = send_message(AGENT1_URL, "Hello!")
    print(f"\n[3] Agent 1 → Client: '{reply}'")

    print("\n" + "=" * 55)
    print("Flow: Client → Agent 1 → Agent 2 (A2A) → Agent 1 → Client")
    print("=" * 55)


if __name__ == "__main__":
    main()
