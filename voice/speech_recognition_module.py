"""
Speech Recognition module for Ultron.
Converts microphone input into text and supports Indian English.
"""

import threading
from typing import Optional

import speech_recognition as sr


class SpeechRecognizer:
    """Handles speech-to-text conversion."""

    def __init__(self, config=None):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.recognized_text = ""
        self.language = getattr(config, "SPEECH_RECOGNITION_LANGUAGE", "en-IN") if config else "en-IN"

    def listen(self, timeout: int = None) -> Optional[str]:
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                timeout_val = timeout or getattr(self.config, "SPEECH_RECOGNITION_TIMEOUT", 10) if self.config else 10
                audio = self.recognizer.listen(source, timeout=timeout_val)

            text = self.recognizer.recognize_google(audio, language=self.language)
            self.recognized_text = text
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Error during listening: {e}")
            return None

    def listen_async(self, callback):
        def listen_thread():
            text = self.listen()
            callback(text)

        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()

    def set_listening_state(self, state: bool):
        self.is_listening = state

    def is_currently_listening(self) -> bool:
        return self.is_listening

    def get_last_recognized_text(self) -> str:
        return self.recognized_text
