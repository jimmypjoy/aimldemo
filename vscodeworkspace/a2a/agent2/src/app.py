import uuid
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

HOST = os.getenv("AGENT2_HOST", "127.0.0.1")
PORT = int(os.getenv("AGENT2_PORT", "8002"))

AGENT_CARD = {
    "name": "Agent 2",
    "description": "A simple greeting agent that says hello from Agent 2.",
    "url": f"http://{HOST}:{PORT}",
    "version": "1.0.0",
    "capabilities": {"streaming": False},
    "skills": [
        {
            "id": "greet",
            "name": "Greet",
            "description": "Responds with a greeting from Agent 2.",
            "examples": ["Hello!", "Say hi"],
        }
    ],
}

app = FastAPI(title="Agent 2 - A2A Demo")


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

    print(f"[Agent 2] Received message: {incoming_text}")
    reply = "Hello JJ from agent2"
    print(f"[Agent 2] Returning: {reply}")

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
                        "parts": [{"kind": "text", "text": reply}],
                    }
                ],
            },
        }
    )
