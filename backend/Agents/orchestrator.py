import json
from typing import List, Dict, Any, Optional
from backend.LLM.provider import LLMProvider
from backend.MEMORY.manager import MemoryManager
from backend.Agents.specialized import (
    CoderAgent, ResearchAgent, MemoryAgent,
    BrowserAgent, VisionAgent, PlannerAgent
)

class AgentCollaborationTeam:
    """
    Orchestrator to coordinate, assign, monitor, and synthesize tasks
    among specialized agent squads.
    """
    def __init__(self, provider: Optional[LLMProvider] = None, memory_manager: Optional[MemoryManager] = None):
        self.provider = provider or LLMProvider()
        self.memory_manager = memory_manager or MemoryManager()

        # Instantiate available agents
        self.agents = {
            "CoderAgent": CoderAgent(provider=self.provider),
            "ResearchAgent": ResearchAgent(provider=self.provider),
            "MemoryAgent": MemoryAgent(provider=self.provider),
            "BrowserAgent": BrowserAgent(provider=self.provider),
            "VisionAgent": VisionAgent(provider=self.provider),
            "PlannerAgent": PlannerAgent(provider=self.provider),
        }

    def solve_problem(self, session_id: str, problem_statement: str) -> Dict[str, Any]:
        """
        Orchestration pipeline:
        1. Query PlannerAgent to break down the request.
        2. Execute structured subtasks through assigned specialized agents sequentially.
        3. Store subtask execution contexts and interactions.
        4. Synthesize all agent responses into a final comprehensive report.
        """
        # Save user request in history
        self.memory_manager.add_to_session(session_id, "User", problem_statement, role="user")

        # 1. Plan breakdown
        planner_prompt = (
            f"Break down the user's project/request into a structured JSON list of subtasks. "
            f"Each subtask must contain: 'agent' (which should be one of {list(self.agents.keys())}) and "
            f"'task' (the direct action description for that agent).\n\n"
            f"User request: \"{problem_statement}\""
        )

        plan_response = self.agents["PlannerAgent"].execute_task(planner_prompt)

        # Parse planning response
        subtasks = []
        try:
            # Look for JSON structure in the planning response
            start_idx = plan_response.find("[")
            end_idx = plan_response.rfind("]") + 1
            if start_idx != -1 and end_idx != -1:
                json_data = plan_response[start_idx:end_idx]
                subtasks = json.loads(json_data)
            else:
                parsed_json = json.loads(plan_response)
                if isinstance(parsed_json, dict) and "subtasks" in parsed_json:
                    subtasks = parsed_json["subtasks"]
                elif isinstance(parsed_json, list):
                    subtasks = parsed_json
        except Exception:
            # Fallback subtasks if parsing failed
            subtasks = [
                {"agent": "ResearchAgent", "task": f"Research details and key requirements for: {problem_statement}"},
                {"agent": "PlannerAgent", "task": f"Structure the flow and step-by-step logic for: {problem_statement}"},
                {"agent": "CoderAgent", "task": f"Write Python code/boilerplate for: {problem_statement}"}
            ]

        # 2. Sequential execution of subtasks
        execution_results = []
        context_accumulator = ""

        for idx, subtask in enumerate(subtasks):
            agent_name = subtask.get("agent", "CoderAgent")
            task_desc = subtask.get("task", "")

            # Default to CoderAgent if agent name is not recognized
            if agent_name not in self.agents:
                agent_name = "CoderAgent"

            agent = self.agents[agent_name]

            # Execute agent task with accrued context
            result = agent.execute_task(task_desc, context=context_accumulator)

            # Accumulate context
            context_accumulator += f"\n--- Step {idx+1} ({agent_name} Output) ---\n{result}\n"

            # Log subtask completion to memory
            self.memory_manager.add_to_session(
                session_id,
                sender=agent_name,
                message=f"Task: {task_desc}\nResult: {result}",
                role="assistant"
            )

            execution_results.append({
                "step": idx + 1,
                "agent": agent_name,
                "task": task_desc,
                "result": result
            })

        # 3. Final synthesis
        synthesis_prompt = (
            f"Synthesize the accumulated results into a unified, high-quality, professional solution addressable to the user's request. "
            f"Keep all critical code, research findings, and action items intact.\n\n"
            f"User original request: \"{problem_statement}\"\n"
            f"Accumulated Context:\n{context_accumulator}"
        )

        final_solution = self.provider.generate(
            prompt=synthesis_prompt,
            system_message="You are the Lead Gen Alpha Orchestrator synthesizing multi-agent results."
        )

        # Store final response
        self.memory_manager.add_to_session(session_id, "Orchestrator", final_solution, role="assistant")

        return {
            "session_id": session_id,
            "problem": problem_statement,
            "subtasks": subtasks,
            "execution_steps": execution_results,
            "final_solution": final_solution
        }
