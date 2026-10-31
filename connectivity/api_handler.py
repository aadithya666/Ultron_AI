"""
Memory module for Ultron.
Stores and retrieves conversation history and learned information.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List


class Memory:
    """Memory management for Ultron AI."""

    def __init__(self, memory_file: str = "data/memory.json"):
        self.memory_file = memory_file
        self.memory = self.load_memory()
        self.session_memory = []
        self.learned_patterns = {}

    def load_memory(self) -> Dict:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                return self.create_empty_memory()
        return self.create_empty_memory()

    def create_empty_memory(self) -> Dict:
        return {
            "user_preferences": {},
            "learned_responses": {},
            "frequent_queries": {},
            "user_profile": {},
            "important_dates": {},
            "reminders": [],
            "sessions": [],
        }

    def save_memory(self):
        try:
            os.makedirs(os.path.dirname(self.memory_file) or ".", exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def remember_preference(self, key: str, value: Any):
        self.memory["user_preferences"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
        }
        self.save_memory()

    def get_preference(self, key: str) -> Any:
        if key in self.memory["user_preferences"]:
            return self.memory["user_preferences"][key]["value"]
        return None

    def learn_response(self, query: str, response: str, effectiveness: float = 0.8):
        self.memory["learned_responses"][query] = {
            "response": response,
            "effectiveness": effectiveness,
            "times_used": 0,
            "first_learned": datetime.now().isoformat(),
        }
        self.save_memory()

    def get_learned_response(self, query: str) -> str:
        if query in self.memory["learned_responses"]:
            entry = self.memory["learned_responses"][query]
            entry["times_used"] += 1
            self.save_memory()
            return entry["response"]
        return None

    def track_query(self, query: str):
        if query in self.memory["frequent_queries"]:
            self.memory["frequent_queries"][query]["count"] += 1
        else:
            self.memory["frequent_queries"][query] = {
                "count": 1,
                "first_asked": datetime.now().isoformat(),
            }
        self.save_memory()

    def get_frequent_queries(self, limit: int = 5) -> List[Dict]:
        sorted_queries = sorted(
            self.memory["frequent_queries"].items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        )
        return [{"query": q, "count": data["count"]} for q, data in sorted_queries[:limit]]

    def set_user_profile(self, profile_data: Dict):
        self.memory["user_profile"].update(profile_data)
        self.save_memory()

    def get_user_profile(self) -> Dict:
        return self.memory["user_profile"]

    def add_important_date(self, label: str, date: str):
        self.memory["important_dates"][label] = {
            "date": date,
            "added": datetime.now().isoformat(),
        }
        self.save_memory()

    def set_reminder(self, reminder: str, due_date: str = None):
        reminder_obj = {
            "text": reminder,
            "created": datetime.now().isoformat(),
            "due": due_date,
            "completed": False,
        }
        self.memory["reminders"].append(reminder_obj)
        self.save_memory()
        return reminder_obj

    def get_reminders(self, completed: bool = False) -> List[Dict]:
        return [r for r in self.memory["reminders"] if r["completed"] == completed]

    def complete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.memory["reminders"]):
            self.memory["reminders"][reminder_index]["completed"] = True
            self.save_memory()

    def add_to_session_memory(self, event: Dict):
        event["timestamp"] = datetime.now().isoformat()
        self.session_memory.append(event)

    def get_session_memory(self) -> List[Dict]:
        return self.session_memory.copy()

    def clear_session_memory(self):
        self.session_memory = []

    def learn_pattern(self, pattern: str, response: str):
        self.learned_patterns[pattern] = response

    def recognize_pattern(self, input_text: str) -> str:
        for pattern, response in self.learned_patterns.items():
            if pattern.lower() in input_text.lower():
                return response
        return None

    def get_memory_stats(self) -> Dict:
        return {
            "total_preferences": len(self.memory["user_preferences"]),
            "learned_responses": len(self.memory["learned_responses"]),
            "frequent_queries": len(self.memory["frequent_queries"]),
            "total_reminders": len(self.memory["reminders"]),
            "session_events": len(self.session_memory),
            "total_interactions": sum(item["count"] for item in self.memory["frequent_queries"].values()),
            "total_sessions": len(self.memory.get("sessions", [])),
        }

    def start_session(self):
        self.session_memory = []

    def end_session(self):
        self.memory.setdefault("sessions", []).append({
            "ended_at": datetime.now().isoformat(),
            "event_count": len(self.session_memory),
        })
        self.save_memory()
        self.session_memory = []
