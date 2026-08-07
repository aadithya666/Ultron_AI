"""
Text-to-Speech module for Ultron
Converts text responses to speech
"""

import pyttsx3
import threading
from typing import Optional

class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self, config):
        self.config = config
        self.engine = pyttsx3.init()
        self.setup_engine()
        self.is_speaking = False
        
    def setup_engine(self):
        """Configure TTS engine"""
        # Set speech rate
        self.engine.setProperty('rate', self.config.VOICE_RATE)
        
        # Set volume
        self.engine.setProperty('volume', self.config.VOICE_VOLUME)
        
        # Get available voices and set one
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to use a natural-sounding voice
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            else:
                self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text: str) -> bool:
        """
        Speak the given text
        
        Args:
            text: Text to speak
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text:
                return False
            
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
            return True
            
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            self.is_speaking = False
            return False
    
    def speak_async(self, text: str):
        """Speak text asynchronously"""
        def speak_thread():
            self.speak(text)
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
    
    def stop_speaking(self):
        """Stop current speech"""
        try:
            self.engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"Error stopping speech: {e}")
    
    def is_currently_speaking(self) -> bool:
        """Check if currently speaking"""
        return self.is_speaking
    
    def set_rate(self, rate: int):
        """Set speech rate"""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        voices = self.engine.getProperty('voices')
        return [{"id": v.id, "name": v.name} for v in voices]
