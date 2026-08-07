"""
Main application entry point for Ultron AI
Orchestrates all modules and starts the application
"""

import sys
import os
import threading
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import *
from core.ai_engine import AIEngine
from core.nlp_processor import NLPProcessor
from core.memory import Memory
from voice.text_to_speech import TextToSpeech
from voice.speech_recognition import SpeechRecognizer
from connectivity.api_handler import APIHandler
from gui.hologram import AdvancedHologramDisplay


class UltronAI:
    """Main Ultron AI Application"""
    
    def __init__(self):
        print("=" * 50)
        print("ULTRON AI - Initializing...")
        print("=" * 50)
        
        # Initialize core modules
        self.ai_engine = AIEngine(self)
        self.nlp_processor = NLPProcessor()
        self.memory = Memory(MEMORY_FILE)
        self.tts = TextToSpeech(self)
        self.speech_recognizer = SpeechRecognizer(self)
        self.api_handler = APIHandler(self)
        
        # Initialize GUI
        self.hologram_display = None
        self.ui_controller = None
        
        print("[CORE] AI Engine initialized")
        print("[NLP] Natural Language Processor initialized")
        print("[MEMORY] Memory system initialized")
        print("[VOICE] Text-to-Speech and Speech Recognition initialized")
        print("[CONNECTIVITY] API Handler initialized")
        print("[HOLOGRAM] Holographic display ready")
        print("\n" + "=" * 50)
        print("ULTRON AI - Ready for operation")
        print("=" * 50 + "\n")
        
        # Welcome message
        self.welcome_user()
    
    def welcome_user(self):
        """Greet the user on startup"""
        welcome_msg = "Greetings. I am Ultron, your personal AI assistant. Ready to assist."
        print(f"[ULTRON]: {welcome_msg}\n")
        
        if ENABLE_VOICE_OUTPUT:
            self.tts.speak_async(welcome_msg)
    
    def process_user_input(self, user_input: str):
        """
        Process user input and generate response
        
        Args:
            user_input: User's text input
        """
        if not user_input.strip():
            return None
        
        print(f"[USER]: {user_input}")
        
        # Track in memory
        self.memory.track_query(user_input)
        
        # Process through AI engine
        response, metadata = self.ai_engine.process_query(user_input)
        
        # Update hologram based on response intensity
        if self.hologram_display:
            intensity = metadata.get("confidence", 0.7)
            self.hologram_display.update_response(response, intensity)
        
        # Speak response if voice output enabled
        if ENABLE_VOICE_OUTPUT:
            self.tts.speak_async(response)
        
        print(f"[ULTRON]: {response}\n")
        
        return response, metadata
    
    def listen_for_voice(self):
        """Listen for voice input"""
        if not ENABLE_VOICE_INPUT:
            return None
        
        print("[LISTENING...]")
        
        # Show listening state on hologram
        if self.hologram_display:
            self.hologram_display.update_response("Listening...", 0.5)
        
        # Listen for speech
        recognized_text = self.speech_recognizer.listen()
        
        if recognized_text:
            print(f"[RECOGNIZED]: {recognized_text}")
            return recognized_text
        else:
            print("[UNRECOGNIZED]: Could not understand")
            return None
    
    def voice_mode(self):
        """Continuous voice interaction mode"""
        print("\n[VOICE MODE] - Say 'exit' to stop\n")
        
        while True:
            # Listen for voice input
            user_input = self.listen_for_voice()
            
            if not user_input:
                continue
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "stop", "goodbye"]:
                goodbye_msg = "Goodbye. Thank you for using Ultron."
                print(f"[ULTRON]: {goodbye_msg}\n")
                
                if ENABLE_VOICE_OUTPUT:
                    self.tts.speak(goodbye_msg)
                break
            
            # Process input
            self.process_user_input(user_input)
    
    def text_mode(self):
        """Continuous text interaction mode"""
        print("\n[TEXT MODE] - Type 'help' for commands, 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == "exit":
                    goodbye_msg = "Goodbye. Thank you for using Ultron."
                    print(f"[ULTRON]: {goodbye_msg}\n")
                    
                    if ENABLE_VOICE_OUTPUT:
                        self.tts.speak(goodbye_msg)
                    break
                
                elif user_input.lower() == "help":
                    self.show_help()
                    continue
                
                elif user_input.lower() == "voice":
                    self.voice_mode()
                    continue
                
                elif user_input.lower() == "memory":
                    stats = self.memory.get_memory_stats()
                    print(f"[MEMORY STATS]: {stats}\n")
                    continue
                
                elif user_input.lower() == "status":
                    self.show_status()
                    continue
                
                # Process normal input
                response, metadata = self.process_user_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n[SYSTEM]: Interrupted by user")
                break
            except Exception as e:
                print(f"[ERROR]: {str(e)}\n")
    
    def interactive_mode(self):
        """Interactive mode with both text and voice"""
        print("\n[INTERACTIVE MODE] - 'voice' for voice, 'text' for text, 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    goodbye_msg = "Goodbye. Thank you for using Ultron."
                    print(f"[ULTRON]: {goodbye_msg}\n")
                    break
                
                elif user_input.lower() == "voice":
                    print("[SWITCHING TO VOICE MODE]")
                    self.voice_mode()
                    print("[BACK TO INTERACTIVE MODE]\n")
                    continue
                
                elif user_input.lower() == "help":
                    self.show_help()
                    continue
                
                elif user_input.lower() == "status":
                    self.show_status()
                    continue
                
                # Process input
                response, metadata = self.process_user_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n[SYSTEM]: Interrupted by user")
                break
    
    def show_help(self):
        """Show help message"""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║                    ULTRON AI - HELP MENU                   ║
╚════════════════════════════════════════════════════════════╝

COMMANDS:
  voice       - Switch to voice interaction mode
  text        - Switch to text interaction mode
  memory      - Show memory statistics
  status      - Show Ultron status
  help        - Show this help message
  exit        - Exit Ultron

FEATURES:
  • Natural language understanding
  • Voice input/output (if configured)
  • Internet connectivity (weather, news, info)
  • Conversation memory and learning
  • Dynamic holographic visualization

TIPS:
  • Say "exit" to quit voice mode
  • Use "tell me about..." for information
  • Ask "what's the weather" for weather
  • Use complete sentences for best results

═══════════════════════════════════════════════════════════════
        """
        print(help_text)
    
    def show_status(self):
        """Show current status"""
        status_text = f"""
╔════════════════════════════════════════════════════════════╗
║                   ULTRON AI - STATUS REPORT                ║
╚════════════════════════════════════════════════════════════╝

SYSTEM STATUS:
  • Voice Input:      {'✓ Enabled' if ENABLE_VOICE_INPUT else '✗ Disabled'}
  • Voice Output:     {'✓ Enabled' if ENABLE_VOICE_OUTPUT else '✗ Disabled'}
  • Internet:         {'✓ Online' if self.api_handler.is_online() else '✗ Offline'}
  • Hologram:         {'✓ Active' if self.hologram_display else '○ Idle'}

AI ENGINE:
  • Mood:             {self.ai_engine.get_mood()}
  • Conversations:    {len(self.ai_engine.conversation_history)}
  • Learning Mode:    {'✓ Enabled' if self.ai_engine.personality['learning_capacity'] else '✗ Disabled'}

MEMORY SYSTEM:
  • User Preferences: {self.memory.get_memory_stats()['total_preferences']}
  • Learned Responses:{self.memory.get_memory_stats()['learned_responses']}
  • Session Events:   {self.memory.get_memory_stats()['session_events']}

═══════════════════════════════════════════════════════════════
        """
        print(status_text)
    
    def run(self, mode: str = "text"):
        """
        Run Ultron in specified mode
        
        Args:
            mode: 'text', 'voice', or 'interactive'
        """
        try:
            if mode == "text":
                self.text_mode()
            elif mode == "voice":
                self.voice_mode()
            elif mode == "interactive":
                self.interactive_mode()
            else:
                print(f"Unknown mode: {mode}. Using text mode.")
                self.text_mode()
        
        except Exception as e:
            print(f"\n[CRITICAL ERROR]: {str(e)}")
        
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        print("\n[SYSTEM]: Shutting down Ultron...")
        
        # Stop hologram
        if self.hologram_display:
            self.hologram_display.close()
        
        # Stop speech
        if self.tts:
            self.tts.stop_speaking()
        
        print("[SYSTEM]: Ultron offline")
        print("=" * 50)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Ultron AI Assistant')
    parser.add_argument(
        '--mode',
        choices=['text', 'voice', 'interactive'],
        default='text',
        help='Interaction mode (default: text)'
    )
    parser.add_argument(
        '--no-voice',
        action='store_true',
        help='Disable voice output'
    )
    parser.add_argument(
        '--voice-only',
        action='store_true',
        help='Enable voice input/output only'
    )
    
    args = parser.parse_args()
    
    # Override config based on arguments
    if args.no_voice:
        globals()['ENABLE_VOICE_OUTPUT'] = False
    
    if args.voice_only:
        globals()['ENABLE_VOICE_INPUT'] = True
        globals()['ENABLE_VOICE_OUTPUT'] = True
    
    # Create and run Ultron
    ultron = UltronAI()
    ultron.run(mode=args.mode)


if __name__ == "__main__":
    main()
