import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from app import app

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("AGENT2_HOST", "127.0.0.1")
    port = int(os.getenv("AGENT2_PORT", "8002"))
    print(f"Starting Agent 2 on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
