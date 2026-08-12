from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.Agents.orchestrator import AgentCollaborationTeam

router = APIRouter(prefix="/chat", tags=["Chat"])
orchestrator = AgentCollaborationTeam()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"

class ChatResponse(BaseModel):
    session_id: str
    problem: str
    subtasks: List[Dict[str, Any]]
    execution_steps: List[Dict[str, Any]]
    final_solution: str

@router.post("", response_model=ChatResponse)
def run_chat(payload: ChatRequest):
    """
    Sends a user message through the existing agent orchestration system.
    """
    try:
        result = orchestrator.solve_problem(
            session_id=payload.session_id,
            problem_statement=payload.message
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat orchestration failed: {str(e)}")
