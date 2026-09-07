import sys
from datetime import date
from pathlib import Path

_src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_src_dir))

from dotenv import load_dotenv

load_dotenv(_src_dir.parent / ".env")

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from config.settings import get_settings

settings = get_settings()

_SKILL_PATH = _src_dir / "skills" / "company_annual_review" / "SKILL.md"
_SKILL_CONTENT = _SKILL_PATH.read_text(encoding="utf-8")


def build_instruction(context: ReadonlyContext) -> str:
    today = date.today().isoformat()
    return f"Today's date is {today}.\n\n{_SKILL_CONTENT}"


root_agent = Agent(
    name="company_annual_review_agent",
    model=settings.agent_model,
    description=(
        "Specialized agent that produces a Company Annual Review summary "
        "(revenue, market capitalization, internal rating, analyst name) "
        "using only the tools exposed by the mcp-demo MCP server."
    ),
    instruction=build_instruction,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=f"{settings.mcp_server_url}/mcp"
            )
        ),
    ],
)
