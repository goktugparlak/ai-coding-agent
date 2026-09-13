from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.agent import CodingAgent
from app.config import PROJECT_ROOT

FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title="AI Coding Agent Prototype",
    version="1.0.0",
    description=(
        "A portfolio-ready coding-agent prototype using a mock provider."
    ),
)

agent = CodingAgent()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)


class ChatResponse(BaseModel):
    response: str


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "provider": "mock",
        "llm_connected": False,
    }


@app.get("/api/history")
def history() -> list[dict]:
    return agent.history.recent(limit=20)


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(response=agent.run(request.message))


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
