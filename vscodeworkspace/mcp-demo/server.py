import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv

load_dotenv()

import uvicorn
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

from app import mcp
from telemetry import SessionTraceLoggingMiddleware

if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", "3001"))
    print(f"Starting MCP server on http://{host}:{port}")

    # mcp.run() builds and runs its own ASGI app internally with no hook to wrap
    # it with OTEL middleware, so the app is built manually here instead and
    # served directly via uvicorn. SessionTraceLoggingMiddleware sits inside
    # OpenTelemetryMiddleware so it logs after trace/baggage context has been
    # extracted from the incoming request.
    asgi_app = OpenTelemetryMiddleware(SessionTraceLoggingMiddleware(mcp.streamable_http_app()))
    uvicorn.run(asgi_app, host=host, port=port)
