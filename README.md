```markdown
# 🐰 Bunzi Bunny

<p align="center">
  <img src="https://raw.githubusercontent.com/sussybocca/Bunzi-Bunny/main/icon.png" alt="Bunzi Bunny Icon" width="128">
</p>

<p align="center">
  <strong>Your intelligent, animated desktop companion — helpful, expressive, and always by your side.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform Support">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Animations-20%2B-orange.svg" alt="Animation Count">
  <img src="https://img.shields.io/badge/Bunny%20Types-20-ff69b4.svg" alt="Bunny Varieties">
  <img src="https://img.shields.io/badge/Version-2.0.0-brightgreen.svg" alt="Version">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Project Status">
</p>

---

## 🎯 What Is Bunzi Bunny?

Bunzi Bunny is a **genuine desktop companion application** — not malware, not a prank, not a virus. It's a fully animated, voice-interactive bunny that lives on your desktop, responds to your voice, searches the web, tells jokes, monitors your system, and keeps you company throughout your day.

Unlike other desktop assistants that feel robotic or intrusive, Bunzi was designed from the ground up to be a **friendly presence** on your screen. It wanders around freely, reacts to your voice, expresses emotions through detailed 2D animations, and even gets hungry or tired over time — making it feel truly alive.

Bunzi learns from your interactions and becomes more personalized the more you use it. It remembers your name, your interests, the commands you use most often, and even your search history to provide better responses over time.

<p align="center"><strong>✨ Your desktop has never been this alive. ✨</strong></p>

---

## 📖 Table of Contents

- [What Is Bunzi Bunny?](#-what-is-bunzi-bunny)
- [Core Features](#-core-features)
- [Quick Start](#-quick-start)
- [Controls](#-controls)
- [Configuration](#️-configuration)
- [Bunny Varieties](#-bunny-varieties-20-total)
- [Offline Vocabulary](#-offline-vocabulary)
- [Animation States](#-animation-states-20)
- [System Requirements](#️-system-requirements)
- [Dependencies](#-dependencies-auto-installed)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Core Features

| Category | Feature | Details |
|----------|---------|---------|
| 🎤 **Voice Interaction** | Speak naturally | Bunzi listens via microphone, understands your words, and responds with text-to-speech |
| 🌐 **Intelligent Web Search** | Background search | Silent Google/Wikipedia search with dynamic response generation or full read-out mode with sources |
| 🧠 **Offline Vocabulary** | 70+ responses | Built-in responses across 12 categories — greetings, jokes, facts, and conversation — no internet required |
| 🎨 **20 Bunny Varieties** | Unique characters | Classic, Snow, Chocolate, Midnight, Caramel, Spotted, Striped, Golden, Lavender, Peach, Mint, Coral, Amber, Ruby, Sapphire, Emerald, Onyx, Pearl, Rose, and Sunset — each with distinct fur, eye, and ear colors |
| 🏃 **20+ Animation States** | Full life simulation | Idle, Walking, Running, Waving, Listening, Eating, Sleeping, Hopping, Sniffing, Stretching, Sitting, Grooming, Scared, Curious, Determined, Bashful, Mischievous, Confident, Terrified, Dancing, Basketball |
| 🖱️ **Drag & Drop Feeding** | Interactive feeding | Grab the 🥕 carrot and drag it to Bunzi — visible carrot appears in paw with bite and chew animation |
| 🛏️ **Auto Hunger & Sleep** | Needs simulation | Bunzi gets tired and hungry over time — feed it carrots or let it sleep automatically when energy runs low |
| 🔊 **Text-to-Speech** | Natural voice | Speaks responses aloud with selectable female voice using pyttsx3 engine |
| 🔁 **Repeat Mode** | Voice echo | Toggle on/off — either repeats what you say verbatim or uses intelligent vocabulary responses |
| 📊 **System Monitor** | CPU alerts | Alerts you when CPU usage exceeds 85% — helpful for catching runaway processes |
| 🪟 **Windowless Mode** | Desktop freedom | Roams freely on your desktop with no window borders and transparent background |
| 🎮 **Mini-Game** | Carrot Catch | Built-in reflex game — catch as many carrots as possible in 10 seconds |
| 📧 **Email Support** | SMTP integration | Send emails directly through Bunzi with configurable SMTP settings |
| 📚 **Learning System** | Adaptive memory | Remembers your name, interests, frequently used commands, search history, and interaction patterns |
| ⚙️ **Fully Configurable** | JSON config | Every setting adjustable via `bunzi.config` file stored in AppData |
| 🎯 **Radial Menu** | Quick access | Floating circular menu with one-click access to feeding, sleep, microphone, chat, wave, and more |
| 💬 **Chat Panel** | Text interface | Optional chat window for typing messages when voice isn't available |
| 🎵 **Sound Effects** | Pygame audio | Audio feedback for interactions, powered by pygame mixer |
| 😈 **Evil Mode** | Fun prank mode | Temporary "evil" personality with red flashing screen — harmless fun that reveals itself as a joke |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** or higher installed on your system
- **Git** (optional, for cloning the repository)

### Installation

```bash
# Clone the repository
git clone https://github.com/sussybocca/Bunzi-Bunny.git
cd BunziBunny

# Install all dependencies
pip install pyttsx3 Pillow psutil requests beautifulsoup4 speechrecognition pyaudio pygame

# Run Bunzi Bunny
python app.py
```

Alternative: Direct Download

1. Download the ZIP file from the repository
2. Extract to any folder
3. Open terminal in that folder
4. Run pip install pyttsx3 Pillow psutil requests beautifulsoup4 speechrecognition pyaudio pygame
5. Run python app.py

Note: Missing dependencies will auto-install on first run if you skip the manual installation step. For best results with voice recognition, ensure you have a working microphone. Offline conversation mode works without any internet connection.

---

🎮 Controls

Keyboard Shortcuts

Action Shortcut
🎤 Toggle Microphone Ctrl + M
🥕 Feed Carrot Ctrl + C
🛏️ Put to Sleep Ctrl + B
💬 Toggle Chat Panel Ctrl + H
✅ Confirm Search Ctrl + Y
❌ Cancel Search Ctrl + N

Alternative Methods

Action Method
👋 Make Bunzi Wave Radial menu or voice command "wave"
🌐 Toggle Web Search Config file or menu bar (windowed mode)
🔁 Toggle Repeat Mode Config file or menu bar (windowed mode)
🔊 Toggle Voice Menu bar (windowed mode)
😈 Activate Evil Mode Radial menu or voice "evil mode"
📊 System Status Radial menu
🎮 Play Mini-Game Menu bar (windowed mode)
❌ Quit Application Radial menu, menu bar, or close button

Mouse Interactions

Action Result
🖱️ Single Click on Bunzi Bunzi reacts with surprise and a cute response
🖱️ Double Click on Bunzi Pet Bunzi — triggers happy emotion and purring sound
🖱️ Drag Carrot to Bunzi Feed Bunzi — restores hunger and shows eating animation
🖱️ Drag Menu Button Reposition the radial menu button anywhere on screen

---

⚙️ Configuration

Bunzi stores all settings in a JSON configuration file:

Operating System Config Path
Windows %APPDATA%\BunziBunny\bunzi.config
Linux ~/.config/BunziBunny/bunzi.config
macOS ~/Library/Application Support/BunziBunny/bunzi.config

Complete Configuration Example

```json
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
    "search_response_mode": "dynamic",
    "silent_background_search": true,
    "auto_confirm_search": true,
    "max_search_results": 3,
    "search_timeout": 10,
    "theme": "dark",
    "bunny_name": "Bunzi",
    "personality": "playful",
    "bunny_type": "classic"
}
```

Configuration Reference

Key Type Default Description
windowless_mode bool true When true, Bunzi roams freely on desktop with no window borders. When false, appears in a standard window.
auto_walk bool true Bunzi automatically wanders to random positions when idle.
auto_run bool false Bunzi runs instead of walks when moving to targets.
walk_speed int 2 Movement speed in pixels per frame when walking.
run_speed int 5 Movement speed in pixels per frame when running.
interaction_range int 100 Pixel range for detecting interactions like carrot feeding.
email_enabled bool false Enable Bunzi's email sending capability.
email_address str "" Sender email address for outgoing messages.
email_password str "" App-specific password for email authentication.
smtp_server str "smtp.gmail.com" SMTP server address for email delivery.
smtp_port int 587 SMTP server port number.
learning_enabled bool true Bunzi remembers interactions, names, interests, and commands.
voice_enabled bool true Enable or disable text-to-speech voice output.
web_search_enabled bool true Allow Bunzi to search Google and Wikipedia for information.
repeat_mode_enabled bool false When true, Bunzi repeats your voice input verbatim instead of responding intelligently.
mic_shortcut_enabled bool true Enable Ctrl+M keyboard shortcut for microphone.
mic_auto_listen bool true Microphone starts listening automatically when activated.
listen_wake_word str "hey bunzi" Wake word that triggers listening mode.
search_response_mode str "dynamic" "dynamic" for AI-summarized response or "full" for detailed read-out with source links.
silent_background_search bool true Search Google in the background without opening a browser window.
auto_confirm_search bool true Skip the confirmation prompt and search immediately. Set to false to be asked first.
max_search_results int 3 Maximum number of search results to process per query.
search_timeout int 10 Timeout in seconds for web search requests.
theme str "dark" UI theme — currently supports "dark".
bunny_name str "Bunzi" Custom display name for your bunny companion.
personality str "playful" Affects response style and tone of voice.
bunny_type str "classic" Choose from 20 unique bunny varieties with different colors.

---

🎨 Bunny Varieties (20 Total)

Each variety features completely unique fur colors, eye colors, inner ear colors, paw pad colors, and tail colors. All varieties share the same smooth animation system and expressive range.

# Name Fur Color Eye Color Personality Vibe
1 🟫 Classic Tan/Brown Purple-Blue The original Bunzi — friendly and playful
2 ⬜ Snow White/Silver Light Blue Cool and serene winter spirit
3 🟤 Chocolate Dark Brown Gold Rich, warm, and comforting
4 ⬛ Midnight Dark Navy Fiery Orange Mysterious and intriguing
5 🟠 Caramel Golden Brown Forest Green Sweet, warm, and gentle
6 ⚪ Spotted Cream with spots Deep Brown Playful and energetic
7 🩶 Striped Grey/Silver Emerald Green Unique and stands out
8 🌟 Golden Bright Gold Royal Blue Radiant and confident
9 💜 Lavender Soft Purple Deep Purple Calm, dreamy, and soothing
10 🍑 Peach Warm Peach Sage Green Soft, gentle, and approachable
11 🌿 Mint Cool Mint Rosy Pink Fresh, cool, and refreshing
12 🪸 Coral Warm Coral Ocean Blue Tropical and vibrant
13 🔶 Amber Rich Amber Sky Blue Warm and glowing
14 🔴 Ruby Deep Red Golden Yellow Bold, fiery, and passionate
15 🔵 Sapphire Deep Blue Sunset Orange Cool, collected, and wise
16 🟢 Emerald Forest Green Bright Orange Nature-loving and grounded
17 🖤 Onyx Pure Black Crimson Red Sleek, edgy, and modern
18 🤍 Pearl Soft Pearl Steel Blue Elegant, pure, and refined
19 🌹 Rose Rosy Pink Lavender Purple Romantic, sweet, and caring
20 🌅 Sunset Warm Orange Deep Purple Warm, vibrant, and full of energy

Switching Bunny Types

Change the bunny_type value in your bunzi.config file to any of the following: classic, snow, chocolate, midnight, caramel, spotted, striped, golden, lavender, peach, mint, coral, amber, ruby, sapphire, emerald, onyx, pearl, rose, sunset. Restart Bunzi to see the change.

---

🧠 Offline Vocabulary

Bunzi understands these categories without any internet connection. Responses are randomly selected from a pool to keep conversations fresh.

Category Example Triggers Response Style
🙋 Greeting "hello", "hi", "hey", "sup", "howdy", "greetings", "yo", "bonjour" Warm and welcoming
💬 How Are You "how are you", "how's it going", "how ya doing", "what's up" Positive and energetic
🤔 What Doing "what are you doing", "whatcha doing", "what you up to" Playful and casual
❤️ Love "love you", "i love", "adore you", "you're the best", "you are awesome" Heartwarming and affectionate
🙏 Thanks "thank you", "thanks", "appreciate", "grateful" Humble and appreciative
👋 Goodbye "bye", "goodbye", "see you", "later", "farewell", "catch you later" Warm farewells
😂 Joke "tell me a joke", "make me laugh", "humor", "funny" Silly bunny-themed puns
📚 Fun Fact "tell me something", "did you know", "fact", "trivia" Educational bunny facts
🌤️ Weather "weather", "rain", "sunny", "temperature", "forecast" Playful deflection (desktop-bound)
🥲 Sad "sad", "depressed", "down", "unhappy", "feeling bad" Comforting and supportive
😊 Happy "happy", "joy", "excited", "wonderful", "fantastic" Celebratory and matching energy
💪 Compliment "you look", "nice", "cool", "awesome", "amazing", "great job" Genuine and uplifting

---

🎨 Animation States (20+)

Each animation state features smooth lerp-based transitions, gradient-shaded artwork, and context-appropriate particle effects.

State Visual Appearance Trigger Condition
🚶 Walking Legs swing with knee articulation, arms sway opposite, body bobs Moving toward a target position
🏃 Running Faster leg cycle, wider arm swing, more body lean Moving quickly to a distant target
🧍 Idle Gentle breathing, nose twitching, occasional blinking No movement or interaction
👋 Waving One arm raised swinging side to side User command or menu interaction
🦻 Listening Ears tilted forward, head slightly cocked, paw near ear Microphone active and listening
🍽️ Eating Carrot held in paw, brought to mouth, visible chewing with food particles Fed a carrot by user
😴 Sleeping Lying on a drawn bed, floating Z's, gentle breathing Energy depleted or manual sleep command
🐇 Hopping Both legs bent, body compressed then extended upward Random idle behavior
👃 Sniffing Nose twitching rapidly, head moving side to side slightly Random idle behavior
🧘 Stretching Arms extended upward, body elongated Random idle behavior
🧎 Sitting Legs folded, arms resting on lap Random idle behavior
🧼 Grooming Paw wiping over ears and face Random idle behavior
😰 Scared Body leaned back, ears flat, worried eyes, trembling lines Startled or spooked
🤔 Curious Head tilted, one ear up, inquisitive eyes Investigating something new
💪 Determined Forward lean, furrowed eyebrows, straight mouth line Focused on a task
😳 Bashful Looking down, blushing heavily, small shy smile Embarrassed or complimented
😏 Mischievous Half-lidded eyes, one-sided grin, sly posture Planning something fun
😎 Confident Chest puffed out, sparkle effect, bright eyes with shine Proud or accomplished
😱 Terrified Body cowering, ears fully back, wide eyes with tiny pupils, sweat drops Seriously frightened
💃 Dancing Rhythmic body movement, arms swinging, bouncing ears Celebrating or happy
🏀 Basketball Holding orange basketball, dribbling motion Sports mode activated

---

🖥️ System Requirements

Component Minimum Recommended
Python 3.10 3.11 or higher
Operating System Windows 10 / Linux (Ubuntu 20.04+) / macOS 11+ Windows 11 / Ubuntu 22.04+ / macOS 13+
RAM 512 MB 1 GB or more
Storage 200 MB 500 MB
Microphone Optional (for voice commands) Any working USB or built-in microphone
Internet Optional (for search and voice recognition) Broadband connection
Display 1024x768 1920x1080 or higher

---

📦 Dependencies (Auto-installed)

All dependencies are automatically installed on first run if missing. Manual installation is also supported.

Package Version Purpose Required
pyttsx3 2.90+ Text-to-speech voice synthesis engine Yes
Pillow 9.0+ 2D graphics rendering and animation (PIL fork) Yes
psutil 5.9+ System CPU and memory monitoring Yes
speechrecognition 3.10+ Microphone input capture and Google Speech API Optional
pyaudio 0.2+ Audio hardware interface for microphone Optional
requests 2.28+ HTTP requests for web search and Wikipedia API Optional
beautifulsoup4 4.11+ HTML parsing for Google search results Optional
pygame 2.5+ Audio mixer for sound effects Yes

Install All Dependencies

```bash
pip install pyttsx3 Pillow psutil requests beautifulsoup4 speechrecognition pyaudio pygame
```

---

🐛 Troubleshooting

Issue Cause Solution
Microphone not working Device not recognized or permissions denied Run python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())" to list available devices. Check system permissions.
Voice not speaking TTS engine not configured or disabled Verify voice_enabled: true in bunzi.config. Reinstall pyttsx3: pip install --force-reinstall pyttsx3
Bunzi character invisible Windowless mode rendering issue Set windowless_mode: false in config temporarily to debug, then re-enable. Restart application.
Bunzi won't move Auto-walk disabled or stuck state Verify auto_walk: true in config. Click on Bunzi to reset state.
PIL/Emoji rendering errors Outdated Pillow version Upgrade: pip install --upgrade Pillow
Web search not working No internet or disabled in config Check internet connection. Verify web_search_enabled: true in config.
High CPU usage Animation loop running too fast Reduce walk_speed and run_speed in config. Close other GPU-intensive applications.
Config not saving Permission denied in AppData Run application as administrator once, or manually create the BunziBunny folder in AppData.
Speech recognition timeout Slow internet or poor microphone quality Speak clearly, reduce background noise, or disable web search for offline-only use.
Application won't start Missing Python or dependencies Verify Python 3.10+ is installed: python --version. Run pip install -r requirements.txt if available.

---

📁 Project Structure

```
BunziBunny/
├── app.py                    # Main application entry point
├── bunzi.config              # Default configuration file
├── README.md                 # Project documentation
├── icon.png                  # Application icon
├── requirements.txt          # Python dependencies list
└── AppData/
    └── BunziBunny/
        ├── bunzi.config      # User configuration (created on first run)
        └── learning.pkl      # Learned user data and interaction history
```

Key Components in app.py

Class Purpose
BunziConfig Configuration manager — loads, saves, and manages all settings from JSON
BunziVocabulary Offline response database — 70+ responses across 12 categories with pattern matching
BunziLearner Machine learning system — tracks interactions, remembers names/interests, saves history
BunziVoice Text-to-speech engine — pyttsx3 wrapper with voice selection and chunked long-text support
VoiceInput Speech recognition — microphone capture with Google Speech API integration
IntelligentSearchEngine Web search — Google scraping and Wikipedia API with dynamic response generation
FreeRoamingBunny Character renderer — 2D PIL-based animation with 20+ states, 20 varieties, lerp smoothing
BunziEmail Email sender — SMTP integration for sending messages through Bunzi
RadialMenu UI component — floating circular menu with 8 action buttons
BunziBunny Main controller — orchestrates all systems, UI setup, animation loop, event handling

---

🤝 Contributing

Bunzi Bunny is open source and welcomes contributions of all kinds — bug fixes, new features, documentation improvements, new bunny varieties, and more.

How to Contribute

1. Fork the repository to your GitHub account
2. Clone your fork: git clone https://github.com/YOUR_USERNAME/Bunzi-Bunny.git
3. Create a branch: git checkout -b feature/my-amazing-feature
4. Make your changes and test thoroughly
5. Commit with a clear message: git commit -m 'Add amazing feature: detailed description'
6. Push to your fork: git push origin feature/my-amazing-feature
7. Open a Pull Request against the main repository

Contribution Ideas

· 🎨 Add new bunny varieties with unique color schemes
· 🏃 Create new animation states (jumping rope, reading a book, playing music)
· 🌐 Improve the web search result parsing
· 🗣️ Add support for more languages in voice recognition
· 🎵 Integrate music playback features
· 📊 Add more system monitoring metrics (GPU temp, disk usage, network speed)
· 🎮 Create additional mini-games
· 🖼️ Improve the 2D artwork quality with better shading and details
· 📝 Improve documentation and add tutorials

---

📄 License

This project is licensed under the MIT License — one of the most permissive open source licenses available.

You are free to:

· ✅ Use Bunzi Bunny for personal or commercial purposes
· ✅ Modify the source code to suit your needs
· ✅ Distribute the original or modified version
· ✅ Use it privately without any obligations

Under the condition that:

· 📋 The original license and copyright notice must be included
· ⚠️ The software is provided "as is" without warranty of any kind

See the LICENSE file for the full legal text.

---

🌟 Acknowledgements

Bunzi Bunny was built with love and a passion for creating software that brings joy to people's desktops. Special thanks to:

· The Python community for creating an accessible and powerful programming language
· The Pillow team for making 2D graphics rendering possible in Python
· The pyttsx3 maintainers for offline text-to-speech capabilities
· All contributors who help improve Bunzi Bunny
· You — for using and supporting this project

---

<p align="center">Made with ❤️ and 🥕 by the Bunzi Bunny team</p>
<p align="center"><sub>Bunzi Bunny — Your desktop has never been this alive.</sub></p>
```
