"""
UI Controller for Ultron AI
Manages the graphical user interface and chat interaction
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
from datetime import datetime


class ChatDisplay(tk.Frame):
    """Chat message display area"""
    
    def __init__(self, parent):
        super().__init__(parent, bg="#0a0e27")
        self.config(bg="#0a0e27")
        
        # Chat text widget
        self.chat_text = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            bg="#0a0e27",
            fg="#FF0000",
            font=("Courier", 11),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        self.chat_text.config(state=tk.DISABLED)
        
        # Configure tags for different message types
        self.chat_text.tag_config("user", foreground="#00FFFF", font=("Courier", 11, "bold"))
        self.chat_text.tag_config("ultron", foreground="#FF0000", font=("Courier", 11, "bold"))
        self.chat_text.tag_config("system", foreground="#FFFF00", font=("Courier", 10, "italic"))
        self.chat_text.tag_config("error", foreground="#FF0000", font=("Courier", 10, "bold"))
        self.chat_text.tag_config("timestamp", foreground="#888888", font=("Courier", 9))
    
    def add_message(self, sender: str, message: str, msg_type: str = "normal"):
        """Add a message to the chat display"""
        self.chat_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message based on type
        if sender.lower() == "user":
            self.chat_text.insert(tk.END, f"You: ", "user")
            self.chat_text.insert(tk.END, f"{message}\n", "normal")
        elif sender.lower() == "ultron":
            self.chat_text.insert(tk.END, f"Ultron: ", "ultron")
            self.chat_text.insert(tk.END, f"{message}\n", "ultron")
        elif msg_type == "system":
            self.chat_text.insert(tk.END, f"{message}\n", "system")
        elif msg_type == "error":
            self.chat_text.insert(tk.END, f"ERROR: {message}\n", "error")
        else:
            self.chat_text.insert(tk.END, f"{message}\n", "normal")
        
        self.chat_text.insert(tk.END, "\n")
        
        # Auto scroll to bottom
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def clear(self):
        """Clear chat display"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)


class InputPanel(tk.Frame):
    """Input panel for user messages"""
    
    def __init__(self, parent, on_send_callback=None):
        super().__init__(parent, bg="#1a1f3a")
        self.config(bg="#1a1f3a")
        self.on_send_callback = on_send_callback
        
        # Input label
        label = tk.Label(
            self,
            text="Enter your command:",
            bg="#1a1f3a",
            fg="#FF0000",
            font=("Courier", 10)
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Input frame
        input_frame = tk.Frame(self, bg="#1a1f3a")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            bg="#0a0e27",
            fg="#FF0000",
            font=("Courier", 11),
            insertbackground="#FF0000",
            relief=tk.FLAT,
            bd=2
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self.on_enter_pressed)
        self.input_entry.focus()
        
        # Send button
        self.send_btn = tk.Button(
            input_frame,
            text="SEND",
            bg="#FF0000",
            fg="#000000",
            font=("Courier", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            command=self.send_message
        )
        self.send_btn.pack(side=tk.LEFT)
        
        # Button frame
        btn_frame = tk.Frame(self, bg="#1a1f3a")
        btn_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Voice button
        self.voice_btn = tk.Button(
            btn_frame,
            text="🎤 VOICE",
            bg="#FF6600",
            fg="#FFFFFF",
            font=("Courier", 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5
        )
        self.voice_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Clear button
        self.clear_btn = tk.Button(
            btn_frame,
            text="🗑️ CLEAR",
            bg="#FF3333",
            fg="#FFFFFF",
            font=("Courier", 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Help button
        self.help_btn = tk.Button(
            btn_frame,
            text="❓ HELP",
            bg="#3366FF",
            fg="#FFFFFF",
            font=("Courier", 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5
        )
        self.help_btn.pack(side=tk.LEFT)
    
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        self.send_message()
    
    def send_message(self):
        """Send message"""
        message = self.input_entry.get().strip()
        
        if message and self.on_send_callback:
            self.on_send_callback(message)
            self.input_entry.delete(0, tk.END)
    
    def get_message(self) -> str:
        """Get current message text"""
        return self.input_entry.get().strip()
    
    def clear_input(self):
        """Clear input field"""
        self.input_entry.delete(0, tk.END)
    
    def disable(self):
        """Disable input"""
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
    
    def enable(self):
        """Enable input"""
        self.input_entry.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        self.input_entry.focus()


class StatusBar(tk.Frame):
    """Status bar showing system information"""
    
    def __init__(self, parent):
        super().__init__(parent, bg="#1a1f3a")
        self.config(bg="#1a1f3a", height=30)
        
        # Status labels
        self.status_text = tk.Label(
            self,
            text="Status: Ready",
            bg="#1a1f3a",
            fg="#FF0000",
            font=("Courier", 9),
            anchor="w"
        )
        self.status_text.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        # Info labels
        self.info_text = tk.Label(
            self,
            text="Voice: ON | Memory: Ready",
            bg="#1a1f3a",
            fg="#FF0000",
            font=("Courier", 9),
            anchor="e"
        )
        self.info_text.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def update_status(self, status: str, info: str = ""):
        """Update status bar"""
        self.status_text.config(text=f"Status: {status}")
        if info:
            self.info_text.config(text=info)
    
    def set_listening(self):
        """Show listening status"""
        self.status_text.config(text="Status: Listening...", fg="#FFFF00")
    
    def set_processing(self):
        """Show processing status"""
        self.status_text.config(text="Status: Processing...", fg="#FFFF00")
    
    def set_ready(self):
        """Show ready status"""
        self.status_text.config(text="Status: Ready", fg="#FF0000")
    
    def set_error(self, message: str):
        """Show error status"""
        self.status_text.config(text=f"Status: Error - {message}", fg="#FF0000")


class UIController:
    """Main UI Controller for Ultron"""
    
    def __init__(self, ultron_instance):
        self.ultron = ultron_instance
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("ULTRON - AI Assistant Interface")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0e27")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Create main layout
        self.create_layout()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("[UI] Interface initialized")
    
    def setup_styles(self):
        """Setup UI styles and themes"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark theme colors
        style.configure('Dark.TButton', background="#1a1f3a", foreground="#FF0000")
    
    def create_layout(self):
        """Create main UI layout"""
        # Title bar
        title_frame = tk.Frame(self.root, bg="#000000", height=50)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="⚡ ULTRON AI INTERFACE ⚡",
            bg="#000000",
            fg="#FF0000",
            font=("Courier", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#0a0e27")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Chat display
        self.chat_display = ChatDisplay(content_frame)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input panel
        self.input_panel = InputPanel(content_frame, self.on_message_send)
        self.input_panel.pack(fill=tk.X)
        
        # Bind voice button
        self.input_panel.voice_btn.config(command=self.on_voice_button)
        self.input_panel.clear_btn.config(command=self.on_clear_button)
        self.input_panel.help_btn.config(command=self.on_help_button)
        
        # Status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(fill=tk.X)
        
        # Initial message
        self.chat_display.add_message("system", "Welcome to Ultron AI Interface", "system")
        self.chat_display.add_message("ultron", "Greetings. I am Ultron. How may I assist you?")
    
    def on_message_send(self, message: str):
        """Handle message send"""
        if not message:
            return
        
        # Display user message
        self.chat_display.add_message("user", message)
        
        # Disable input during processing
        self.input_panel.disable()
        self.status_bar.set_processing()
        
        # Process in thread
        thread = threading.Thread(target=self.process_message, args=(message,), daemon=True)
        thread.start()
    
    def process_message(self, message: str):
        """Process user message"""
        try:
            # Get response from Ultron
            response, metadata = self.ultron.process_user_input(message)
            
            # Display response
            self.root.after(0, lambda: self.chat_display.add_message("ultron", response))
            self.root.after(100, lambda: self.status_bar.set_ready())
            self.root.after(100, lambda: self.input_panel.enable())
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.root.after(0, lambda: self.chat_display.add_message("system", error_msg, "error"))
            self.root.after(100, lambda: self.status_bar.set_error(str(e)))
            self.root.after(100, lambda: self.input_panel.enable())
    
    def on_voice_button(self):
        """Handle voice button click"""
        self.input_panel.disable()
        self.status_bar.set_listening()
        self.chat_display.add_message("system", "Listening for voice input...")
        
        # Listen in thread
        thread = threading.Thread(target=self.listen_voice, daemon=True)
        thread.start()
    
    def listen_voice(self):
        """Listen for voice input"""
        try:
            recognized_text = self.ultron.listen_for_voice()
            
            if recognized_text:
                self.root.after(0, lambda: self.chat_display.add_message("system", f"Recognized: {recognized_text}"))
                self.root.after(100, lambda: self.on_message_send(recognized_text))
            else:
                self.root.after(0, lambda: self.chat_display.add_message("system", "Voice not recognized", "error"))
                self.root.after(100, lambda: self.input_panel.enable())
                self.root.after(100, lambda: self.status_bar.set_ready())
        
        except Exception as e:
            error_msg = f"Voice error: {str(e)}"
            self.root.after(0, lambda: self.chat_display.add_message("system", error_msg, "error"))
            self.root.after(100, lambda: self.input_panel.enable())
            self.root.after(100, lambda: self.status_bar.set_error(str(e)))
    
    def on_clear_button(self):
        """Handle clear button click"""
        self.chat_display.clear()
        self.chat_display.add_message("system", "Chat cleared", "system")
    
    def on_help_button(self):
        """Show help dialog"""
        help_text = """
ULTRON AI - QUICK HELP

COMMANDS:
• Type any question or command
• Press ENTER or click SEND
• Click VOICE to use voice input

FEATURES:
✓ Natural language understanding
✓ Voice input/output support
✓ Real-time holographic visualization
✓ Internet connectivity
✓ Conversation memory

TIPS:
• Use complete sentences for best results
• Say "exit" in voice mode to stop
• Check status bar for system info

For more help, type "help" in chat
        """
        messagebox.showinfo("ULTRON - Help", help_text)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Are you sure you want to exit Ultron?"):
            self.ultron.shutdown()
            self.root.destroy()
    
    def run(self):
        """Run the UI"""
        self.root.mainloop()
    
    def display_message(self, sender: str, message: str):
        """Display a message in the chat"""
        self.root.after(0, lambda: self.chat_display.add_message(sender, message))
    
    def show_status(self, status: str):
        """Update status"""
        self.root.after(0, lambda: self.status_bar.update_status(status))
