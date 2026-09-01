# 🤖 N.E.M.E.S.I.S.
## Neural Execution Engine for Mass Eradication Systems

> *A sophisticated AI assistant with deep voice, natural language understanding, and advanced holographic visualization.*

---

## 📋 Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide-step-by-step)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🧠 Advanced AI Engine
- Natural language understanding and processing
- Context-aware responses
- Learning and adaptation capabilities
- Conversation memory system
- Multi-modal interaction support

### 🎤 Voice Integration
- **Deep Male Voice** (Bass-enhanced audio output)
- Real-time speech recognition
- Asynchronous voice processing
- Multiple interaction modes (text, voice, interactive)

### 🌐 Connectivity
- Internet connectivity for real-time data
- Weather information retrieval
- News updates
- API handler for external services
- Async HTTP requests

### 💾 Memory System
- Conversation history tracking
- User preferences storage
- Learned responses database
- Session management
- Persistent data storage

### 🎨 GUI Interface
- Dark futuristic theme (neon red & black)
- Real-time chat interface
- Status monitoring
- Voice input button
- Help and utility functions
- Color-coded messages

### 🌌 Holographic Display
- Dynamic visualization
- Response intensity mapping
- Real-time updates
- Advanced animation effects

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for installation
- **Processor**: Intel i5 or equivalent

### Optional Requirements
- **Microphone**: For voice input
- **Speakers/Headphones**: For voice output
- **Internet Connection**: For API features and weather/news

---

## 📦 Installation Guide (Step-by-Step)

### Step 1: Prerequisites
Before installing N.E.M.E.S.I.S., ensure you have:
- Python 3.8+ installed ([Download Python](https://www.python.org/downloads/))
- Git installed ([Download Git](https://git-scm.com/downloads))
- A text editor or IDE (VS Code, PyCharm, etc.)

**Verify installations:**
```bash
python --version
git --version
```

---

### Step 2: Clone the Repository

```bash
# Navigate to your desired directory
cd ~/projects  # or any directory of your choice

# Clone the repository
git clone https://github.com/aadithya666/Ultron_AI.git

# Enter the project directory
cd Ultron_AI
```

---

### Step 3: Create Virtual Environment

A virtual environment keeps project dependencies isolated from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal line, indicating the virtual environment is active.

---

### Step 4: Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all required packages from requirements.txt
pip install -r requirements.txt
```

This installs:
- OpenAI API client
- Speech Recognition
- Text-to-Speech (pyttsx3)
- NLP libraries (NLTK, TextBlob)
- GUI framework (Tkinter)
- Web libraries (Requests, aiohttp)
- Data processing (NumPy, Pandas)
- And more utilities

**Installation time**: 5-10 minutes depending on internet speed

---

### Step 5: Configure Environment Variables

**Copy the example configuration:**
```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

**Edit the `.env` file** with your credentials:

```bash
# Open .env in your text editor
# On Windows:
notepad .env

# On macOS/Linux:
nano .env
```

**Required configurations:**
```env
# Essential - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_actual_openai_key_here

# Voice settings (customize to preference)
ENABLE_VOICE_INPUT=True
ENABLE_VOICE_OUTPUT=True
VOICE_RATE=120
VOICE_VOLUME=1.0
VOICE_PITCH=0.6

# Optional - For weather and news features
WEATHER_API_KEY=your_weather_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

---

### Step 6: Download NLTK Data

N.E.M.E.S.I.S. needs NLTK data for NLP processing:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
```

---

### Step 7: Test Installation

Verify everything is working:

```bash
# Test Python import
python -c "import tkinter; import pyttsx3; import speech_recognition; print('✓ All dependencies installed!')"

# Run N.E.M.E.S.I.S. in text mode
python main.py --mode text
```

You should see:
```
==================================================
N.E.M.E.S.I.S. - Initializing...
==================================================
[CORE] AI Engine initialized
[NLP] Natural Language Processor initialized
[MEMORY] Memory system initialized
[VOICE] Text-to-Speech and Speech Recognition initialized
[CONNECTIVITY] API Handler initialized
[HOLOGRAM] Holographic display ready

==================================================
N.E.M.E.S.I.S. - Ready for operation
==================================================
```

---

### Step 8: Deactivate Virtual Environment (Optional)

When you're done using N.E.M.E.S.I.S., deactivate the environment:

```bash
# On Windows and macOS/Linux
deactivate
```

---

## 🚀 Usage

### Launch N.E.M.E.S.I.S.

**Text Mode** (default, no microphone needed):
```bash
python main.py --mode text
```

**Voice Mode** (requires microphone):
```bash
python main.py --mode voice
```

**Interactive Mode** (switch between text and voice):
```bash
python main.py --mode interactive
```

**Disable Voice Output** (for quiet testing):
```bash
python main.py --no-voice
```

### In-App Commands

**Text Mode Commands:**
- `help` - Show help menu
- `voice` - Switch to voice mode
- `memory` - Display memory statistics
- `status` - Show system status
- `exit` - Quit application

**Voice Mode:**
- Say "exit", "quit", "stop", or "goodbye" to exit
- Speak naturally for AI to process

---

## 📁 Project Structure

```
Ultron_AI/
├── main.py                 # Entry point - Run this to start N.E.M.E.S.I.S.
│
├── core/
│   ├── ai_engine.py       # AI response generation
│   ├── nlp_processor.py   # Natural language processing
│   └── memory.py          # Conversation memory management
│
├── voice/
│   ├── text_to_speech.py  # Text-to-Speech (Deep male voice)
│   └── speech_recognition.py # Speech-to-Text
│
├── gui/
│   ├── ui_controller.py   # Main GUI interface
│   └── hologram.py        # Holographic visualization
│
├── connectivity/
│   └── api_handler.py     # Internet API calls
│
├── utils/
│   ├── logger.py          # Logging system
│   └── helpers.py         # Utility functions
│
├── config/
│   └── config.py          # Configuration settings
│
├── data/                  # Data storage (auto-created)
│   └── memory.json        # Saved memory data
│
├── logs/                  # Log files (auto-created)
│   └── ultron.log         # Application logs
│
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## ⚙️ Configuration

### Key Configuration Files

#### `config/config.py`
Main configuration file with settings like:
- Voice parameters
- API timeouts
- Memory settings
- UI dimensions

#### `.env` File
Your personal configuration (API keys, preferences). **Never commit this to GitHub!**

---

## 🔌 API Integration

### OpenAI (Required)
1. Get API key from [OpenAI](https://platform.openai.com/api-keys)
2. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Weather API (Optional)
1. Get key from [OpenWeatherMap](https://openweathermap.org/api)
2. Add to `.env`: `WEATHER_API_KEY=...`

### News API (Optional)
1. Get key from [NewsAPI](https://newsapi.org/)
2. Add to `.env`: `NEWS_API_KEY=...`

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named..."
**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: "No microphone detected"
**Solution:**
```bash
# Use text mode instead
python main.py --mode text
```

### Issue: Voice output not working
**Solution:**
```bash
# Disable voice and run in text mode
python main.py --no-voice
```

### Issue: OpenAI API errors
**Solution:**
- Check your API key is correct in `.env`
- Ensure you have API credits
- Check internet connection
- Verify API key has necessary permissions

### Issue: GUI doesn't appear
**Solution:**
```bash
# Check if Tkinter is installed
python -m tkinter

# If error, install Tkinter:
# Windows: Already included with Python
# macOS: brew install python-tk
# Linux: sudo apt-get install python3-tk
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Roadmap

- [ ] Advanced ML model integration
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Cloud sync for memory
- [ ] Enhanced holographic rendering
- [ ] Custom voice training
- [ ] Quantum computing integration

---

## 📞 Support

For issues and questions:
- Open an [Issue](https://github.com/aadithya666/Ultron_AI/issues)
- Check existing documentation
- Contact: aadithya2509@gmail.com

---

## 🌟 Acknowledgments

- OpenAI for GPT models
- NLTK and TextBlob for NLP
- pyttsx3 for voice synthesis
- SpeechRecognition library

---

**Made with ❤️ by Aadithya**

*Last Updated: September 2026*
