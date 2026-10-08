import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.main import run_checkpoint, score_answers

load_dotenv()

app = FastAPI(title="Learning Agent API")
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "LEARNING_AGENT_CORS_ORIGINS", "http://localhost:5173"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

sessions = {}


class StartRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=300)
    context: str = Field(default="", max_length=20000)


class AnswersRequest(BaseModel):
    answers: list[str]


def session_response(session_id, state, phase):
    return {
        "sessionId": session_id,
        "phase": phase,
        "topic": state.checkpoints[0]["topic"],
        "relevanceScore": state.relevance_score,
        "explanation": state.explanation,
        "questions": [
            {"question": question["question"], "options": question["options"]}
            for question in state.questions
        ],
        "score": state.verification_score,
        "answerFeedback": (
            state.answer_feedback if state.verification_score is not None else None
        ),
        "feynmanExplanation": getattr(state, "feynman_explanation", None),
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/sessions")
def start_session(request: StartRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=422, detail="Enter a topic to get started.")

    state = run_checkpoint(topic, request.context)
    session_id = str(uuid4())
    sessions[session_id] = state
    return session_response(session_id, state, "quiz")


@app.post("/api/sessions/{session_id}/answers")
def submit_answers(session_id: str, request: AnswersRequest):
    state = sessions.get(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Learning session not found.")
    if len(request.answers) != len(state.questions):
        raise HTTPException(
            status_code=422,
            detail=f"Submit one answer for each of the {len(state.questions)} questions.",
        )

    state = score_answers(state, request.answers)
    sessions[session_id] = state
    phase = "retry" if state.feynman_required else "complete"
    return session_response(session_id, state, phase)


@app.post("/api/sessions/{session_id}/retry")
def retry_session(session_id: str, request: AnswersRequest):
    state = sessions.get(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Learning session not found.")
    if not state.feynman_required:
        raise HTTPException(status_code=409, detail="There is no retry quiz pending.")
    if len(request.answers) != len(state.questions):
        raise HTTPException(
            status_code=422,
            detail=f"Submit one answer for each of the {len(state.questions)} questions.",
        )

    state = score_answers(state, request.answers)
    sessions[session_id] = state
    phase = "retry" if state.feynman_required else "complete"
    return session_response(session_id, state, phase)
