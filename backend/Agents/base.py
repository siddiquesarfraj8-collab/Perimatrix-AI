from typing import List, Dict, Any, Optional
from backend.LLM.provider import LLMProvider

class BaseAgent:
    """
    Base Agent definition.
    Defines general traits (role, goal, backstory, tools) and provides standard invocation hooks.
    """
    def __init__(self, role: str, goal: str, backstory: str, provider: Optional[LLMProvider] = None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.provider = provider or LLMProvider()

    def get_system_prompt(self) -> str:
        return (
            f"You are a specialized AI Agent: {self.role}.\n"
            f"Your Goal: {self.goal}\n"
            f"Your Background: {self.backstory}\n\n"
            f"Always prioritize accurate execution of your designated task. Return clean, well-formatted results."
        )

    def execute_task(self, task_description: str, context: Optional[str] = None) -> str:
        prompt = f"Task to perform: {task_description}\n"
        if context:
            prompt += f"\nAdditional Context / Resources:\n{context}\n"

        return self.provider.generate(
            prompt=prompt,
            system_message=self.get_system_prompt()
        )

    async def execute_task_async(self, task_description: str, context: Optional[str] = None) -> str:
        prompt = f"Task to perform: {task_description}\n"
        if context:
            prompt += f"\nAdditional Context / Resources:\n{context}\n"

        return await self.provider.generate_async(
            prompt=prompt,
            system_message=self.get_system_prompt()
        )
