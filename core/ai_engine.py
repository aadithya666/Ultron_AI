"""
N.E.M.E.S.I.S. AI Engine
Core AI response generation and processing
"""

import os
import json
from typing import Dict, Tuple, List, Optional
import openai
from config.config import (
    OPENAI_API_KEY, OPENAI_MODEL, AI_PERSONALITY, 
    AI_SYSTEM_PROMPT, DEBUG_MODE
)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY


class AIEngine:
    """Main AI engine for generating responses"""
    
    def __init__(self):
        """Initialize AI Engine"""
        self.model = OPENAI_MODEL
        self.personality = AI_PERSONALITY
        self.conversation_history: List[Dict] = []
        self.system_prompt = AI_SYSTEM_PROMPT
        self.response_cache: Dict = {}
        
        if DEBUG_MODE:
            print("[DEBUG] AI Engine initialized with model:", self.model)
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate AI response for user input
        
        Args:
            user_input: Processed user input
            
        Returns:
            AI response string
        """
        try:
            # Check cache first
            if user_input in self.response_cache:
                if DEBUG_MODE:
                    print("[DEBUG] Response found in cache")
                return self.response_cache[user_input]
            
            # Build messages for API
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history (last 5 exchanges)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )
            
            # Extract response text
            ai_response = response['choices'][0]['message']['content'].strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Limit history size
            if len(self.conversation_history) > 100:
                self.conversation_history = self.conversation_history[-100:]
            
            # Cache response
            self.response_cache[user_input] = ai_response
            
            if DEBUG_MODE:
                print(f"[DEBUG] Generated response length: {len(ai_response)}")
            
            return ai_response
        
        except openai.error.APIError as e:
            error_msg = f"OpenAI API Error: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
        
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def get_mood(self) -> str:
        """Get current AI mood based on conversation"""
        mood_map = {
            0: "Analytical",
            1: "Helpful",
            2: "Engaged",
            3: "Attentive",
            4: "Curious"
        }
        mood_index = len(self.conversation_history) % 5
        return mood_map.get(mood_index, "Neutral")
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.response_cache = {}
        if DEBUG_MODE:
            print("[DEBUG] Conversation history cleared")
    
    def get_context(self) -> Dict:
        """Get current AI context"""
        return {
            "personality": self.personality,
            "conversation_length": len(self.conversation_history),
            "mood": self.get_mood(),
            "cache_size": len(self.response_cache)
        }
