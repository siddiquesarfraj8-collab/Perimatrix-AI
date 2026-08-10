from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.Agents.orchestrator import AgentCollaborationTeam

router = APIRouter(prefix="/agents", tags=["Agents"])
orchestrator = AgentCollaborationTeam()

class CollaborateRequest(BaseModel):
    session_id: str
    problem: str

class CollaborateResponse(BaseModel):
    session_id: str
    problem: str
    subtasks: List[Dict[str, Any]]
    execution_steps: List[Dict[str, Any]]
    final_solution: str

@router.get("/")
def get_agents():
    """
    Returns available intelligent agents in the collaboration squad.
    """
    return {
        "agents": [
            {
                "name": name,
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory
            }
            for name, agent in orchestrator.agents.items()
        ]
    }

@router.post("/collaborate", response_model=CollaborateResponse)
def run_collaboration(payload: CollaborateRequest):
    """
    Runs a full AI agent collaboration session to address and solve a specified project or user problem.
    """
    try:
        result = orchestrator.solve_problem(
            session_id=payload.session_id,
            problem_statement=payload.problem
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Collaboration failed: {str(e)}")
