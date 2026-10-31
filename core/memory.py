"""
N.E.M.E.S.I.S. AI Engine
Core Gemini-based AI response generation.
"""

import os
from typing import Dict, List

from config.config import AI_PERSONALITY, AI_SYSTEM_PROMPT, DEBUG_MODE, GEMINI_API_KEY, GEMINI_MODEL

try:
    from google import genai
except ImportError:  # pragma: no cover
    genai = None


class AIEngine:
    """Main AI engine for generating responses using Gemini."""

    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL", GEMINI_MODEL)
        self.personality = AI_PERSONALITY
        self.conversation_history: List[Dict] = []
        self.system_prompt = AI_SYSTEM_PROMPT
        self.response_cache: Dict = {}
        self.api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)

        self.client = None
        if genai is not None and self.api_key:
            self.client = genai.Client(api_key=self.api_key)

        if DEBUG_MODE:
            print("[DEBUG] AI Engine initialized with model:", self.model)

    def _extract_text(self, response) -> str:
        """Pull plain text from a Gemini response object."""
        if response is None:
            return ""

        text = getattr(response, "text", None)
        if text:
            return text.strip()

        try:
            candidates = getattr(response, "candidates", None)
            if candidates:
                content = getattr(candidates[0], "content", None)
                if content is not None:
                    parts = getattr(content, "parts", None)
                    if parts:
                        first = getattr(parts[0], "text", None)
                        if first:
                            return first.strip()
        except Exception:
            pass

        return ""

    def generate_response(self, user_input: str) -> str:
        """Generate an AI response for user input."""
        try:
            if not user_input:
                return ""

            if user_input in self.response_cache:
                if DEBUG_MODE:
                    print("[DEBUG] Response found in cache")
                return self.response_cache[user_input]

            if not self.api_key or self.client is None:
                return "Gemini is not configured. Set GEMINI_API_KEY in your .env file."

            messages = [{"role": "user", "content": user_input}]
            for msg in self.conversation_history[-10:]:
                messages.append(msg)

            prompt = self.system_prompt + "\n\nConversation context:\n"
            for message in messages:
                if isinstance(message, dict):
                    prompt += f"{message.get('role', 'user')}: {message.get('content', '')}\n"
            prompt += f"\nUser: {user_input}"

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            ai_response = self._extract_text(response)

            if not ai_response:
                return "Gemini returned an empty response."

            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            if len(self.conversation_history) > 100:
                self.conversation_history = self.conversation_history[-100:]

            self.response_cache[user_input] = ai_response
            if DEBUG_MODE:
                print(f"[DEBUG] Generated response length: {len(ai_response)}")
            return ai_response

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    def get_mood(self) -> str:
        mood_map = {
            0: "Analytical",
            1: "Helpful",
            2: "Engaged",
            3: "Attentive",
            4: "Curious",
        }
        mood_index = len(self.conversation_history) % 5
        return mood_map.get(mood_index, "Neutral")

    def clear_history(self):
        self.conversation_history = []
        self.response_cache = {}
        if DEBUG_MODE:
            print("[DEBUG] Conversation history cleared")

    def get_context(self) -> Dict:
        return {
            "personality": self.personality,
            "conversation_length": len(self.conversation_history),
            "mood": self.get_mood(),
            "cache_size": len(self.response_cache),
        }
