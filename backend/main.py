from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import anthropic
import json
import os
from dotenv import load_dotenv

from seasons import get_season_list, get_system_prompt
from tba import TOOL_HANDLERS

load_dotenv()

app = FastAPI(title="FRC/FTC Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

TBA_TOOLS = [
    {
        "name": "get_team_info",
        "description": "Get basic info about an FRC team: name, location, rookie year, website.",
        "input_schema": {
            "type": "object",
            "properties": {"team_number": {"type": "integer", "description": "FRC team number, e.g. 254"}},
            "required": ["team_number"],
        },
    },
    {
        "name": "get_team_events",
        "description": "Get the list of FRC events a team attended in a given year.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_number": {"type": "integer", "description": "FRC team number"},
                "year": {"type": "integer", "description": "Season year, e.g. 2024"},
            },
            "required": ["team_number", "year"],
        },
    },
    {
        "name": "get_team_event_status",
        "description": "Get a team's ranking, record, and playoff status at a specific event. Event key format: year + event code, e.g. '2024arc' for 2024 Archimedes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_number": {"type": "integer", "description": "FRC team number"},
                "event_key": {"type": "string", "description": "TBA event key, e.g. '2024arc'"},
            },
            "required": ["team_number", "event_key"],
        },
    },
    {
        "name": "get_event_rankings",
        "description": "Get the top 20 rankings at an FRC event. Event key format: year + event code, e.g. '2024arc'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_key": {"type": "string", "description": "TBA event key, e.g. '2024arc'"}
            },
            "required": ["event_key"],
        },
    },
    {
        "name": "get_event_teams",
        "description": "Get all teams attending a specific FRC event.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_key": {"type": "string", "description": "TBA event key, e.g. '2024arc'"}
            },
            "required": ["event_key"],
        },
    },
    {
        "name": "get_team_awards",
        "description": "Get awards an FRC team won in a given year.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_number": {"type": "integer", "description": "FRC team number"},
                "year": {"type": "integer", "description": "Season year, e.g. 2024"},
            },
            "required": ["team_number", "year"],
        },
    },
    {
        "name": "get_team_season_summary",
        "description": (
            "Get a complete season summary for an FRC team: all events attended, "
            "their ranking and win/loss record at each event, playoff results, and awards. "
            "Use this whenever the user asks about a team's performance, season, results, or history "
            "for a specific year. Prefer this over calling get_team_events + get_team_event_status separately."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "team_number": {"type": "integer", "description": "FRC team number"},
                "year": {"type": "integer", "description": "Season year, e.g. 2026"},
            },
            "required": ["team_number", "year"],
        },
    },
]


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    season_id: Optional[str] = None


@app.get("/seasons")
def list_seasons():
    return get_season_list()


@app.post("/chat")
def chat(req: ChatRequest):
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")

    system_prompt = get_system_prompt(req.season_id)
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # Agentic loop: let Claude call TBA tools as needed
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            tools=TBA_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            text = next((b.text for b in response.content if hasattr(b, "text")), "")
            return {"response": text}

        if response.stop_reason == "tool_use":
            # Append Claude's response (with tool calls) to messages
            messages.append({"role": "assistant", "content": response.content})

            # Execute each tool call and collect results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    handler = TOOL_HANDLERS.get(block.name)
                    result = handler(block.input) if handler else {"error": f"Unknown tool: {block.name}"}
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            messages.append({"role": "user", "content": tool_results})
            continue

        # Unexpected stop reason
        break

    return {"response": "Sorry, I encountered an unexpected error."}


@app.get("/health")
def health():
    return {"status": "ok"}
