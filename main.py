import sys
import argparse
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import core components
try:
    from config import config as app_config
    from core.ai_engine import AIEngine
    from core.nlp_processor import NLPProcessor
    from core.memory import Memory
    from voice.text_to_speech import TextToSpeech
    from voice.speech_recognition_module import SpeechRecognitionModule
    from gui.ui_controller import UIController
    from connectivity.api_handler import APIHandler
    from utils.logger import UltronLogger
    from utils.helpers import clean_text, is_valid_email, get_current_time
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


class NEMESIS:
    """
    N.E.M.E.S.I.S. - Neural Execution Engine for Mass Eradication Systems
    Main application controller
    """

    def __init__(self, mode: str = "interactive", enable_voice: bool = True):
        """Initialize N.E.M.E.S.I.S."""
        self.mode = mode
        self.enable_voice = enable_voice
        self.running = False

        # Initialize logger
        self.logger = UltronLogger(level="INFO" if mode != "debug" else "DEBUG")
        self.logger.info("=" * 50)
        self.logger.info("N.E.M.E.S.I.S. - Initializing...")
        self.logger.info("=" * 50)

        # Initialize components
        self.memory = Memory()
        self.ai_engine = AIEngine()
        self.nlp_processor = NLPProcessor()
        self.api_handler = APIHandler(app_config)

        # Initialize voice components if enabled
        if self.enable_voice:
            self.tts = TextToSpeech(app_config)
            self.stt = SpeechRecognitionModule(app_config)
        else:
            self.tts = None
            self.stt = None

        # Initialize UI if mode is not CLI
        self.ui_controller = None
        if mode in ["interactive", "text"]:
            self.ui_controller = UIController(self)

        self.logger.info("[CORE] AI Engine initialized")
        self.logger.info("[NLP] Natural Language Processor initialized")
        self.logger.info("[MEMORY] Memory system initialized")

        if self.enable_voice:
            self.logger.info("[VOICE] Text-to-Speech initialized")
            self.logger.info("[VOICE] Speech Recognition initialized")

        self.logger.info("[CONNECTIVITY] API Handler initialized")

        self.logger.info("=" * 50)
        self.logger.info("N.E.M.E.S.I.S. - Ready for operation")
        self.logger.info("=" * 50)

    def process_user_input(self, user_input: str) -> tuple:
        """
        Process user input and generate response

        Args:
            user_input: User's text or voice input

        Returns:
            Tuple of (response_text, metadata)
        """
        try:
            # Clean input
            user_input = clean_text(user_input)

            # Track query in memory
            self.memory.track_query(user_input)

            # Process through NLP
            processed_input = self.nlp_processor.process(user_input)

            # Generate AI response
            response = self.ai_engine.generate_response(processed_input)

            # Learn from response
            self.memory.learn_response(user_input, response)

            # Return response and metadata
            metadata = {
                "timestamp": get_current_time(),
                "mode": self.mode,
                "input_length": len(user_input),
                "response_length": len(response)
            }

            return response, metadata

        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return f"Error: {str(e)}", {"error": True}

    def listen_for_voice(self) -> str:
        """
        Listen for voice input

        Returns:
            Recognized text or empty string if recognition failed
        """
        if not self.enable_voice or not self.stt:
            self.logger.warning("Voice input not enabled")
            return ""

        try:
            self.logger.info("[VOICE] Listening for voice input...")
            recognized_text = self.stt.listen()

            if recognized_text:
                self.logger.info(f"[VOICE] Recognized: {recognized_text}")
                return recognized_text
            else:
                self.logger.warning("[VOICE] No speech detected")
                return ""

        except Exception as e:
            self.logger.error(f"Voice recognition error: {e}")
            return ""

    def speak(self, text: str):
        """
        Speak text using text-to-speech

        Args:
            text: Text to speak
        """
        if not self.enable_voice or not self.tts:
            return

        try:
            self.logger.info(f"[VOICE] Speaking: {text[:50]}...")
            self.tts.speak(text)
        except Exception as e:
            self.logger.error(f"Text-to-speech error: {e}")

    def run_text_mode(self):
        """Run in text-only mode"""
        self.logger.info("[MODE] Starting Text Mode")
        print("\n" + "=" * 50)
        print("N.E.M.E.S.I.S. - Text Mode")
        print("=" * 50)
        print("Type your commands below (type 'exit' to quit)")
        print("=" * 50 + "\n")

        self.running = True
        while self.running:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                    self.logger.info("User requested exit")
                    self.shutdown()
                    break

                if user_input.lower() == "help":
                    self.show_help()
                    continue

                if user_input.lower() == "memory":
                    stats = self.memory.get_memory_stats()
                    print(f"\nMemory Statistics: {stats}\n")
                    continue

                if user_input.lower() == "status":
                    self.show_status()
                    continue

                response, metadata = self.process_user_input(user_input)
                print(f"\nN.E.M.E.S.I.S.: {response}\n")

                if self.enable_voice:
                    self.speak(response)

            except KeyboardInterrupt:
                print("\n\nShutting down...")
                self.shutdown()
                break
            except Exception as e:
                self.logger.error(f"Error in text mode: {e}")
                print(f"Error: {e}\n")

    def run_voice_mode(self):
        """Run in voice-only mode"""
        if not self.enable_voice:
            self.logger.error("Voice mode requires voice to be enabled")
            self.run_text_mode()
            return

        self.logger.info("[MODE] Starting Voice Mode")
        print("\n" + "=" * 50)
        print("N.E.M.E.S.I.S. - Voice Mode")
        print("=" * 50)
        print("Listening for voice input... (say 'exit' to quit)")
        print("=" * 50 + "\n")

        self.running = True
        while self.running:
            try:
                user_input = self.listen_for_voice()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "stop", "goodbye"]:
                    self.logger.info("User requested exit via voice")
                    self.speak("Shutting down. Goodbye!")
                    self.shutdown()
                    break

                response, metadata = self.process_user_input(user_input)
                print(f"N.E.M.E.S.I.S.: {response}\n")
                self.speak(response)

            except KeyboardInterrupt:
                print("\n\nShutting down...")
                self.shutdown()
                break
            except Exception as e:
                self.logger.error(f"Error in voice mode: {e}")

    def run_interactive_mode(self):
        """Run in interactive mode with GUI"""
        self.logger.info("[MODE] Starting Interactive Mode")

        if self.ui_controller:
            self.ui_controller.run()
        else:
            self.logger.error("UI Controller not initialized")
            self.run_text_mode()

    def show_help(self):
        """Show help menu"""
        help_text = """
 ╔══════════════════════════════════════════════╗
 ║  N.E.M.E.S.I.S. - Help Menu                 ║
 ╚══════════════════════════════════════════════╝

 COMMANDS:
   help     - Show this help menu
   memory   - Display memory statistics
   status   - Show system status
   exit     - Exit N.E.M.E.S.I.S.

 FEATURES:
   ✓ Natural language understanding
   ✓ Voice input/output (if enabled)
   ✓ Conversation memory
   ✓ API connectivity
   ✓ Real-time responses

 TIPS:
   • Type complete sentences for best results
   • Use voice mode for hands-free interaction
   • Memory is automatically saved

 For more information, visit:
 https://github.com/aadithya666/Ultron_AI

 """
        print(help_text)

    def show_status(self):
        """Show system status"""
        stats = self.memory.get_memory_stats()

        status_text = f"""
 ╔══════════════════════════════════════════════╗
 ║  N.E.M.E.S.I.S. - System Status             ║
 ╚══════════════════════════════════════════════╝

 Mode:                    {self.mode}
 Voice Enabled:           {self.enable_voice}
 Running:                 {self.running}

 Memory Statistics:
   Total Interactions:    {stats['total_interactions']}
   Total Sessions:        {stats['total_sessions']}
   User Preferences:      {stats['total_preferences']}
   Learned Responses:     {stats['learned_responses']}
   Session Events:        {stats['session_events']}

 Time:                    {get_current_time()}

 """
        print(status_text)

    def shutdown(self):
        """Shutdown N.E.M.E.S.I.S. gracefully"""
        self.logger.info("N.E.M.E.S.I.S. shutting down...")

        self.memory.end_session()

        if self.api_handler:
            try:
                self.api_handler.close()
            except Exception:
                pass

        self.running = False
        self.logger.info("Shutdown complete")
        print("\n✓ N.E.M.E.S.I.S. has been shut down successfully\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="N.E.M.E.S.I.S. - Neural Execution Engine for Mass Eradication Systems"
    )

    parser.add_argument(
        "--mode",
        choices=["text", "voice", "interactive"],
        default="interactive",
        help="Operation mode (default: interactive)"
    )

    parser.add_argument(
        "--no-voice",
        action="store_true",
        help="Disable voice input/output"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    args = parser.parse_args()

    nemesis = NEMESIS(mode=args.mode, enable_voice=not args.no_voice)

    try:
        if args.mode == "text":
            nemesis.run_text_mode()
        elif args.mode == "voice":
            nemesis.run_voice_mode()
        else:
            nemesis.run_interactive_mode()

    except Exception as e:
        nemesis.logger.critical(f"Critical error: {e}")
        print(f"\n❌ Critical Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
