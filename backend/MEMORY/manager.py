import os
import json
from typing import Dict, Any, List, Optional

class MemoryManager:
    """
    Manages short-term conversation logs and long-term memory elements for the agents.
    Provides session-based persistence using a local JSON file or in-memory fallback.
    """
    def __init__(self, memory_dir: str = "backend/MEMORY"):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)
        self.db_path = os.path.join(self.memory_dir, "memory_store.json")
        self.memories = self._load_store()

    def _load_store(self) -> Dict[str, Any]:
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    return json.load(f)
            except Exception:
                return {"sessions": {}, "long_term_memories": []}
        return {"sessions": {}, "long_term_memories": []}

    def _save_store(self):
        try:
            with open(self.db_path, "w") as f:
                json.dump(self.memories, f, indent=2)
        except Exception as e:
            # Silently handle fallback if writing fails during execution environments
            pass

    def add_to_session(self, session_id: str, sender: str, message: str, role: Optional[str] = None):
        """
        Adds an entry to short-term session conversation history.
        """
        if "sessions" not in self.memories:
            self.memories["sessions"] = {}
        if session_id not in self.memories["sessions"]:
            self.memories["sessions"][session_id] = []

        self.memories["sessions"][session_id].append({
            "sender": sender,
            "role": role or "assistant",
            "message": message
        })
        self._save_store()

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the conversation history of a specific session.
        """
        return self.memories.get("sessions", {}).get(session_id, [])

    def clear_session(self, session_id: str):
        """
        Clears short-term memory for a session.
        """
        if "sessions" in self.memories and session_id in self.memories["sessions"]:
            del self.memories["sessions"][session_id]
            self._save_store()

    def store_long_term_memory(self, memory_text: str, tags: Optional[List[str]] = None):
        """
        Stores key insights or guidelines for future reference (long-term memory).
        """
        if "long_term_memories" not in self.memories:
            self.memories["long_term_memories"] = []

        self.memories["long_term_memories"].append({
            "memory": memory_text,
            "tags": tags or []
        })
        self._save_store()

    def search_long_term_memories(self, keyword: str) -> List[str]:
        """
        Searches long-term memories matching keywords or tags.
        """
        results = []
        keyword_lower = keyword.lower()
        for entry in self.memories.get("long_term_memories", []):
            if (keyword_lower in entry["memory"].lower() or
                any(keyword_lower in tag.lower() for tag in entry.get("tags", []))):
                results.append(entry["memory"])
        return results
