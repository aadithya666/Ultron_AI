"""
Speech Recognition module for Ultron
Converts speech to text using various engines
"""

import speech_recognition as sr
from typing import Tuple, Optional
import threading

class SpeechRecognizer:
    """Handles speech-to-text conversion"""
    
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.recognized_text = ""
        
    def listen(self, timeout: int = None) -> Optional[str]:
        """
        Listen to microphone input and convert to text
        
        Args:
            timeout: Maximum time to listen in seconds
            
        Returns:
            Recognized text or None if not recognized
        """
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen with timeout
                timeout_val = timeout or self.config.SPEECH_RECOGNITION_TIMEOUT
                audio = self.recognizer.listen(source, timeout=timeout_val)
            
            # Try to recognize speech
            text = self.recognizer.recognize_google(audio)
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
        """Listen asynchronously and call callback when done"""
        def listen_thread():
            text = self.listen()
            callback(text)
        
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
    
    def set_listening_state(self, state: bool):
        """Set listening state"""
        self.is_listening = state
    
    def is_currently_listening(self) -> bool:
        """Check if currently listening"""
        return self.is_listening
    
    def get_last_recognized_text(self) -> str:
        """Get last recognized text"""
        return self.recognized_text
