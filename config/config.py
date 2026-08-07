"""
Configuration settings for Ultron AI
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_api_key_here')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_api_key_here')

# AI Settings
AI_MODEL = "gpt-3.5-turbo"  # or your preferred model
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 500

# Voice Settings
VOICE_ENGINE = "pyttsx3"  # or "google" for Google TTS
VOICE_RATE = 150
VOICE_VOLUME = 0.9
SPEECH_RECOGNITION_TIMEOUT = 10

# GUI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
THEME = "dark"  # dark or light
HOLOGRAM_COLOR = "#00FF00"  # Neon green
HOLOGRAM_UPDATE_INTERVAL = 50  # milliseconds

# Hologram Animation Settings
CORE_RADIUS = 100
CORE_PULSE_SPEED = 2
CORE_ROTATION_SPEED = 3
HOLOGRAM_ENABLED = True

# Location Settings (for weather and news)
DEFAULT_LOCATION = "New York"
DEFAULT_COUNTRY_CODE = "US"

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FILE = "logs/ultron.log"

# Memory Settings
MAX_CONVERSATION_HISTORY = 50
MEMORY_FILE = "data/memory.json"

# System Settings
ENABLE_VOICE_INPUT = True
ENABLE_VOICE_OUTPUT = True
ENABLE_INTERNET_FEATURES = True
AUTO_START_LISTENING = False

# Hologram Visualization Settings
ANIMATION_SPEED = "normal"  # fast, normal, slow
CORE_GLOW_EFFECT = True
WAVE_ANIMATION = True
PARTICLE_EFFECTS = True

print("[CONFIG] Ultron AI Configuration Loaded")
