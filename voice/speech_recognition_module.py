"""
Compatibility wrapper for speech recognition module.
Keeps the older import path working while exposing the expected class name.
"""

from .speech_recognition import SpeechRecognizer


class SpeechRecognitionModule(SpeechRecognizer):
    """Backward-compatible alias used by main.py."""
    pass
