"""
Text-to-Speech module for Ultron.
Converts text responses to speech with a deep male voice.
"""

import threading

import pyttsx3


class TextToSpeech:
    """Handles text-to-speech conversion with deep male voice."""

    def __init__(self, config=None):
        self.config = config
        self.engine = pyttsx3.init()
        self.setup_engine()
        self.is_speaking = False

    def setup_engine(self):
        self.engine.setProperty("rate", getattr(self.config, "VOICE_RATE", 120) if self.config else 120)
        self.engine.setProperty("volume", getattr(self.config, "VOICE_VOLUME", 1.0) if self.config else 1.0)

        voices = self.engine.getProperty("voices")
        if voices:
            male_voice_found = False
            for voice in voices:
                voice_name = voice.name.lower()
                if any(keyword in voice_name for keyword in ["male", "david", "george", "henry", "michael"]):
                    self.engine.setProperty("voice", voice.id)
                    male_voice_found = True
                    print(f"[VOICE] Using voice: {voice.name}")
                    break

            if not male_voice_found and len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
                print(f"[VOICE] Using voice: {voices[1].name}")
            elif not male_voice_found:
                self.engine.setProperty("voice", voices[0].id)
                print(f"[VOICE] Using voice: {voices[0].name}")

        try:
            self.engine.setProperty("pitch", getattr(self.config, "VOICE_PITCH", 0.6) if self.config else 0.6)
        except Exception:
            pass

        print("[VOICE] Voice configured: Deep Male Bass")

    def speak(self, text: str) -> bool:
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
        def speak_thread():
            self.speak(text)

        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()

    def stop_speaking(self):
        try:
            self.engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"[ERROR] Error stopping speech: {e}")

    def is_currently_speaking(self) -> bool:
        return self.is_speaking

    def set_rate(self, rate: int):
        self.engine.setProperty("rate", max(50, min(300, rate)))

    def set_volume(self, volume: float):
        self.engine.setProperty("volume", max(0.0, min(1.0, volume)))

    def set_pitch(self, pitch: float):
        try:
            self.engine.setProperty("pitch", max(0.1, min(2.0, pitch)))
        except Exception:
            print("[WARNING] Pitch adjustment not supported by current TTS engine")

    def get_available_voices(self) -> list:
        voices = self.engine.getProperty("voices")
        return [{"id": v.id, "name": v.name, "gender": "Unknown", "index": i} for i, v in enumerate(voices)]

    def list_voices(self):
        voices = self.get_available_voices()
        print("\n[AVAILABLE VOICES]")
        print("=" * 60)
        for voice in voices:
            print(f"  [{voice['index']}] {voice['name']} (ID: {voice['id']})")
        print("=" * 60 + "\n")

    def set_voice_by_index(self, index: int):
        voices = self.engine.getProperty("voices")
        if 0 <= index < len(voices):
            self.engine.setProperty("voice", voices[index].id)
            print(f"[VOICE] Voice changed to: {voices[index].name}")
            return True
        print(f"[ERROR] Voice index {index} not found")
        return False

    def test_voice(self):
        test_message = "Greetings. I am Ultron. Testing voice configuration."
        print(f"\n[TEST] Playing: '{test_message}'\n")
        self.speak(test_message)
