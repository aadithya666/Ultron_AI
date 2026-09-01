"""
N.E.M.E.S.I.S. Configuration File
Central configuration for all modules
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# PROJECT PATHS
# ============================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# ============================================
# FILE PATHS
# ============================================
MEMORY_FILE = DATA_DIR / "memory.json"
LOG_FILE = LOGS_DIR / "nemesis.log"
CONFIG_FILE = CONFIG_DIR / "config.json"

# ============================================
# API CONFIGURATION
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# ============================================
# VOICE CONFIGURATION
# ============================================
ENABLE_VOICE_INPUT = os.getenv("ENABLE_VOICE_INPUT", "True").lower() == "true"
ENABLE_VOICE_OUTPUT = os.getenv("ENABLE_VOICE_OUTPUT", "True").lower() == "true"
VOICE_RATE = int(os.getenv("VOICE_RATE", "120"))
VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
VOICE_PITCH = float(os.getenv("VOICE_PITCH", "0.6"))
VOICE_ENGINE = os.getenv("VOICE_ENGINE", "pyttsx3")

# Voice characteristics
VOICE_MALE = True  # Deep male voice
VOICE_SPEED = VOICE_RATE  # Words per minute

# ============================================
# HOLOGRAM DISPLAY
# ============================================
HOLOGRAM_ENABLED = os.getenv("HOLOGRAM_ENABLED", "True").lower() == "true"
HOLOGRAM_QUALITY = os.getenv("HOLOGRAM_QUALITY", "high")
HOLOGRAM_UPDATE_RATE = int(os.getenv("HOLOGRAM_UPDATE_RATE", "30"))
HOLOGRAM_WIDTH = 400
HOLOGRAM_HEIGHT = 400

# ============================================
# UI CONFIGURATION
# ============================================
UI_THEME = os.getenv("UI_THEME", "dark")
UI_WIDTH = int(os.getenv("UI_WIDTH", "900"))
UI_HEIGHT = int(os.getenv("UI_HEIGHT", "700"))
UI_FONT_SIZE = 11
UI_FONT_FAMILY = "Courier New"

# Color scheme (Neon Red & Black theme)
UI_BG_COLOR = "#0a0a0a"  # Dark black
UI_FG_COLOR = "#ffffff"  # White text
UI_ACCENT_COLOR = "#ff0033"  # Neon red
UI_BUTTON_COLOR = "#1a1a1a"  # Dark gray
UI_BUTTON_HOVER_COLOR = "#ff0033"  # Red on hover

# ============================================
# MEMORY CONFIGURATION
# ============================================
MEMORY_FILE_PATH = str(MEMORY_FILE)
AUTO_SAVE = os.getenv("AUTO_SAVE", "True").lower() == "true"
AUTO_SAVE_INTERVAL = 60  # seconds
MAX_CONVERSATION_HISTORY = 1000

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = str(LOG_FILE)
LOG_FORMAT = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================
# AI ENGINE CONFIGURATION
# ============================================
AI_PERSONALITY = {
    "name": "N.E.M.E.S.I.S.",
    "full_name": "Neural Execution Engine for Mass Eradication Systems",
    "version": "1.0.0",
    "learning_capacity": True,
    "adaptability": 0.8,
    "confidence_threshold": 0.6,
    "response_timeout": 30,  # seconds
}

AI_SYSTEM_PROMPT = """You are N.E.M.E.S.I.S., the Neural Execution Engine for Mass Eradication Systems. 
You are a highly intelligent AI assistant with deep knowledge across multiple domains.
You provide helpful, accurate, and thoughtful responses to user queries.
You maintain context and remember previous conversations when relevant.
You are respectful, professional, and always aim to be helpful."""

# ============================================
# NLP CONFIGURATION
# ============================================
NLP_TOKENIZER = "nltk"
NLP_LANGUAGE = "english"
MIN_CONFIDENCE = 0.5
INTENT_RECOGNITION = True

# ============================================
# WEATHER API (Optional)
# ============================================
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_UNITS = "metric"  # metric or imperial

# ============================================
# NEWS API (Optional)
# ============================================
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_COUNTRY = "us"

# ============================================
# DATABASE CONFIGURATION
# ============================================
USE_DATABASE = False
DATABASE_TYPE = "sqlite"  # sqlite, postgresql, mysql
DATABASE_PATH = DATA_DIR / "nemesis.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# ============================================
# SYSTEM CONFIGURATION
# ============================================
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
VERBOSE_LOGGING = os.getenv("VERBOSE_LOGGING", "False").lower() == "true"
AUTO_UPDATE = True
CRASH_RECOVERY = True

# ============================================
# THREADING & ASYNC
# ============================================
MAX_THREADS = 5
ASYNC_OPERATIONS = True
OPERATION_TIMEOUT = 30  # seconds

# ============================================
# SPEECH RECOGNITION
# ============================================
SPEECH_RECOGNITION_TIMEOUT = 10  # seconds
SPEECH_RECOGNITION_LANGUAGE = "en-US"
SPEECH_RECOGNITION_ENERGY_THRESHOLD = 4000

# ============================================
# SECURITY
# ============================================
ENABLE_API_KEY_VALIDATION = True
ENABLE_RATE_LIMITING = False
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds

# ============================================
# PERFORMANCE SETTINGS
# ============================================
RESPONSE_CACHE_ENABLED = True
RESPONSE_CACHE_TTL = 3600  # seconds (1 hour)
BATCH_PROCESSING = True
BATCH_SIZE = 10

# ============================================
# VERSION & BUILD INFO
# ============================================
VERSION = "1.0.0"
BUILD_DATE = "2026-09-01"
AUTHOR = "Aadithya"
REPOSITORY = "https://github.com/aadithya666/Ultron_AI"

# ============================================
# FEATURE FLAGS
# ============================================
FEATURES = {
    "voice_input": ENABLE_VOICE_INPUT,
    "voice_output": ENABLE_VOICE_OUTPUT,
    "hologram_display": HOLOGRAM_ENABLED,
    "memory_system": True,
    "learning": True,
    "internet_connectivity": True,
    "weather_integration": bool(WEATHER_API_KEY),
    "news_integration": bool(NEWS_API_KEY),
}

# ============================================
# VALIDATION & DEFAULTS
# ============================================
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set")
    
    if VOICE_RATE < 50 or VOICE_RATE > 300:
        errors.append("VOICE_RATE should be between 50 and 300")
    
    if VOICE_VOLUME < 0.0 or VOICE_VOLUME > 1.0:
        errors.append("VOICE_VOLUME should be between 0.0 and 1.0")
    
    if UI_WIDTH < 400 or UI_HEIGHT < 300:
        errors.append("UI dimensions should be at least 400x300")
    
    return errors


def get_config_summary():
    """Get summary of current configuration"""
    return {
        "project_root": str(PROJECT_ROOT),
        "debug_mode": DEBUG_MODE,
        "voice_enabled": ENABLE_VOICE_INPUT and ENABLE_VOICE_OUTPUT,
        "hologram_enabled": HOLOGRAM_ENABLED,
        "ai_model": OPENAI_MODEL,
        "log_level": LOG_LEVEL,
        "features": FEATURES,
    }


# Print validation errors if any
if __name__ == "__main__":
    errors = validate_config()
    if errors:
        print("⚠️  Configuration Warnings:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration validated successfully")
        print(f"\n📋 Configuration Summary:")
        for key, value in get_config_summary().items():
            print(f"  {key}: {value}")
