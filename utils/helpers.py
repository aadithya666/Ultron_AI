"""
Helper utilities for Ultron AI
Provides common utility functions
"""

import re
from typing import List, Dict, Any, Tuple
import time


class TextHelpers:
    """Text processing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """Extract numbers from text"""
        number_pattern = r'[-+]?\d*\.?\d+'
        matches = re.findall(number_pattern, text)
        return [float(num) for num in matches]
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to max length"""
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text
    
    @staticmethod
    def capitalize_sentences(text: str) -> str:
        """Capitalize first letter of sentences"""
        sentences = re.split(r'([.!?])', text)
        result = []
        
        for i, sentence in enumerate(sentences):
            if sentence and i % 2 == 0:  # Actual sentences
                result.append(sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper())
            else:
                result.append(sentence)
        
        return ''.join(result)
    
    @staticmethod
    def remove_special_characters(text: str, keep_spaces: bool = True) -> str:
        """Remove special characters from text"""
        if keep_spaces:
            pattern = r'[^a-zA-Z0-9\s]'
        else:
            pattern = r'[^a-zA-Z0-9]'
        return re.sub(pattern, '', text)


class TimeHelpers:
    """Time and date utilities"""
    
    @staticmethod
    def get_current_time() -> str:
        """Get current time as string"""
        return time.strftime("%H:%M:%S")
    
    @staticmethod
    def get_current_date() -> str:
        """Get current date as string"""
        return time.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_timestamp() -> float:
        """Get current timestamp"""
        return time.time()
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Format seconds into readable time"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    @staticmethod
    def time_since(timestamp: float) -> str:
        """Get readable time since timestamp"""
        elapsed = time.time() - timestamp
        return TimeHelpers.format_time(elapsed)


class ValidationHelpers:
    """Input validation utilities"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL"""
        pattern = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number"""
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None
    
    @staticmethod
    def is_empty(value: Any) -> bool:
        """Check if value is empty"""
        if value is None:
            return True
        if isinstance(value, str):
            return len(value.strip()) == 0
        if isinstance(value, (list, dict, tuple)):
            return len(value) == 0
        return False
    
    @staticmethod
    def validate_input(text: str, min_length: int = 1, max_length: int = 1000) -> Tuple[bool, str]:
        """Validate input text"""
        if ValidationHelpers.is_empty(text):
            return False, "Input cannot be empty"
        
        if len(text) < min_length:
            return False, f"Input must be at least {min_length} characters"
        
        if len(text) > max_length:
            return False, f"Input must not exceed {max_length} characters"
        
        return True, "Valid"


class DataHelpers:
    """Data processing utilities"""
    
    @staticmethod
    def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
        """Merge two dictionaries"""
        result = dict1.copy()
        result.update(dict2)
        return result
    
    @staticmethod
    def filter_dict(data: Dict, keys: List[str]) -> Dict:
        """Filter dictionary by keys"""
        return {k: v for k, v in data.items() if k in keys}
    
    @staticmethod
    def deep_get(data: Dict, keys: List[str], default: Any = None) -> Any:
        """Deep get from nested dictionary"""
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key)
            else:
                return default
        return result if result is not None else default
    
    @staticmethod
    def flatten_list(nested_list: List) -> List:
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(DataHelpers.flatten_list(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def remove_duplicates(items: List) -> List:
        """Remove duplicates from list while preserving order"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def chunk_list(items: List, chunk_size: int) -> List[List]:
        """Split list into chunks"""
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


class FormatHelpers:
    """Formatting utilities"""
    
    @staticmethod
    def format_number(number: float, decimals: int = 2) -> str:
        """Format number with decimals"""
        return f"{number:.{decimals}f}"
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes into readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    @staticmethod
    def format_percentage(value: float, total: float, decimals: int = 2) -> str:
        """Format as percentage"""
        if total == 0:
            return "0%"
        percentage = (value / total) * 100
        return f"{percentage:.{decimals}f}%"
    
    @staticmethod
    def format_dict_to_string(data: Dict, indent: int = 0) -> str:
        """Format dictionary to readable string"""
        result = []
        for key, value in data.items():
            if isinstance(value, dict):
                result.append(f"{'  ' * indent}{key}:")
                result.append(FormatHelpers.format_dict_to_string(value, indent + 1))
            else:
                result.append(f"{'  ' * indent}{key}: {value}")
        return '\n'.join(result)


# Convenience functions
def clean_text(text: str) -> str:
    """Clean text"""
    return TextHelpers.clean_text(text)


def is_valid_email(email: str) -> bool:
    """Validate email"""
    return ValidationHelpers.is_valid_email(email)


def get_current_time() -> str:
    """Get current time"""
    return TimeHelpers.get_current_time()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text"""
    return TextHelpers.truncate_text(text, max_length)
