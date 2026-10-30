"""
N.E.M.E.S.I.S. NLP Processor
Natural Language Processing and text analysis
"""

import re
from collections import Counter
from typing import Dict, List

import nltk
from nltk.corpus import stopwords
from nltk.pos_tag import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob

from config.config import DEBUG_MODE, NLP_LANGUAGE


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


SLANG_MAP = {
    "gonna": "going to",
    "gotta": "got to",
    "wanna": "want to",
    "lemme": "let me",
    "y'all": "you all",
    "ya": "you",
    "u": "you",
    "r": "are",
    "pls": "please",
    "plz": "please",
    "fr": "for real",
    "bro": "brother",
    "nah": "no",
    "idk": "I do not know",
    "imo": "in my opinion",
    "smh": "shaking my head",
    "wtf": "what the hell",
    "omg": "oh my god",
    "b4": "before",
    "neva": "never",
    "luv": "love",
    "wanna": "want to",
    "ain't": "is not",
    "can't": "cannot",
    "won't": "will not",
}


class NLPProcessor:
    """Natural Language Processing module"""

    def __init__(self):
        self.language = NLP_LANGUAGE
        self.stop_words = set(stopwords.words(self.language))
        if DEBUG_MODE:
            print("[DEBUG] NLP Processor initialized")

    def normalize_slang(self, text: str) -> str:
        """Convert common slang and informal speech into clearer English."""
        normalized = text.lower()
        for slang, expanded in SLANG_MAP.items():
            normalized = re.sub(rf"\b{re.escape(slang)}\b", expanded, normalized)

        normalized = normalized.replace("'", " ")
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def process(self, text: str) -> str:
        """Main NLP processing pipeline."""
        text = self.normalize_slang(text)
        text = self.clean_text(text)
        tokens = self.tokenize(text)
        tokens = [t for t in tokens if t.lower() not in self.stop_words]
        processed_text = ' '.join(tokens)

        if DEBUG_MODE:
            print(f"[DEBUG] Processed text: {processed_text}")

        return processed_text

    def clean_text(self, text: str) -> str:
        """Clean text by removing special characters."""
        text = text.lower()
        text = ' '.join(text.split())
        return text

    def tokenize(self, text: str) -> List[str]:
        return word_tokenize(text)

    def extract_sentences(self, text: str) -> List[str]:
        return sent_tokenize(text)

    def analyze_sentiment(self, text: str) -> Dict:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        if polarity > 0.1:
            sentiment_label = "positive"
        elif polarity < -0.1:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        return {
            "sentiment": sentiment_label,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
        }

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)

        entities = {"nouns": [], "verbs": [], "adjectives": []}

        for word, tag in pos_tags:
            if tag.startswith('NN'):
                entities["nouns"].append(word)
            elif tag.startswith('VB'):
                entities["verbs"].append(word)
            elif tag.startswith('JJ'):
                entities["adjectives"].append(word)

        return entities

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        tokens = word_tokenize(text.lower())
        keywords = [t for t in tokens if t.isalnum() and t not in self.stop_words]
        freq_dist = Counter(keywords)
        return [kw for kw, _ in freq_dist.most_common(top_n)]

    def detect_language(self, text: str) -> str:
        blob = TextBlob(text)
        try:
            return blob.detect_language()
        except Exception:
            return "unknown"

    def correct_spelling(self, text: str) -> str:
        blob = TextBlob(text)
        return str(blob.correct())

    def get_word_frequency(self, text: str) -> Dict[str, int]:
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t.isalnum()]
        freq_dist = Counter(tokens)
        return dict(freq_dist)

    def summarize(self, text: str, num_sentences: int = 3) -> str:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text

        words = word_tokenize(text.lower())
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1

        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            sentence_words = word_tokenize(sentence.lower())
            score = sum(freq.get(word, 0) for word in sentence_words)
            sentence_scores[i] = score

        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        top_sentences.sort()
        return ' '.join(sentences[i] for i in top_sentences)

    def analyze_readability(self, text: str) -> Dict:
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        readability_score = min(100, max(0, 206.835 - 1.015 * avg_words_per_sentence - 84.6 * (1 if avg_words_per_sentence > 15 else 0)))

        return {
            "sentence_count": len(sentences),
            "word_count": len(words),
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "readability_score": round(readability_score, 2),
        }
