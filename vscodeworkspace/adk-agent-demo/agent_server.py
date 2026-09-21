import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("ADK_PORT", "8080"))
    agents_dir = os.path.join(os.path.dirname(__file__), "src", "agents")
    print(f"Starting ADK Web UI on http://127.0.0.1:{port}")

    subprocess.run(["opentelemetry-instrument", "adk", "web", agents_dir, "--port", str(port)])
