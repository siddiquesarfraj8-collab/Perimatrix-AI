from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.Agents.orchestrator import AgentCollaborationTeam

router = APIRouter(prefix="/chat", tags=["Chat"])
orchestrator = AgentCollaborationTeam()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    final_answer: str
    subtasks: List[Dict[str, Any]]
    execution_steps: List[Dict[str, Any]]
    session_id: str

@router.post("/", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    """
    Unified single-point chat endpoint that uses the AI Agent Collaboration Team
    under the hood to solve user goals, returning the final synthesized answer and process logs.
    """
    try:
        result = orchestrator.solve_problem(
            session_id=payload.session_id,
            problem_statement=payload.message
        )
        return {
            "final_answer": result.get("final_solution", ""),
            "subtasks": result.get("subtasks", []),
            "execution_steps": result.get("execution_steps", []),
            "session_id": payload.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat session failed: {str(e)}")
