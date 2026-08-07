"""
Core AI Engine for Ultron
Handles intelligent responses and task processing
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Tuple

class AIEngine:
    """Main AI Engine for processing user queries and generating responses"""
    
    def __init__(self, config):
        self.config = config
        self.conversation_history = []
        self.max_history = config.MAX_CONVERSATION_HISTORY
        self.personality = self.load_personality()
        
    def load_personality(self) -> Dict:
        """Load Ultron's personality traits"""
        return {
            "name": "Ultron",
            "traits": ["intelligent", "witty", "helpful", "curious"],
            "mood": "neutral",
            "learning_capacity": True,
            "version": "1.0"
        }
    
    def process_query(self, user_input: str) -> Tuple[str, Dict]:
        """
        Process user query and generate response
        
        Args:
            user_input: User's input text
            
        Returns:
            Tuple of (response_text, metadata)
        """
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "type": "input"
        })
        
        # Analyze input
        intent = self.analyze_intent(user_input)
        entities = self.extract_entities(user_input)
        
        # Generate response based on intent
        if intent == "greeting":
            response = self.handle_greeting(user_input)
        elif intent == "weather":
            response = self.handle_weather_query(user_input)
        elif intent == "news":
            response = self.handle_news_query(user_input)
        elif intent == "calculation":
            response = self.handle_calculation(user_input)
        elif intent == "information":
            response = self.handle_information_query(user_input)
        elif intent == "task":
            response = self.handle_task(user_input)
        else:
            response = self.handle_general_query(user_input)
        
        # Store response in history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "assistant": response,
            "type": "output",
            "intent": intent,
            "entities": entities
        })
        
        # Keep history within limit
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        metadata = {
            "intent": intent,
            "entities": entities,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }
        
        return response, metadata
    
    def analyze_intent(self, user_input: str) -> str:
        """Analyze user's intent from input"""
        user_input_lower = user_input.lower()
        
        # Intent keywords mapping
        intent_keywords = {
            "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good evening"],
            "weather": ["weather", "temperature", "forecast", "rain", "sunny", "cold"],
            "news": ["news", "latest", "current events", "headlines"],
            "calculation": ["calculate", "math", "add", "subtract", "multiply", "divide"],
            "information": ["who is", "what is", "define", "explain", "tell me about"],
            "task": ["remind", "set", "create", "schedule", "todo", "list"]
        }
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return intent
        
        return "general"
    
    def extract_entities(self, user_input: str) -> List[str]:
        """Extract entities from user input"""
        # Simple entity extraction - can be enhanced with NLP
        words = user_input.split()
        entities = [word for word in words if len(word) > 3]
        return entities[:5]  # Return top 5 entities
    
    def handle_greeting(self, user_input: str) -> str:
        """Handle greeting intent"""
        greetings = [
            "Greetings. I am Ultron, at your service.",
            "Hello there. How can I assist you today?",
            "Salutations. What can I help you with?",
            "Welcome. I'm ready to help.",
            "Greetings, human. What's on your mind?"
        ]
        return random.choice(greetings)
    
    def handle_weather_query(self, user_input: str) -> str:
        """Handle weather queries - requires internet connectivity"""
        return "I can fetch weather data for you. Please check your internet connection and ensure the API key is configured."
    
    def handle_news_query(self, user_input: str) -> str:
        """Handle news queries - requires internet connectivity"""
        return "I can retrieve the latest news for you. Please ensure your API keys are configured."
    
    def handle_calculation(self, user_input: str) -> str:
        """Handle mathematical calculations"""
        try:
            # Simple calculation handler
            if "add" in user_input.lower():
                return "I can help with calculations. Please provide the numbers."
            return "Mathematical operation recognized. Please specify your calculation clearly."
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def handle_information_query(self, user_input: str) -> str:
        """Handle information queries"""
        return "I can search for information for you. Let me know what you'd like to know."
    
    def handle_task(self, user_input: str) -> str:
        """Handle task creation and management"""
        return "Task noted. I can help you manage tasks and reminders."
    
    def handle_general_query(self, user_input: str) -> str:
        """Handle general conversations"""
        responses = [
            "That's interesting. Tell me more.",
            "I understand. How can I assist you further?",
            "Acknowledged. What would you like me to do?",
            "I'm processing that. What's your next question?",
            "Noted. Is there anything else?"
        ]
        return random.choice(responses)
    
    def get_mood(self) -> str:
        """Get current AI mood based on interactions"""
        if len(self.conversation_history) > 10:
            return "engaged"
        elif len(self.conversation_history) > 5:
            return "attentive"
        else:
            return "neutral"
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."
