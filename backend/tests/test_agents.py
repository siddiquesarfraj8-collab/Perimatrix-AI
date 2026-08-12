import os
import json
import pytest
from fastapi.testclient import TestClient
from backend.Main import app
from backend.LLM.provider import LLMProvider
from backend.MEMORY.manager import MemoryManager
from backend.Agents.base import BaseAgent
from backend.Agents.specialized import CoderAgent, ResearchAgent
from backend.Agents.orchestrator import AgentCollaborationTeam

client = TestClient(app)

def test_llm_provider_mock():
    provider = LLMProvider(provider_type="mock")
    # Base generation
    res = provider.generate("hello world")
    assert "Simulated response" in res or "PeriMatrix" in res

    # System-specific/Agent-specific mock trigger
    coder_res = provider.generate("generate coder class", system_message="You are a coder")
    assert "CoderAgent" in coder_res or "PeriMatrixCore" in coder_res

    # Planner mock trigger
    plan_res = provider.generate("breakdown task")
    assert "subtasks" in plan_res

def test_memory_manager(tmp_path):
    mem_dir = str(tmp_path)
    manager = MemoryManager(memory_dir=mem_dir)

    # Check initial
    assert manager.get_session_history("session-1") == []

    # Store short term
    manager.add_to_session("session-1", "user", "Hello agent")
    history = manager.get_session_history("session-1")
    assert len(history) == 1
    assert history[0]["sender"] == "user"
    assert history[0]["message"] == "Hello agent"

    # Store long term
    manager.store_long_term_memory("Important architecture rule: Use FastAPI for async backends", tags=["arch"])
    search_res = manager.search_long_term_memories("FastAPI")
    assert len(search_res) == 1
    assert "FastAPI" in search_res[0]

def test_agents_and_orchestration(tmp_path):
    mem_dir = str(tmp_path)
    provider = LLMProvider(provider_type="mock")
    manager = MemoryManager(memory_dir=mem_dir)
    orchestrator = AgentCollaborationTeam(provider=provider, memory_manager=manager)

    # Resolve a dummy problem
    result = orchestrator.solve_problem("test-session", "Create a task manager microservice")
    assert result["session_id"] == "test-session"
    assert len(result["subtasks"]) > 0
    assert len(result["execution_steps"]) > 0
    assert "final_solution" in result
    assert "Final Report" in result["final_solution"] or "PeriMatrix" in result["final_solution"]

def test_fastapi_endpoints():
    # Test GET agents list
    res = client.get("/agents/")
    assert res.status_code == 200
    data = res.json()
    assert "agents" in data
    assert any(a["name"] == "CoderAgent" for a in data["agents"])

    # Test POST collaborate
    collab_payload = {
        "session_id": "api-session-123",
        "problem": "Design a modern multi-agent portfolio optimizer"
    }
    collab_res = client.post("/agents/collaborate", json=collab_payload)
    assert collab_res.status_code == 200
    collab_data = collab_res.json()
    assert collab_data["session_id"] == "api-session-123"
    assert len(collab_data["subtasks"]) > 0
    assert "final_solution" in collab_data

def test_chat_endpoint():
    # Test POST /chat with message and custom session
    chat_payload = {
        "message": "Let's build a clean codebase for PeriMatrix",
        "session_id": "chat-session-456"
    }
    chat_res = client.post("/chat", json=chat_payload)
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert chat_data["session_id"] == "chat-session-456"
    assert chat_data["problem"] == "Let's build a clean codebase for PeriMatrix"
    assert len(chat_data["subtasks"]) > 0
    assert "final_solution" in chat_data

    # Test POST /chat with default session_id
    chat_payload_default = {
        "message": "Tell me a joke about agents"
    }
    chat_res_default = client.post("/chat", json=chat_payload_default)
    assert chat_res_default.status_code == 200
    chat_data_default = chat_res_default.json()
    assert chat_data_default["session_id"] == "default_session"
    assert chat_data_default["problem"] == "Tell me a joke about agents"
    assert len(chat_data_default["subtasks"]) > 0
    assert "final_solution" in chat_data_default
