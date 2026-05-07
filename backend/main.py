from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import anthropic
import os
from dotenv import load_dotenv

from seasons import get_season_list, get_system_prompt

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


class Message(BaseModel):
    role: str  # "user" or "assistant"
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

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": m.role, "content": m.content} for m in req.messages],
    )

    return {"response": response.content[0].text}


@app.get("/health")
def health():
    return {"status": "ok"}
