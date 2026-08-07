"""
Natural Language Processing module for Ultron
Handles text analysis and understanding
"""

import re
from typing import List, Dict, Tuple

class NLPProcessor:
    """Natural Language Processing for user input"""
    
    def __init__(self):
        self.stop_words = self.load_stop_words()
        self.context = {}
        
    def load_stop_words(self) -> List[str]:
        """Load common English stop words"""
        return [
            "the", "is", "at", "which", "on", "a", "an", "and", "or", "but",
            "in", "with", "by", "for", "of", "to", "from", "as", "be", "have",
            "has", "had", "do", "does", "did", "will", "would", "should", "could"
        ]
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Convert to lowercase and split by whitespace and punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """Remove stop words from tokens"""
        return [token for token in tokens if token not in self.stop_words]
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        tokens = self.tokenize(text)
        keywords = self.remove_stop_words(tokens)
        return keywords
    
    def sentiment_analysis(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        positive_words = ["good", "great", "excellent", "happy", "love", "best", "amazing"]
        negative_words = ["bad", "terrible", "hate", "angry", "worst", "awful", "sad"]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = min(positive_count / (positive_count + negative_count + 1), 1.0)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = min(negative_count / (positive_count + negative_count + 1), 1.0)
        else:
            sentiment = "neutral"
            score = 0.5
        
        return {
            "sentiment": sentiment,
            "score": score,
            "positive_words": positive_count,
            "negative_words": negative_count
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        entities = {
            "people": [],
            "locations": [],
            "organizations": [],
            "dates": [],
            "numbers": []
        }
        
        # Simple regex-based entity extraction
        # Dates
        date_pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        entities["dates"] = re.findall(date_pattern, text)
        
        # Numbers
        number_pattern = r'\b\d+(?:\.\d+)?\b'
        entities["numbers"] = re.findall(number_pattern, text)
        
        return entities
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        tokens1 = set(self.remove_stop_words(self.tokenize(text1)))
        tokens2 = set(self.remove_stop_words(self.tokenize(text2)))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union)
    
    def find_similar_queries(self, query: str, previous_queries: List[str], threshold: float = 0.6) -> List[str]:
        """Find similar queries from history"""
        similar = []
        for prev_query in previous_queries:
            score = self.similarity_score(query, prev_query)
            if score >= threshold:
                similar.append(prev_query)
        return similar
    
    def parse_command(self, text: str) -> Dict:
        """Parse text as a command"""
        tokens = self.tokenize(text)
        
        command_info = {
            "command": None,
            "parameters": [],
            "modifiers": []
        }
        
        # Simple command parsing
        if tokens:
            command_info["command"] = tokens[0]
            command_info["parameters"] = tokens[1:]
        
        return command_info
    
    def generate_response_template(self, intent: str) -> str:
        """Generate response template based on intent"""
        templates = {
            "greeting": "Greetings, {user}. How may I assist you?",
            "confirmation": "Understood. {action} has been {status}.",
            "error": "I encountered an issue: {error}. Please try again.",
            "information": "Based on my analysis: {info}",
            "clarification": "Could you clarify: {question}?",
            "action": "Executing {action}. Please stand by."
        }
        
        return templates.get(intent, "I'm processing your request.")
    
    def correct_spelling(self, text: str) -> str:
        """Basic spelling correction (can be enhanced)"""
        # This is a simple placeholder - real implementation would use spell checker
        return text
    
    def language_detection(self, text: str) -> str:
        """Detect language of text"""
        # Simplified language detection
        # In production, use libraries like langdetect or textblob
        return "en"  # Default to English
