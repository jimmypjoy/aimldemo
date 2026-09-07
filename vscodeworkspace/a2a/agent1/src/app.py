import uuid
import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

HOST = os.getenv("AGENT1_HOST", "127.0.0.1")
PORT = int(os.getenv("AGENT1_PORT", "8001"))
AGENT2_URL = f"http://{os.getenv('AGENT2_HOST', '127.0.0.1')}:{os.getenv('AGENT2_PORT', '8002')}"

AGENT_CARD = {
    "name": "Agent 1",
    "description": "A simple greeting agent that says hello from Agent 1.",
    "url": f"http://{HOST}:{PORT}",
    "version": "1.0.0",
    "capabilities": {"streaming": False},
    "skills": [
        {
            "id": "greet",
            "name": "Greet",
            "description": "Responds with a greeting from Agent 1.",
            "examples": ["Hello!", "Say hi"],
        }
    ],
}

app = FastAPI(title="Agent 1 - A2A Demo")


def call_agent2(text: str) -> str:
    """A2A call — Agent 1 contacts Agent 2 using the A2A protocol."""
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
    response = httpx.post(AGENT2_URL, json=payload)
    response.raise_for_status()
    artifacts = response.json().get("result", {}).get("artifacts", [])
    if artifacts:
        parts = artifacts[0].get("parts", [])
        return next((p.get("text", "") for p in parts if p.get("kind") == "text"), "")
    return ""


@app.get("/.well-known/agent.json")
def get_agent_card():
    """A2A Agent Card — describes this agent's identity and capabilities."""
    return JSONResponse(content=AGENT_CARD)


@app.post("/")
async def handle_task(request: Request):
    """A2A task endpoint — receives JSON-RPC 2.0 message/send calls."""
    body = await request.json()
    rpc_id = body.get("id", str(uuid.uuid4()))

    parts = body.get("params", {}).get("message", {}).get("parts", [])
    incoming_text = next((p.get("text", "") for p in parts if p.get("kind") == "text"), "")

    print(f"[Agent 1] Received message: {incoming_text}")

    own_message = "Hello JJ from agent1"
    print(f"[Agent 1] My own message: {own_message}")

    print(f"[Agent 1] Calling Agent 2 via A2A...")
    agent2_reply = call_agent2(incoming_text)
    print(f"[Agent 1] Got response from Agent 2: {agent2_reply}")

    combined = f"{own_message} | {agent2_reply}"
    print(f"[Agent 1] Returning to client: {combined}")

    return JSONResponse(
        content={
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "id": rpc_id,
                "status": {"state": "completed"},
                "artifacts": [
                    {
                        "name": "greeting",
                        "parts": [{"kind": "text", "text": combined}],
                    }
                ],
            },
        }
    )
