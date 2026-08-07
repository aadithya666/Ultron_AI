"""
Text-to-Speech module for Ultron
Converts text responses to speech with deep male voice
"""

import pyttsx3
import threading
from typing import Optional

class TextToSpeech:
    """Handles text-to-speech conversion with deep male voice"""
    
    def __init__(self, config):
        self.config = config
        self.engine = pyttsx3.init()
        self.setup_engine()
        self.is_speaking = False
        
    def setup_engine(self):
        """Configure TTS engine for deep male voice"""
        # Set speech rate - slower for deeper, more authoritative tone
        self.engine.setProperty('rate', 120)  # Slower than default (200)
        
        # Set volume to maximum
        self.engine.setProperty('volume', 1.0)
        
        # Get available voices and select MALE voice
        voices = self.engine.getProperty('voices')
        
        if voices:
            # Priority: Look for male/David voice (natural deep voice)
            male_voice_found = False
            
            for voice in voices:
                voice_name = voice.name.lower()
                
                # Prefer male voices
                if any(keyword in voice_name for keyword in ['male', 'david', 'george', 'henry', 'michael']):
                    self.engine.setProperty('voice', voice.id)
                    male_voice_found = True
                    print(f"[VOICE] Using voice: {voice.name}")
                    break
            
            # If no male voice found, use the second voice (usually male on most systems)
            if not male_voice_found and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
                print(f"[VOICE] Using voice: {voices[1].name}")
            elif not male_voice_found:
                self.engine.setProperty('voice', voices[0].id)
                print(f"[VOICE] Using voice: {voices[0].name}")
        
        # Lower the pitch for deeper bass voice
        try:
            # Try setting pitch (if supported by engine)
            self.engine.setProperty('pitch', 0.6)  # Lower pitch = deeper voice
        except:
            pass  # Some engines don't support pitch adjustment
        
        print("[VOICE] Voice configured: Deep Male Bass")
    
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
            print(f"[ERROR] Text-to-speech error: {e}")
            self.is_speaking = False
            return False
    
    def speak_async(self, text: str):
        """Speak text asynchronously (non-blocking)"""
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
            print(f"[ERROR] Error stopping speech: {e}")
    
    def is_currently_speaking(self) -> bool:
        """Check if currently speaking"""
        return self.is_speaking
    
    def set_rate(self, rate: int):
        """
        Set speech rate (words per minute)
        Lower = deeper/slower, Higher = faster
        """
        self.engine.setProperty('rate', max(50, min(300, rate)))
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def set_pitch(self, pitch: float):
        """
        Set pitch (0.0 to 2.0)
        Lower = deeper voice, Higher = higher pitched
        """
        try:
            self.engine.setProperty('pitch', max(0.1, min(2.0, pitch)))
        except:
            print("[WARNING] Pitch adjustment not supported by current TTS engine")
    
    def get_available_voices(self) -> list:
        """Get list of available voices with details"""
        voices = self.engine.getProperty('voices')
        voice_list = []
        
        for i, v in enumerate(voices):
            voice_list.append({
                "id": v.id,
                "name": v.name,
                "gender": "Unknown",
                "index": i
            })
        
        return voice_list
    
    def list_voices(self):
        """Print available voices"""
        voices = self.get_available_voices()
        print("\n[AVAILABLE VOICES]")
        print("=" * 60)
        for voice in voices:
            print(f"  [{voice['index']}] {voice['name']} (ID: {voice['id']})")
        print("=" * 60 + "\n")
    
    def set_voice_by_index(self, index: int):
        """Set voice by index from available voices"""
        voices = self.engine.getProperty('voices')
        
        if 0 <= index < len(voices):
            self.engine.setProperty('voice', voices[index].id)
            print(f"[VOICE] Voice changed to: {voices[index].name}")
            return True
        else:
            print(f"[ERROR] Voice index {index} not found")
            return False
    
    def test_voice(self):
        """Test current voice with sample text"""
        test_message = "Greetings. I am Ultron. Testing voice configuration."
        print(f"\n[TEST] Playing: '{test_message}'\n")
        self.speak(test_message)
