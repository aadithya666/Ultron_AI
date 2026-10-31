"""Compatibility wrapper for the speech recognition interface."""

from voice.speech_recognition import SpeechRecognizer


class SpeechRecognitionModule(SpeechRecognizer):
    """Backward-compatible alias used by main.py."""
    pass
