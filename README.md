<p align="center">
  <img src="https://raw.githubusercontent.com/sussybocca/BunziBunny/main/icon.png" alt="Bunzi Bunny" width="128">
</p>

<h1 align="center">🐰 Bunzi Bunny</h1>

<p align="center">
  <strong>A genuine desktop companion & utility — cute, intelligent, and completely offline-capable.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

## ✨ What Bunzi Bunny Can Do

| Feature | Description |
|---------|-------------|
| 🎤 **Voice Commands** | Speak naturally — Bunzi understands and responds. Search the web hands-free. |
| 🌐 **Web Search** | Opens your default browser with Google search results — faster than typing. |
| 🧠 **Offline Vocabulary** | 70+ built-in responses for greetings, jokes, facts, and conversation — no internet required. |
| 🖱️ **Drag & Drop Feeding** | Grab the 🥕 carrot and drag it to Bunzi for an instant snack. |
| 🛏️ **Auto Sleep / Hunger** | Bunzi gets tired and hungry — feed or let it sleep automatically. |
| 🎨 **Living Animations** | Walks, runs, waves, listens, eats, sleeps, sniffs, stretches — fully animated. |
| 🔊 **Text-to-Speech** | Speaks responses with selectable voices (pyttsx3). |
| 🔁 **Repeat Mode** | Toggle on/off — repeats what you say or uses intelligent vocabulary. |
| 📊 **System Monitor** | Alerts you when CPU is under heavy load. |
| 🪟 **Windowless Mode** | Roams freely on your desktop — no distracting window borders. |
| ⚙️ **Configurable** | Everything adjustable via `bunzi.config`. |

---

## 🚀 Quick Start

```bash
# Clone or download the repository
cd BunziBunny

# Run the application
python app.py
Note: Missing dependencies will auto-install. For best results, ensure you have a working microphone and internet connection for voice recognition (offline mode still works for conversation).

🎮 Controls
Action	Method
🎤 Microphone	Ctrl + M
🥕 Feed Carrot	Drag 🥕 to bunny or Ctrl + C
🛏️ Sleep	Auto when tired, or Ctrl + B
💬 Chat Panel	Ctrl + H
🔁 Toggle Repeat Mode	From config or menu (windowed mode)
🌐 Toggle Web Search	From config or menu (windowed mode)
👋 Make Bunzi Wave	Click menu or say "wave"
⚙️ Configuration
Bunzi stores its settings in %APPDATA%\BunziBunny\bunzi.config (Windows) or ~/.config/BunziBunny/bunzi.config (Linux/macOS).

Example Configuration
json
{
    "windowless_mode": true,
    "auto_walk": true,
    "auto_run": false,
    "walk_speed": 2,
    "run_speed": 5,
    "interaction_range": 100,
    "email_enabled": false,
    "email_address": "",
    "email_password": "",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "learning_enabled": true,
    "voice_enabled": true,
    "web_search_enabled": true,
    "repeat_mode_enabled": false,
    "mic_shortcut_enabled": true,
    "mic_auto_listen": true,
    "listen_wake_word": "hey bunzi",
    "theme": "dark",
    "bunny_name": "Bunzi",
    "personality": "playful"
}
Configuration Options
Key	Type	Default	Description
windowless_mode	bool	true	Bunzi roams freely on desktop
auto_walk	bool	true	Automatically wanders when idle
auto_run	bool	false	Runs instead of walks
walk_speed	int	2	Movement speed (pixels/frame)
run_speed	int	5	Running speed
voice_enabled	bool	true	Enable/disable text-to-speech
web_search_enabled	bool	true	Allow Google searches
repeat_mode_enabled	bool	false	Repeats your voice input
learning_enabled	bool	true	Bunzi remembers interactions
bunny_name	str	"Bunzi"	Custom name for your companion
personality	str	"playful"	Affects response style
🧠 Offline Vocabulary
Bunzi understands these categories without internet:

Category	Example Triggers
🙋 Greeting	"hello", "hi", "hey", "sup", "howdy"
❤️ Love	"love you", "adore you", "you're the best"
🙏 Thanks	"thank you", "thanks", "appreciate it"
👋 Goodbye	"bye", "goodbye", "see you later"
😂 Joke	"tell me a joke", "make me laugh"
📚 Fun Fact	"tell me something", "did you know"
🌤️ Weather	"how's the weather" (offline response)
🥲 Sad	"I'm sad", "feeling down"
🎨 Animation States
Bunzi has 15+ animation states that trigger based on context:

State	Trigger
🚶 Walking	Moving toward target
🏃 Running	Long distance movement
👋 Waving	User command or interaction
🦻 Listening	Microphone active
🍽️ Eating	Fed a carrot
😴 Sleeping	Energy low or manual sleep
🐇 Hopping	Random idle behavior
👃 Sniffing	Random idle behavior
🧘 Stretching	Random idle behavior
🧼 Grooming	Random idle behavior
🖥️ System Requirements
Python 3.10 or higher

Windows, Linux, or macOS

Microphone (optional — for voice commands)

Internet (optional — only for Google search and voice recognition)

📦 Dependencies (Auto-installed)
pyttsx3 — Text-to-speech

Pillow — Graphics and animation

psutil — System monitoring

speechrecognition — Microphone input

pyaudio — Audio capture

requests / beautifulsoup4 — Web search

🐛 Troubleshooting
Issue	Solution
Microphone not working	Run python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
Voice not speaking	Check voice_enabled: true in config. Run pip install pyttsx3==2.90
PIL emoji errors	Update Pillow: pip install --upgrade Pillow
Bunzi won't move	Set auto_walk: true in config
🤝 Contributing
Bunzi Bunny is open source and welcomes contributions!

Fork the repository

Create a feature branch

Submit a pull request

📄 License
MIT License — feel free to use, modify, and share.

<p align="center"> Made with ❤️ and 🥕 by the Bunzi Bunny team </p><p align="center"> <sub>Bunzi Bunny — Your desktop has never been this alive.</sub> </p> ```
