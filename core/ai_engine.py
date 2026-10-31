"""
N.E.M.E.S.I.S. Configuration File
Central configuration for all modules.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

MEMORY_FILE = DATA_DIR / "memory.json"
LOG_FILE = LOGS_DIR / "nemesis.log"
CONFIG_FILE = CONFIG_DIR / "config.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
AI_ENGINE_PROVIDER = os.getenv("AI_ENGINE_PROVIDER", "gemini")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

ENABLE_VOICE_INPUT = os.getenv("ENABLE_VOICE_INPUT", "True").lower() == "true"
ENABLE_VOICE_OUTPUT = os.getenv("ENABLE_VOICE_OUTPUT", "True").lower() == "true"
VOICE_RATE = int(os.getenv("VOICE_RATE", "120"))
VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
VOICE_PITCH = float(os.getenv("VOICE_PITCH", "0.6"))
VOICE_ENGINE = os.getenv("VOICE_ENGINE", "pyttsx3")
VOICE_MALE = True
VOICE_SPEED = VOICE_RATE

HOLOGRAM_ENABLED = os.getenv("HOLOGRAM_ENABLED", "True").lower() == "true"
HOLOGRAM_QUALITY = os.getenv("HOLOGRAM_QUALITY", "high")
HOLOGRAM_UPDATE_RATE = int(os.getenv("HOLOGRAM_UPDATE_RATE", "30"))
HOLOGRAM_WIDTH = 400
HOLOGRAM_HEIGHT = 400

UI_THEME = os.getenv("UI_THEME", "dark")
UI_WIDTH = int(os.getenv("UI_WIDTH", "900"))
UI_HEIGHT = int(os.getenv("UI_HEIGHT", "700"))
UI_FONT_SIZE = 11
UI_FONT_FAMILY = "Courier New"

UI_BG_COLOR = "#0a0a0a"
UI_FG_COLOR = "#ffffff"
UI_ACCENT_COLOR = "#ff0033"
UI_BUTTON_COLOR = "#1a1a1a"
UI_BUTTON_HOVER_COLOR = "#ff0033"

MEMORY_FILE_PATH = str(MEMORY_FILE)
AUTO_SAVE = os.getenv("AUTO_SAVE", "True").lower() == "true"
AUTO_SAVE_INTERVAL = 60
MAX_CONVERSATION_HISTORY = 1000

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = str(LOG_FILE)
LOG_FORMAT = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

AI_PERSONALITY = {
    "name": "N.E.M.E.S.I.S.",
    "full_name": "Neural Execution Engine for Mass Eradication Systems",
    "version": "1.0.0",
    "learning_capacity": True,
    "adaptability": 0.8,
    "confidence_threshold": 0.6,
    "response_timeout": 30,
}

AI_SYSTEM_PROMPT = """You are N.E.M.E.S.I.S., the Neural Execution Engine for Mass Eradication Systems.
You are a highly intelligent AI assistant with deep knowledge across multiple domains.
You provide helpful, accurate, and thoughtful responses to user queries.
You maintain context and remember previous conversations when relevant.
You are respectful, professional, and always aim to be helpful."""

NLP_TOKENIZER = "nltk"
NLP_LANGUAGE = "english"
MIN_CONFIDENCE = 0.5
INTENT_RECOGNITION = True

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_UNITS = "metric"

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_COUNTRY = "us"

USE_DATABASE = False
DATABASE_TYPE = "sqlite"
DATABASE_PATH = DATA_DIR / "nemesis.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
VERBOSE_LOGGING = os.getenv("VERBOSE_LOGGING", "False").lower() == "true"
AUTO_UPDATE = True
CRASH_RECOVERY = True

MAX_THREADS = 5
ASYNC_OPERATIONS = True
OPERATION_TIMEOUT = 30

SPEECH_RECOGNITION_TIMEOUT = 10
SPEECH_RECOGNITION_LANGUAGE = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "en-IN")
SPEECH_RECOGNITION_ENERGY_THRESHOLD = 4000

ENABLE_API_KEY_VALIDATION = True
ENABLE_RATE_LIMITING = False
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

RESPONSE_CACHE_ENABLED = True
RESPONSE_CACHE_TTL = 3600
BATCH_PROCESSING = True
BATCH_SIZE = 10

VERSION = "1.0.0"
BUILD_DATE = "2026-09-01"
AUTHOR = "Aadithya"
REPOSITORY = "https://github.com/aadithya666/Ultron_AI"

FEATURES = {
    "voice_input": ENABLE_VOICE_INPUT,
    "voice_output": ENABLE_VOICE_OUTPUT,
    "hologram_display": HOLOGRAM_ENABLED,
    "memory_system": True,
    "learning": True,
    "internet_connectivity": True,
    "weather_integration": bool(WEATHER_API_KEY),
    "news_integration": bool(NEWS_API_KEY),
    "gemini_ai": bool(GEMINI_API_KEY),
}


def validate_config():
    """Validate configuration settings."""
    errors = []
    if not GEMINI_API_KEY and not OPENAI_API_KEY:
        errors.append("GEMINI_API_KEY is not set")
    if VOICE_RATE < 50 or VOICE_RATE > 300:
        errors.append("VOICE_RATE should be between 50 and 300")
    if VOICE_VOLUME < 0.0 or VOICE_VOLUME > 1.0:
        errors.append("VOICE_VOLUME should be between 0.0 and 1.0")
    if UI_WIDTH < 400 or UI_HEIGHT < 300:
        errors.append("UI dimensions should be at least 400x300")
    return errors


def get_config_summary():
    """Get summary of current configuration."""
    return {
        "project_root": str(PROJECT_ROOT),
        "debug_mode": DEBUG_MODE,
        "voice_enabled": ENABLE_VOICE_INPUT and ENABLE_VOICE_OUTPUT,
        "hologram_enabled": HOLOGRAM_ENABLED,
        "ai_model": GEMINI_MODEL,
        "ai_provider": AI_ENGINE_PROVIDER,
        "speech_language": SPEECH_RECOGNITION_LANGUAGE,
        "log_level": LOG_LEVEL,
        "features": FEATURES,
    }


if __name__ == "__main__":
    errors = validate_config()
    if errors:
        print("⚠️  Configuration Warnings:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration validated successfully")
        print("\n📋 Configuration Summary:")
        for key, value in get_config_summary().items():
            print(f"  {key}: {value}")
