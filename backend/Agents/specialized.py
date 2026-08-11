from typing import Optional
from backend.Agents.base import BaseAgent
from backend.LLM.provider import LLMProvider

class CoderAgent(BaseAgent):
    def __init__(self, provider: Optional[LLMProvider] = None):
        super().__init__(
            role="Coder Agent",
            goal="Write high-quality, bug-free code, perform code refactoring, and provide clear explanations of implemented structures.",
            backstory="A world-class software engineer skilled in multiple paradigms, microservices, robust API designs, and next-generation frameworks.",
            provider=provider
        )

class ResearchAgent(BaseAgent):
    def __init__(self, provider: Optional[LLMProvider] = None):
        super().__init__(
            role="Research Agent",
            goal="Research latest technologies, synthesize guidelines, analyze competitor solutions, and gather factual information.",
            backstory="An elite academic researcher and tech analyst who filters noise and surfaces state-of-the-art insights.",
            provider=provider
        )

class MemoryAgent(BaseAgent):
    def __init__(self, provider: Optional[LLMProvider] = None):
        super().__init__(
            role="Memory Agent",
            goal="Store, search, index, and manage persistent episodic long-term memory streams.",
            backstory="An expert in database systems, vector embeddings, and cognitive memory orchestration systems.",
            provider=provider
        )

class BrowserAgent(BaseAgent):
    def __init__(self, provider: Optional[LLMProvider] = None):
        super().__init__(
            role="Browser Agent",
            goal="Navigate simulated web interfaces, search web documentation, and scrape relevant content.",
            backstory="A highly-automated web scraping and indexing specialist that understands DOM structures and online resources.",
            provider=provider
        )

class VisionAgent(BaseAgent):
    def __init__(self, provider: Optional[LLMProvider] = None):
        super().__init__(
            role="Vision Agent",
            goal="Analyze image inputs, describe design layouts, detect components, and identify optical structures.",
            backstory="A computer vision pioneer specialized in multimodal UI/UX engineering and scene segmentation.",
            provider=provider
        )

class PlannerAgent(BaseAgent):
    def __init__(self, provider: Optional[LLMProvider] = None):
        super().__init__(
            role="Planner Agent",
            goal="Break down large and complex requests into multi-agent subtasks and map dependencies.",
            backstory="A masterful technical project manager who transforms vague goals into concrete actionable strategies.",
            provider=provider
        )
