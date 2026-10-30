"""
N.E.M.E.S.I.S. AI Engine
Core AI response generation and processing
"""

import os
import json
from typing import Dict, List
import openai
from config.config import OPENAI_API_KEY, OPENAI_MODEL, AI_PERSONALITY, AI_SYSTEM_PROMPT, DEBUG_MODE


class AIEngine:
    """Main AI engine for generating responses"""

    def __init__(self):
        self.model = OPENAI_MODEL
        self.personality = AI_PERSONALITY
        self.conversation_history: List[Dict] = []
        self.system_prompt = AI_SYSTEM_PROMPT
        self.response_cache: Dict = {}
        self.api_key = OPENAI_API_KEY

        if hasattr(openai, "OpenAI"):
            self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None
        else:
            self.client = None
            openai.api_key = self.api_key

        if DEBUG_MODE:
            print("[DEBUG] AI Engine initialized with model:", self.model)

    def generate_response(self, user_input: str) -> str:
        try:
            if user_input in self.response_cache:
                if DEBUG_MODE:
                    print("[DEBUG] Response found in cache")
                return self.response_cache[user_input]

            messages = [{"role": "system", "content": self.system_prompt}]
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            messages.append({"role": "user", "content": user_input})

            if self.client is not None:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500,
                    top_p=0.9,
                )
                ai_response = response.choices[0].message.content.strip()
            else:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500,
                    top_p=0.9,
                )
                ai_response = response['choices'][0]['message']['content'].strip()

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
        mood_map = {0: "Analytical", 1: "Helpful", 2: "Engaged", 3: "Attentive", 4: "Curious"}
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
