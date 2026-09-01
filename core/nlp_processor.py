"""
N.E.M.E.S.I.S. NLP Processor
Natural Language Processing and text analysis
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.pos_tag import pos_tag
from textblob import TextBlob
from typing import List, Dict, Tuple
from config.config import NLP_LANGUAGE, DEBUG_MODE

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


class NLPProcessor:
    """Natural Language Processing module"""
    
    def __init__(self):
        """Initialize NLP Processor"""
        self.language = NLP_LANGUAGE
        self.stop_words = set(stopwords.words(self.language))
        
        if DEBUG_MODE:
            print("[DEBUG] NLP Processor initialized")
    
    def process(self, text: str) -> str:
        """
        Main NLP processing pipeline
        
        Args:
            text: Raw text input
            
        Returns:
            Processed text
        """
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stopwords
        tokens = [t for t in tokens if t.lower() not in self.stop_words]
        
        # Join back
        processed_text = ' '.join(tokens)
        
        if DEBUG_MODE:
            print(f"[DEBUG] Processed text: {processed_text}")
        
        return processed_text
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        tokens = word_tokenize(text)
        return tokens
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Text to analyze
            
        Returns:
            List of sentences
        """
        sentences = sent_tokenize(text)
        return sentences
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment analysis
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment_label = "positive"
        elif polarity < -0.1:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return {
            "sentiment": sentiment_label,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of entity types and values
        """
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        
        # Simple entity extraction by POS tags
        entities = {
            "nouns": [],
            "verbs": [],
            "adjectives": []
        }
        
        for word, tag in pos_tags:
            if tag.startswith('NN'):
                entities["nouns"].append(word)
            elif tag.startswith('VB'):
                entities["verbs"].append(word)
            elif tag.startswith('JJ'):
                entities["adjectives"].append(word)
        
        return entities
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Text to analyze
            top_n: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Tokenize and filter
        tokens = word_tokenize(text.lower())
        keywords = [t for t in tokens if t.isalnum() and t not in self.stop_words]
        
        # Count frequency
        from collections import Counter
        freq_dist = Counter(keywords)
        
        # Get top keywords
        top_keywords = [kw for kw, _ in freq_dist.most_common(top_n)]
        
        return top_keywords
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code
        """
        blob = TextBlob(text)
        try:
            language = blob.detect_language()
            return language
        except:
            return "unknown"
    
    def correct_spelling(self, text: str) -> str:
        """
        Correct spelling in text
        
        Args:
            text: Text to correct
            
        Returns:
            Corrected text
        """
        blob = TextBlob(text)
        corrected = str(blob.correct())
        return corrected
    
    def get_word_frequency(self, text: str) -> Dict[str, int]:
        """
        Get word frequency distribution
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of word frequencies
        """
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t.isalnum()]
        
        from collections import Counter
        freq_dist = Counter(tokens)
        
        return dict(freq_dist)
    
    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """
        Summarize text (simple extractive summary)
        
        Args:
            text: Text to summarize
            num_sentences: Number of sentences in summary
            
        Returns:
            Summary text
        """
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Simple scoring based on word frequency
        words = word_tokenize(text.lower())
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            sentence_words = word_tokenize(sentence.lower())
            score = sum(freq.get(word, 0) for word in sentence_words)
            sentence_scores[i] = score
        
        # Get top sentences
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        top_sentences.sort()
        
        # Build summary
        summary = ' '.join(sentences[i] for i in top_sentences)
        
        return summary
    
    def analyze_readability(self, text: str) -> Dict:
        """
        Analyze text readability
        
        Args:
            text: Text to analyze
            
        Returns:
            Readability metrics
        """
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        
        # Simple readability score (0-100)
        # Higher = more readable
        readability_score = min(100, max(0, 206.835 - 1.015 * avg_words_per_sentence - 84.6 * (1 if avg_words_per_sentence > 15 else 0)))
        
        return {
            "sentence_count": len(sentences),
            "word_count": len(words),
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "readability_score": round(readability_score, 2)
        }
