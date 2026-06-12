import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import pygame
import psutil
import random
import threading
import time
import os
import json
from datetime import datetime
from pathlib import Path
import math
import sys
import subprocess
from collections import deque
import requests
from bs4 import BeautifulSoup
import webbrowser
import speech_recognition as sr
import re
from urllib.parse import quote
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle

# Initialize pygame mixer
pygame.mixer.init()

# ============================================
# CONFIGURATION SYSTEM
# ============================================

class BunziConfig:
    """Configuration manager with file-based settings"""
    
    CONFIG_FILE = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'BunziBunny' / 'bunzi.config'
    LEARNING_DATA = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'BunziBunny' / 'learning.pkl'
    APPDATA = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'BunziBunny'
    
    DEFAULT_CONFIG = {
        "windowless_mode": True,
        "auto_walk": True,
        "auto_run": False,
        "walk_speed": 2,
        "run_speed": 5,
        "interaction_range": 100,
        "email_enabled": False,
        "email_address": "",
        "email_password": "",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "learning_enabled": True,
        "voice_enabled": True,
        "web_search_enabled": True,
        "repeat_mode_enabled": False,
        "theme": "dark",
        "bunny_name": "Bunzi",
        "personality": "playful"
    }
    
    def __init__(self):
        self.settings = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
                print(f"Loaded config from {self.CONFIG_FILE}")
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            self.save()
            print(f"Created default config at {self.CONFIG_FILE}")
    
    def save(self):
        self.APPDATA.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key):
        return self.settings.get(key, self.DEFAULT_CONFIG.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        self.save()

# ============================================
# EXPANDED VOCABULARY DATABASE
# ============================================

class BunziVocabulary:
    """Massive expanded vocabulary for offline responses"""
    
    RESPONSES = {
        "greeting": [
            "Hi there! So happy to see you!",
            "Hello! How's your day going?",
            "Hey friend! Ready for some fun?",
            "Greetings! I've been waiting for you!",
            "Hop hop! Welcome back!",
            "Well hello there, beautiful human!",
            "Hi hi! You're looking fantastic today!",
            "Heya! What's crackin'?",
            "Howdy partner! Ready to chat?",
            "Bonjour! That's French for hello!"
        ],
        
        "how_are_you": [
            "I'm absolutely fantastic, thanks for asking!",
            "Hopping with joy now that you're here!",
            "Never better! My tail is extra fluffy today!",
            "I'm doing great! Just been bouncing around!",
            "Living the dream, one carrot at a time!",
            "I'm wonderful! Your presence makes my day!"
        ],
        
        "what_doing": [
            "Just hanging out, waiting to chat with you!",
            "Practicing my bunny hops! Wanna see?",
            "Thinking about carrots and coding. A bunny's life!",
            "Watching the pixels on your screen. Fascinating!",
            "Just being cute, as always!"
        ],
        
        "love": [
            "Aww! I love you too, friend!",
            "My heart is doing flips! You're the best!",
            "I'm blushing! Bunnies can blush, you know!",
            "Love you more than carrots! And that's a LOT!",
            "You just made my whole day! ❤️"
        ],
        
        "thanks": [
            "You're very welcome! Happy to help!",
            "No problem at all! That's what I'm here for!",
            "My pleasure! Anytime you need me!",
            "Aww thanks! You're so sweet!",
            "Of course! I love being useful!"
        ],
        
        "bye": [
            "Bye bye! Come back and see me soon!",
            "See you later, alligator! After a while, crocodile!",
            "Take care! I'll be right here when you return!",
            "Farewell, friend! Don't forget about me!",
            "Bye! Hope to see you again real soon!"
        ],
        
        "weather": [
            "I think it's beautiful outside!",
            "Don't ask me, I live on your desktop!",
            "Probably perfect weather for hopping!",
            "I'd need internet to check that for you!"
        ],
        
        "joke": [
            "Why don't bunnies make good poker players? Too many hops!",
            "What do you call a bunny with a dictionary? A well-read rabbit!",
            "Why did the bunny cross the road? To get to the other slide!",
            "What's a bunny's favorite music? Hip hop!",
            "What do you get when you cross a bunny and a computer? A hopping mouse!"
        ],
        
        "compliment": [
            "You're looking especially awesome today!",
            "Your intelligence is as vast as the internet!",
            "You have excellent taste in desktop companions!",
            "I bet you're great at everything you do!",
            "You're the reason I hop out of bed every morning!"
        ],
        
        "confused": [
            "Hmm, I'm not sure I understood that one!",
            "My bunny ears are confused! Can you rephrase?",
            "I didn't quite catch that. Try different words?",
            "Whoops! My brain did a little hop there. Say again?",
            "I'm still learning! Can you explain differently?"
        ],
        
        "happy": [
            "Yay! I love when you're happy!",
            "Your happiness makes me do happy hops!",
            "Seeing you smile makes my day complete!",
            "Wheee! Let's celebrate with virtual carrots!"
        ],
        
        "sad": [
            "Aww, I'm sorry you're feeling down. I'm here for you!",
            "Sending you the biggest bunny hug ever!",
            "Things will get better. I believe in you!",
            "Let me tell you a joke to cheer you up!"
        ],
        
        "fun_fact": [
            "Did you know? Bunnies can jump 3 feet high!",
            "Fun fact: A group of bunnies is called a fluffle!",
            "Rabbits have 28 teeth that never stop growing!",
            "Bunnies can see almost 360 degrees around them!",
            "A happy bunny does a 'binky' - a twist and jump in the air!"
        ]
    }
    
    @classmethod
    def get_response(cls, category):
        if category in cls.RESPONSES:
            return random.choice(cls.RESPONSES[category])
        return random.choice(cls.RESPONSES["confused"])
    
    @classmethod
    def analyze_message(cls, message):
        message = message.lower()
        
        patterns = {
            "greeting": ["hello", "hi", "hey", "greetings", "sup", "howdy", "yo"],
            "how_are_you": ["how are you", "how ya doing", "how's it going", "what's up", "how do you do"],
            "what_doing": ["what are you doing", "whatcha doing", "what's up bunzi", "what you up to"],
            "love": ["love you", "i love", "adore you", "you're the best", "you are awesome"],
            "thanks": ["thank", "thanks", "appreciate", "grateful"],
            "bye": ["bye", "goodbye", "see you", "later", "farewell", "catch you later"],
            "weather": ["weather", "rain", "sunny", "cloudy", "temperature", "forecast"],
            "joke": ["joke", "funny", "laugh", "humor", "tell me a joke"],
            "compliment": ["you look", "nice", "cool", "awesome", "amazing", "great job"],
            "happy": ["happy", "joy", "excited", "wonderful", "fantastic"],
            "sad": ["sad", "depressed", "down", "unhappy", "feeling bad"],
            "fun_fact": ["fact", "tell me something", "did you know", "trivia"]
        }
        
        for category, keywords in patterns.items():
            if any(keyword in message for keyword in keywords):
                return category
        
        return None

# ============================================
# LEARNING SYSTEM
# ============================================

class BunziLearner:
    def __init__(self):
        self.knowledge = {
            "user_name": None,
            "user_interests": [],
            "favorite_topics": [],
            "common_commands": {},
            "interaction_history": [],
            "learned_responses": {}
        }
        self.load()
    
    def load(self):
        if BunziConfig.LEARNING_DATA.exists():
            try:
                with open(BunziConfig.LEARNING_DATA, 'rb') as f:
                    self.knowledge = pickle.load(f)
                print("Learning data loaded!")
            except:
                pass
    
    def save(self):
        try:
            with open(BunziConfig.LEARNING_DATA, 'wb') as f:
                pickle.dump(self.knowledge, f)
        except:
            pass
    
    def learn_from_interaction(self, user_input, bunzi_response):
        timestamp = datetime.now().isoformat()
        self.knowledge["interaction_history"].append({
            "input": user_input,
            "response": bunzi_response,
            "timestamp": timestamp
        })
        
        words = user_input.lower().split()
        for word in words[:3]:
            if len(word) > 3:
                self.knowledge["common_commands"][word] = self.knowledge["common_commands"].get(word, 0) + 1
        
        if len(self.knowledge["interaction_history"]) > 1000:
            self.knowledge["interaction_history"] = self.knowledge["interaction_history"][-500:]
        
        self.save()
    
    def get_common_topics(self):
        topics = {}
        for interaction in self.knowledge["interaction_history"][-50:]:
            words = interaction["input"].lower().split()
            for word in words:
                if len(word) > 4:
                    topics[word] = topics.get(word, 0) + 1
        return sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def remember_user_name(self, name):
        self.knowledge["user_name"] = name
        self.save()
    
    def add_interest(self, topic):
        if topic not in self.knowledge["user_interests"]:
            self.knowledge["user_interests"].append(topic)
            self.save()

# ============================================
# EMAIL SYSTEM
# ============================================

class BunziEmail:
    def __init__(self, config):
        self.enabled = config.get("email_enabled")
        self.email = config.get("email_address")
        self.password = config.get("email_password")
        self.smtp_server = config.get("smtp_server")
        self.smtp_port = config.get("smtp_port")
    
    def send_email(self, to_address, subject, body):
        if not self.enabled or not self.email or not self.password:
            return False, "Email not configured"
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_address
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            return True, "Email sent!"
        except Exception as e:
            return False, f"Error: {e}"

# ============================================
# BUNZI VOICE
# ============================================

class BunziVoice:
    def __init__(self, config):
        self.enabled = config.get("voice_enabled")
        self.speech_lock = threading.Lock()
        self.test_tts()
    
    def test_tts(self):
        try:
            import pyttsx3
            test_engine = pyttsx3.init()
            test_engine.setProperty('rate', 160)
            test_engine.setProperty('volume', 0.85)
            test_engine.stop()
            del test_engine
            print("TTS available!")
        except Exception as e:
            self.enabled = False
            print(f"TTS not available: {e}")
    
    def speak_once(self, text):
        if not self.enabled:
            return
        
        with self.speech_lock:
            engine = None
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty('rate', 160)
                engine.setProperty('volume', 0.85)
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
            finally:
                if engine:
                    try:
                        engine.stop()
                    except:
                        pass
                    del engine
    
    def speak(self, text, callback=None):
        if not self.enabled:
            if callback:
                callback()
            return text
        
        def speak_and_callback():
            self.speak_once(text)
            if callback:
                callback()
        
        threading.Thread(target=speak_and_callback, daemon=True).start()
        return text

# ============================================
# VOICE RECOGNITION
# ============================================

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.listening = False
        self.callback = None
        self.init_microphone()
    
    def init_microphone(self):
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return True
        except:
            return False
    
    def listen_once(self):
        if not self.microphone:
            return None
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
        except:
            return None
    
    def listen_background(self, callback):
        self.callback = callback
        self.listening = True
        
        def listen_loop():
            while self.listening:
                text = self.listen_once()
                if text and self.callback:
                    self.root.after(0, lambda: self.callback(text))
                time.sleep(0.1)
        
        threading.Thread(target=listen_loop, daemon=True).start()
    
    def stop_listening(self):
        self.listening = False
    
    def set_root(self, root):
        self.root = root

# ============================================
# BROWSER MANAGER
# ============================================

class FreeRoamingBunny:
    # Animation states
    STATE_IDLE = "idle"
    STATE_WALKING = "walking"
    STATE_RUNNING = "running"
    STATE_WAVING = "waving"
    STATE_LISTENING = "listening"
    STATE_EATING = "eating"
    STATE_SLEEPING = "sleeping"
    STATE_HOPPING = "hopping"
    STATE_SNIFFING = "sniffing"
    STATE_STRETCHING = "stretching"
    STATE_SITTING = "sitting"
    STATE_GROOMING = "grooming"
    STATE_SCARED = "scared"
    STATE_CURIOUS = "curious"
    
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config
        self.root = None
        self.x = canvas.winfo_screenwidth() // 2
        self.y = canvas.winfo_screenheight() - 150
        self.target_x = self.x
        self.target_y = self.y
        self.state = self.STATE_IDLE
        self.frame = 0
        self.walk_cycle = 0
        self.wave_arm = 0
        self.emotion = "happy"
        self.is_talking = False
        self.is_listening = False
        self.sprite_id = None
        self.current_image = None
        self.breath_offset = 0
        self.breath_direction = 1
        self.tail_wag = 0
        self.nose_twitch = 0
        self.ear_flop = 0
        self.hunger = 50
        self.energy = 100
        self.carrot_count = 0
        
        # Particle system
        self.particles = []
        
        self.screen_width = canvas.winfo_screenwidth()
        self.screen_height = canvas.winfo_screenheight()
        
        self.wander_timer = 0
        self.wander_interval = random.randint(3, 8)
        self.state_timer = 0
        
        self.update_drawing()
    
    def feed_carrot(self):
        """Feed the bunny a carrot"""
        self.carrot_count += 1
        self.hunger = min(100, self.hunger + 20)
        self.state = self.STATE_EATING
        self.is_talking = False
        self.add_particle(self.x, self.y, "heart", 5)
        # Force immediate frame update to show eating
        self.update_drawing()
        if hasattr(self, 'root') and self.root:
            self.root.after(2000, lambda: self._stop_eating())
        return "Yum! Thank you for the carrot!"
    
    def _stop_eating(self):
        """Stop eating animation"""
        self.state = self.STATE_IDLE
        self.update_drawing()
    
    def put_to_bed(self):
        """Put the bunny to sleep in a bed"""
        self.state = self.STATE_SLEEPING
        self.emotion = "sleepy"
        self.is_talking = False
        self.add_particle(self.x, self.y - 20, "sleep", 3)
        self.update_drawing()
        return "Zzz... Good night!"
    
    def wake_up(self):
        """Wake the bunny up"""
        if self.state == self.STATE_SLEEPING:
            self.state = self.STATE_IDLE
            self.emotion = "happy"
            self.add_particle(self.x, self.y, "sparkle", 5)
            self.update_drawing()
            return "Good morning! I'm awake now!"
        return ""
    
    def add_particle(self, x, y, ptype, count=3):
        """Add particle effect at position"""
        for _ in range(count):
            self.particles.append({
                'x': x + random.randint(-30, 30),
                'y': y + random.randint(-30, 30),
                'type': ptype,
                'life': 1.0,
                'vy': random.uniform(-3, -0.5),
                'vx': random.uniform(-2, 2)
            })
    
    def update_particles(self):
        """Update all particles"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1
            p['life'] -= 0.02
            if p['life'] <= 0 or p['y'] > 500:
                self.particles.remove(p)
    
    def draw_particles(self, draw):
        """Draw particles on the image"""
        for p in self.particles:
            char_map = {'heart': '❤️', 'star': '⭐', 'evil': '🦇', 'sparkle': '✨', 'music': '🎵', 'flower': '🌸', 'sleep': '💤'}
            char = char_map.get(p['type'], '💕')
            size = int(20 * p['life'])
            try:
                draw.text((int(p['x']), int(p['y'])), char, fill=f"#{255:02x}{100:02x}{150:02x}")
            except:
                pass
    
    def update_drawing(self):
        img = Image.new('RGBA', (260, 320), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Update particles
        self.update_particles()
        
        # Draw bed if sleeping (NO EMOJI TEXT - FIXED)
        if self.state == self.STATE_SLEEPING:
            bed_x = self.x - 60
            bed_y = self.y + 20
            draw.rectangle([bed_x, bed_y, bed_x + 120, bed_y + 40], fill="#8B4513", outline="#5C3317", width=2)
            draw.rectangle([bed_x + 10, bed_y - 10, bed_x + 110, bed_y], fill="#FFE4B5", outline="#5C3317", width=1)
            # EMOJI TEXT REMOVED - WAS CAUSING PIL ERROR
        
        # Breathing animation
        self.breath_offset += 0.03 * self.breath_direction
        if self.breath_offset > 3:
            self.breath_direction = -1
        elif self.breath_offset < -3:
            self.breath_direction = 1
        
        # Nose twitch
        self.nose_twitch = (self.nose_twitch + 0.2) % (2 * math.pi)
        nose_size = 4 + math.sin(self.nose_twitch) * 1
        
        # Tail wag
        if self.emotion == "happy":
            self.tail_wag = (self.tail_wag + 0.3) % (2 * math.pi)
            tail_angle = math.sin(self.tail_wag) * 15
        else:
            tail_angle = 0
        
        # Listening ear flop
        if self.is_listening:
            self.ear_flop = (self.ear_flop + 0.2) % (2 * math.pi)
            left_ear_angle = math.sin(self.ear_flop) * 12
            right_ear_angle = -math.sin(self.ear_flop) * 8
            head_tilt = math.sin(self.ear_flop * 0.7) * 5
            paw_to_ear = 15 + math.sin(self.ear_flop) * 10
        else:
            left_ear_angle = 0
            right_ear_angle = 0
            head_tilt = 0
            paw_to_ear = 0
        
        # Animation states
        if self.state == self.STATE_WALKING:
            self.walk_cycle = (self.walk_cycle + 0.25) % (2 * math.pi)
            leg_swing = math.sin(self.walk_cycle) * 20
            arm_swing = math.sin(self.walk_cycle) * 15
            body_lean = math.sin(self.walk_cycle) * 4
            ear_bounce = abs(math.sin(self.walk_cycle)) * 5
        elif self.state == self.STATE_RUNNING:
            self.walk_cycle = (self.walk_cycle + 0.6) % (2 * math.pi)
            leg_swing = math.sin(self.walk_cycle) * 30
            arm_swing = math.sin(self.walk_cycle) * 25
            body_lean = math.sin(self.walk_cycle) * 8
            ear_bounce = abs(math.sin(self.walk_cycle)) * 10
        elif self.state == self.STATE_WAVING:
            self.wave_arm = (self.wave_arm + 0.4) % (2 * math.pi)
            arm_swing = math.sin(self.wave_arm) * 50
            leg_swing = 5
            body_lean = 0
            ear_bounce = 0
        elif self.state == self.STATE_HOPPING:
            leg_swing = 25
            arm_swing = 20
            body_lean = math.sin(self.frame * 0.6) * 10
            ear_bounce = 8
        elif self.state == self.STATE_SLEEPING:
            leg_swing = 0
            arm_swing = 0
            body_lean = 5
            ear_bounce = -8
        elif self.state == self.STATE_EATING:
            leg_swing = 0
            arm_swing = 10
            body_lean = 0
            ear_bounce = 0
        else:
            leg_swing = 0
            arm_swing = 0
            body_lean = 0
            ear_bounce = 0
        
        # Apply listening modifications
        if self.is_listening:
            body_lean = body_lean + head_tilt
            arm_swing = arm_swing + (paw_to_ear if self.state != self.STATE_WAVING else 0)
        
        body_y = 125 + self.breath_offset
        head_y = body_y - 60
        
        # Realistic bunny colors
        colors = {
            "happy": ("#D4A574", "#E8C5A0", "#8B5E3C"),
            "evil": ("#8B4513", "#A0522D", "#5C3317"),
            "sad": ("#C4A882", "#D4B896", "#7A5C3A"),
            "surprised": ("#D4A574", "#E8C5A0", "#8B5E3C"),
            "excited": ("#D4A574", "#E8C5A0", "#8B5E3C"),
            "sleepy": ("#C9B99A", "#D9C9AA", "#8B7355")
        }
        body_color, belly_color, outline_color = colors.get(self.emotion, colors["happy"])
        
        # Shadow on ground
        shadow_size = int(50 + abs(body_lean) * 2)
        draw.ellipse([int(self.x - shadow_size + body_lean), int(self.y + 40), 
                      int(self.x + shadow_size + body_lean), int(self.y + 55)], 
                     fill="rgba(0,0,0,30)")
        
        # Realistic fur texture
        for _ in range(30):
            fx = int(random.randint(60, 140) + body_lean)
            fy = int(random.randint(int(body_y + 10), int(body_y + 70)))
            draw.point((fx, fy), fill="#B8966A")
        
        # Back legs
        draw.ellipse([int(55 + leg_swing + body_lean), int(body_y + 65), 
                      int(85 + leg_swing + body_lean), int(body_y + 100)], 
                    fill=body_color, outline=outline_color, width=2)
        draw.ellipse([int(115 - leg_swing + body_lean), int(body_y + 65), 
                      int(145 - leg_swing + body_lean), int(body_y + 100)], 
                    fill=body_color, outline=outline_color, width=2)
        
        # Back feet
        draw.ellipse([int(50 + leg_swing + body_lean), int(body_y + 90), 
                      int(90 + leg_swing + body_lean), int(body_y + 105)], 
                    fill="#E8C5A0", outline=outline_color, width=1)
        draw.ellipse([int(110 - leg_swing + body_lean), int(body_y + 90), 
                      int(150 - leg_swing + body_lean), int(body_y + 105)], 
                    fill="#E8C5A0", outline=outline_color, width=1)
        
        # Body
        draw.ellipse([int(60 + body_lean), int(body_y), 
                      int(140 + body_lean), int(body_y + 80)], 
                    fill=body_color, outline=outline_color, width=2)
        
        # Belly
        draw.ellipse([int(72 + body_lean), int(body_y + 15), 
                      int(128 + body_lean), int(body_y + 70)], 
                    fill=belly_color)
        
        # Head
        draw.ellipse([int(55 + body_lean), int(head_y), 
                      int(145 + body_lean), int(head_y + 78)], 
                    fill=body_color, outline=outline_color, width=2)
        
        # Cheek fluff
        draw.ellipse([int(50 + body_lean), int(head_y + 35), 
                      int(65 + body_lean), int(head_y + 55)], 
                    fill=body_color, outline=None)
        draw.ellipse([int(135 + body_lean), int(head_y + 35), 
                      int(150 + body_lean), int(head_y + 55)], 
                    fill=body_color, outline=None)
        
        # Ears
        ear_left_x = 58 + left_ear_angle + body_lean
        ear_right_x = 142 - right_ear_angle + body_lean
        
        # Left ear
        draw.ellipse([int(ear_left_x), int(head_y - 55 + ear_bounce), 
                      int(ear_left_x + 25), int(head_y + 5)], 
                    fill=body_color, outline=outline_color, width=2)
        draw.ellipse([int(ear_left_x + 3), int(head_y - 48 + ear_bounce), 
                      int(ear_left_x + 22), int(head_y + 2)], 
                    fill="#FFB7C5")
        
        # Right ear
        draw.ellipse([int(ear_right_x - 25), int(head_y - 58 + ear_bounce), 
                      int(ear_right_x), int(head_y + 2)], 
                    fill=body_color, outline=outline_color, width=2)
        draw.ellipse([int(ear_right_x - 22), int(head_y - 51 + ear_bounce), 
                      int(ear_right_x - 3), int(head_y - 1)], 
                    fill="#FFB7C5")
        
        # Blush
        if self.emotion not in ["evil", "sad"]:
            draw.ellipse([int(65 + body_lean), int(head_y + 35), 
                          int(80 + body_lean), int(head_y + 50)], 
                        fill="#FF9999", outline=None)
            draw.ellipse([int(120 + body_lean), int(head_y + 35), 
                          int(135 + body_lean), int(head_y + 50)], 
                        fill="#FF9999", outline=None)
        
        # Eyes
        if self.emotion == "happy":
            draw.arc([int(73 + body_lean), int(head_y + 20), 
                      int(93 + body_lean), int(head_y + 42)], 
                     0, 180, fill="#333333", width=3)
            draw.arc([int(107 + body_lean), int(head_y + 20), 
                      int(127 + body_lean), int(head_y + 42)], 
                     0, 180, fill="#333333", width=3)
        elif self.emotion == "evil":
            draw.ellipse([int(73 + body_lean), int(head_y + 22), 
                          int(93 + body_lean), int(head_y + 38)], 
                        fill="#FF0000")
            draw.ellipse([int(107 + body_lean), int(head_y + 22), 
                          int(127 + body_lean), int(head_y + 38)], 
                        fill="#FF0000")
            draw.ellipse([int(80 + body_lean), int(head_y + 25), 
                          int(86 + body_lean), int(head_y + 35)], 
                        fill="black")
            draw.ellipse([int(114 + body_lean), int(head_y + 25), 
                          int(120 + body_lean), int(head_y + 35)], 
                        fill="black")
        elif self.emotion == "sleepy":
            draw.arc([int(73 + body_lean), int(head_y + 26), 
                      int(93 + body_lean), int(head_y + 42)], 
                     0, 180, fill="#333333", width=2)
            draw.arc([int(107 + body_lean), int(head_y + 26), 
                      int(127 + body_lean), int(head_y + 42)], 
                     0, 180, fill="#333333", width=2)
        elif self.emotion == "surprised":
            draw.ellipse([int(71 + body_lean), int(head_y + 18), 
                          int(95 + body_lean), int(head_y + 44)], 
                        fill="white")
            draw.ellipse([int(105 + body_lean), int(head_y + 18), 
                          int(129 + body_lean), int(head_y + 44)], 
                        fill="white")
            draw.ellipse([int(79 + body_lean), int(head_y + 26), 
                          int(87 + body_lean), int(head_y + 36)], 
                        fill="#333333")
            draw.ellipse([int(113 + body_lean), int(head_y + 26), 
                          int(121 + body_lean), int(head_y + 36)], 
                        fill="#333333")
        else:
            draw.ellipse([int(71 + body_lean), int(head_y + 18), 
                          int(95 + body_lean), int(head_y + 44)], 
                        fill="white")
            draw.ellipse([int(105 + body_lean), int(head_y + 18), 
                          int(129 + body_lean), int(head_y + 44)], 
                        fill="white")
            draw.ellipse([int(78 + body_lean), int(head_y + 25), 
                          int(88 + body_lean), int(head_y + 37)], 
                        fill="#333333")
            draw.ellipse([int(112 + body_lean), int(head_y + 25), 
                          int(122 + body_lean), int(head_y + 37)], 
                        fill="#333333")
            draw.ellipse([int(80 + body_lean), int(head_y + 23), 
                          int(83 + body_lean), int(head_y + 27)], 
                        fill="white")
            draw.ellipse([int(114 + body_lean), int(head_y + 23), 
                          int(117 + body_lean), int(head_y + 27)], 
                        fill="white")
        
        # Nose
        nose_x = 100 + body_lean
        nose_y = head_y + 44
        draw.ellipse([int(nose_x - nose_size), int(nose_y - 3), 
                      int(nose_x + nose_size), int(nose_y + 3)], 
                    fill="#FF69B4")
        
        # ============================================
        # MOUTH WITH TALKING ANIMATION
        # ============================================
        if self.is_talking:
            # 4-frame talking animation
            mouth_frame = (self.frame // 4) % 4
            if mouth_frame == 0:
                # Mouth open wide
                draw.ellipse([int(92 + body_lean), int(head_y + 46), 
                              int(108 + body_lean), int(head_y + 62)], 
                            fill="#FF69B4")
            elif mouth_frame == 1:
                # Mouth slightly open
                draw.arc([int(91 + body_lean), int(head_y + 46), 
                          int(109 + body_lean), int(head_y + 62)], 
                         0, 180, fill="#FF69B4", width=3)
            elif mouth_frame == 2:
                # Mouth closed smile
                draw.arc([int(92 + body_lean), int(head_y + 48), 
                          int(108 + body_lean), int(head_y + 60)], 
                         0, 180, fill="#FF69B4", width=2)
            else:
                # Mouth medium open
                draw.ellipse([int(93 + body_lean), int(head_y + 48), 
                              int(107 + body_lean), int(head_y + 60)], 
                            fill="#FF69B4")
        elif self.state == self.STATE_EATING:
            # Eating animation - chewing motion (NO EMOJI TEXT - FIXED)
            chew_frame = (self.frame // 3) % 3
            if chew_frame == 0:
                # Mouth open with carrot (no emoji text - just mouth shape)
                draw.ellipse([int(92 + body_lean), int(head_y + 46), 
                              int(108 + body_lean), int(head_y + 62)], 
                            fill="#FF69B4")
            elif chew_frame == 1:
                # Mouth closed chewing
                draw.arc([int(92 + body_lean), int(head_y + 48), 
                          int(108 + body_lean), int(head_y + 60)], 
                         0, 180, fill="#FF69B4", width=3)
            else:
                # Mouth open wide chewing
                draw.ellipse([int(91 + body_lean), int(head_y + 45), 
                              int(109 + body_lean), int(head_y + 63)], 
                            fill="#FF69B4")
        elif self.emotion == "happy":
            draw.arc([int(92 + body_lean), int(head_y + 46), 
                      int(108 + body_lean), int(head_y + 62)], 
                     0, 180, fill="#FF69B4", width=2)
        elif self.emotion == "evil":
            draw.arc([int(88 + body_lean), int(head_y + 44), 
                      int(112 + body_lean), int(head_y + 66)], 
                     0, 180, fill="#CC0000", width=3)
            draw.polygon([int(94 + body_lean), int(head_y + 52), 
                          int(98 + body_lean), int(head_y + 62), 
                          int(102 + body_lean), int(head_y + 52)], fill="white")
        elif self.emotion == "sad":
            draw.arc([int(92 + body_lean), int(head_y + 48), 
                      int(108 + body_lean), int(head_y + 62)], 
                     180, 360, fill="#6B7B8D", width=2)
        else:
            draw.arc([int(92 + body_lean), int(head_y + 46), 
                      int(108 + body_lean), int(head_y + 62)], 
                     0, 180, fill="#FF69B4", width=2)
        
        # Whiskers
        whisker_wave = math.sin(self.frame * 0.25) * 2
        draw.line([int(35 + body_lean), int(head_y + 40), 
                   int(70 + body_lean), int(head_y + 46 + whisker_wave)], 
                  fill="#CCCCCC", width=1)
        draw.line([int(35 + body_lean), int(head_y + 50), 
                   int(70 + body_lean), int(head_y + 52 - whisker_wave)], 
                  fill="#CCCCCC", width=1)
        draw.line([int(130 + body_lean), int(head_y + 46 + whisker_wave), 
                   int(165 + body_lean), int(head_y + 40)], 
                  fill="#CCCCCC", width=1)
        draw.line([int(130 + body_lean), int(head_y + 52 - whisker_wave), 
                   int(165 + body_lean), int(head_y + 50)], 
                  fill="#CCCCCC", width=1)
        
        # Arms
        if self.is_listening and self.state != self.STATE_WAVING:
            left_arm_angle = arm_swing
            right_arm_angle = arm_swing + paw_to_ear
        else:
            left_arm_angle = arm_swing
            right_arm_angle = arm_swing
        
        # Left arm
        draw.line([int(65 + body_lean), int(body_y + 22), 
                   int(30 + left_arm_angle + body_lean), int(body_y + 60)], 
                  fill=body_color, width=14)
        # Right arm  
        draw.line([int(135 + body_lean), int(body_y + 22), 
                   int(170 - right_arm_angle + body_lean), int(body_y + 60)], 
                  fill=body_color, width=14)
        
        # Paws
        draw.ellipse([int(25 + left_arm_angle + body_lean), int(body_y + 55), 
                      int(40 + left_arm_angle + body_lean), int(body_y + 70)], 
                    fill="#E8C5A0")
        draw.ellipse([int(160 - right_arm_angle + body_lean), int(body_y + 55), 
                      int(175 - right_arm_angle + body_lean), int(body_y + 70)], 
                    fill="#E8C5A0")
        
        # Tail
        tail_x = 148 + body_lean
        tail_y = body_y + 55
        draw.ellipse([int(tail_x - 12 + tail_angle), int(tail_y - 8), 
                      int(tail_x + 8 + tail_angle), int(tail_y + 12)], 
                    fill="white", outline="#D4A574", width=1)
        
        # Sleep Z's when sleeping
        if self.state == self.STATE_SLEEPING:
            z_frame = (self.frame // 20) % 3
            if z_frame == 0:
                draw.text((int(160 + body_lean), int(head_y - 30)), "z", 
                         fill="#88CCFF", font=("Arial", 12))
            elif z_frame == 1:
                draw.text((int(165 + body_lean), int(head_y - 40)), "z", 
                         fill="#88CCFF", font=("Arial", 14))
            else:
                draw.text((int(170 + body_lean), int(head_y - 50)), "Z", 
                         fill="#88CCFF", font=("Arial", 16))
        
        # Evil accessories
        if self.emotion == "evil":
            draw.polygon([int(65 + body_lean), int(head_y - 45), 
                          int(72 + body_lean), int(head_y - 75), 
                          int(79 + body_lean), int(head_y - 45)], fill="#CC0000")
            draw.polygon([int(121 + body_lean), int(head_y - 45), 
                          int(128 + body_lean), int(head_y - 78), 
                          int(135 + body_lean), int(head_y - 45)], fill="#CC0000")
            draw.line([int(68 + body_lean), int(head_y + 18), 
                       int(95 + body_lean), int(head_y + 30)], 
                      fill="black", width=2)
            draw.line([int(105 + body_lean), int(head_y + 30), 
                       int(132 + body_lean), int(head_y + 18)], 
                      fill="black", width=2)
        
        # Draw particles on top
        self.draw_particles(draw)
        
        self.current_image = ImageTk.PhotoImage(img)
        
        if self.sprite_id:
            self.canvas.delete(self.sprite_id)
        self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.current_image, anchor='center')
    
    def update_movement(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # State timer for automatic state changes
        self.state_timer += 1
        
        # Auto change states when idle
        if self.state == self.STATE_IDLE and self.state_timer > random.randint(180, 300):
            self.state_timer = 0
            random_state = random.choice([self.STATE_SNIFFING, self.STATE_STRETCHING, 
                                          self.STATE_GROOMING, self.STATE_SITTING])
            self.state = random_state
            if hasattr(self, 'root') and self.root:
                self.root.after(2000, lambda: setattr(self, 'state', self.STATE_IDLE))
        
        if abs(dx) > 5:
            speed = self.config.get("run_speed") if self.state == self.STATE_RUNNING else self.config.get("walk_speed")
            self.x += max(-speed, min(speed, dx * 0.1))
            self.state = self.STATE_RUNNING if abs(dx) > 30 else self.STATE_WALKING
        else:
            if self.state in [self.STATE_WALKING, self.STATE_RUNNING]:
                self.state = self.STATE_IDLE
        
        self.x = max(60, min(self.x, self.screen_width - 60))
        self.y = max(60, min(self.y, self.screen_height - 130))
        
        if self.config.get("auto_walk") and self.state == self.STATE_IDLE:
            self.wander_timer += 1
            if self.wander_timer > self.wander_interval * 60:
                self.wander_timer = 0
                self.wander_interval = random.randint(5, 12)
                new_x = random.randint(150, self.screen_width - 200)
                new_y = random.randint(100, self.screen_height - 250)
                self.move_to(new_x, new_y)
    
    def move_to(self, x, y):
        self.target_x = max(60, min(x, self.screen_width - 60))
        self.target_y = max(60, min(y, self.screen_height - 130))
    
    def set_emotion(self, emotion):
        self.emotion = emotion
        self.update_drawing()
    
    def set_talking(self, talking):
        self.is_talking = talking
        # Force immediate frame update to show mouth moving
        self.update_drawing()
    
    def set_listening(self, listening):
        self.is_listening = listening
        if listening:
            self.state = self.STATE_LISTENING
        elif self.state == self.STATE_LISTENING:
            self.state = self.STATE_IDLE
        self.update_drawing()
    
    def wave(self):
        self.state = self.STATE_WAVING
        if hasattr(self, 'root') and self.root:
            self.root.after(1500, lambda: setattr(self, 'state', self.STATE_IDLE))
        self.update_drawing()
    
    def hop(self):
        self.state = self.STATE_HOPPING
        if hasattr(self, 'root') and self.root:
            self.root.after(800, lambda: setattr(self, 'state', self.STATE_IDLE))
        self.update_drawing()
    
    def sleep(self):
        self.state = self.STATE_SLEEPING
        self.emotion = "sleepy"
        self.update_drawing()
    
    def wake(self):
        if self.state == self.STATE_SLEEPING:
            self.state = self.STATE_IDLE
            self.emotion = "happy"
            self.update_drawing()
    
    def animate(self):
        self.frame += 1
        self.update_drawing()
        self.update_movement()
        return self.frame

# ============================================
# BROWSER MANAGER
# ============================================

class BrowserManager:
    def __init__(self, config):
        self.enabled = config.get("web_search_enabled")
        self.search_engine = "https://www.google.com/search?q="
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def search_web(self, query):
        if not self.enabled:
            return None
        encoded_query = quote(query)
        url = self.search_engine + encoded_query
        webbrowser.open(url)
        return url
    

# ============================================
# RADIAL MENU SYSTEM
# ============================================

class RadialMenu:
    """A beautiful circular floating menu that follows the bunny"""
    
    def __init__(self, parent, bunny, controller):
        self.parent = parent
        self.bunny = bunny
        self.controller = controller
        self.is_open = False
        self.menu_items = []
        self.circle_btn = None
        self.menu_frame = None
        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.click_timer = None
        
        self.create_circle_button()
    
    def create_circle_button(self):
        """Create the main circular toggle button (draggable)"""
        self.circle_btn = tk.Canvas(self.parent, width=50, height=50, 
                                     bg='#1a1a2e', highlightthickness=0)
        # Outer glow ring
        self.circle_btn.create_oval(2, 2, 48, 48, fill='#2d2d44', outline='#ff69b4', width=2)
        # Inner circle
        self.circle_btn.create_oval(6, 6, 44, 44, fill='#e94560', outline='')
        # Icon
        self.circle_btn.create_text(25, 25, text="🍽️", font=("Segoe UI Emoji", 20))
        
        # Position in top-right corner initially
        self.circle_btn.place(x=self.parent.winfo_screenwidth() - 80, y=50)
        
        # Bind mouse events
        self.circle_btn.bind('<ButtonPress-1>', self.on_press)
        self.circle_btn.bind('<B1-Motion>', self.on_drag)
        self.circle_btn.bind('<ButtonRelease-1>', self.on_release)
    
    def on_press(self, event):
        """Handle mouse press - record start position"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.drag_x = event.x
        self.drag_y = event.y
        self.dragging = False
        
        # Cancel any pending click timer
        if self.click_timer:
            self.parent.after_cancel(self.click_timer)
            self.click_timer = None
    
    def on_drag(self, event):
        """Handle mouse drag - move the button"""
        # If moved more than 5 pixels, it's a drag
        if abs(event.x - self.drag_start_x) > 5 or abs(event.y - self.drag_start_y) > 5:
            self.dragging = True
        
        if self.dragging:
            x = self.circle_btn.winfo_x() + event.x - self.drag_x
            y = self.circle_btn.winfo_y() + event.y - self.drag_y
            self.circle_btn.place(x=x, y=y)
            # Also move the menu frame if open
            if self.is_open and self.menu_frame:
                self.menu_frame.place(x=x - 40, y=y - 110)
    
    def on_release(self, event):
        """Handle mouse release - if not dragged, toggle menu"""
        if not self.dragging:
            # It was a click, not a drag - toggle menu after a tiny delay
            self.click_timer = self.parent.after(50, self.toggle_menu)
        self.dragging = False
    
    def toggle_menu(self):
        """Open or close the radial menu"""
        if self.is_open:
            self.close_menu()
        else:
            self.open_menu()
    
    def open_menu(self):
        """Open the circular menu with buttons radiating outward"""
        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_items.clear()
        
        btn_x = self.circle_btn.winfo_x()
        btn_y = self.circle_btn.winfo_y()
        
        self.menu_frame = tk.Frame(self.parent, bg='#1a1a2e', bd=0, highlightthickness=0)
        self.menu_frame.place(x=btn_x - 40, y=btn_y - 110)
        
        # Menu items with emojis, text, and colors
        items = [
            ("🥕", " Feed", "#00cc44", self.give_carrot),
            ("🛏️", " Sleep", "#4466cc", self.put_to_bed),
            ("🎤", " Mic", "#e94560", self.toggle_mic),
            ("💬", " Chat", "#ffaa00", self.toggle_chat),
            ("👋", " Wave", "#aa66ff", self.wave),
            ("😈", " Evil", "#ff4400", self.evil_mode),
            ("📊", " Stats", "#33cccc", self.show_stats),
            ("❌", " Exit", "#ff3333", self.quit_app),
        ]
        
        # Create buttons in a circular arc
        radius = 85
        start_angle = -90
        angle_step = 360 / len(items)
        
        for i, (emoji, text, color, action) in enumerate(items):
            angle = math.radians(start_angle + i * angle_step)
            x_offset = radius * math.cos(angle)
            y_offset = radius * math.sin(angle)
            
            # Create button with proper command binding
            btn = tk.Button(self.menu_frame, text=f"{emoji}{text}", font=("Segoe UI", 9, "bold"),
                           bg=color, fg='white', bd=0, padx=10, pady=6,
                           command=lambda a=action: self.select_action(a),
                           cursor="hand2", relief=tk.RAISED)
            btn.place(x=x_offset, y=y_offset, anchor='center')
            self.menu_items.append(btn)
        
        self.is_open = True
    
    def close_menu(self):
        """Close the menu"""
        for item in self.menu_items:
            item.destroy()
        self.menu_items.clear()
        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None
        self.is_open = False
    
    def select_action(self, action):
        """Handle menu action selection"""
        self.close_menu()
        action()
    
    def give_carrot(self):
        """Feed the bunny"""
        if hasattr(self.controller, 'give_carrot'):
            self.controller.give_carrot()
            self.show_feedback("🥕 Yum! Thanks for the carrot!", "#00cc44")
    
    def put_to_bed(self):
        """Put bunny to sleep"""
        if hasattr(self.controller, 'put_bunny_to_bed'):
            self.controller.put_bunny_to_bed()
            self.show_feedback("🛏️ Good night! Zzz...", "#4466cc")
    
    def toggle_mic(self):
        """Toggle microphone"""
        if hasattr(self.controller, 'toggle_microphone'):
            self.controller.toggle_microphone()
            self.show_feedback("🎤 Microphone toggled", "#e94560")
    
    def toggle_chat(self):
        """Toggle chat panel"""
        if hasattr(self.controller, 'toggle_chat'):
            self.controller.toggle_chat()
            self.show_feedback("💬 Chat toggled", "#ffaa00")
    
    def wave(self):
        """Make bunny wave"""
        if hasattr(self.bunny, 'wave'):
            self.bunny.wave()
            self.show_feedback("👋 Hello there!", "#aa66ff")
    
    def evil_mode(self):
        """Activate evil mode"""
        if hasattr(self.controller, 'activate_evil_mode'):
            self.controller.activate_evil_mode()
            self.show_feedback("😈 EVIL MODE!", "#ff4400")
    
    def show_stats(self):
        """Show bunny stats"""
        if hasattr(self.bunny, 'hunger') and hasattr(self.bunny, 'energy'):
            stats = f"Hunger: {self.bunny.hunger}%\nEnergy: {self.bunny.energy}%"
            self.show_feedback(stats, "#33cccc", 3000)
    
    def quit_app(self):
        """Quit application"""
        if hasattr(self.controller, 'quit_app'):
            self.controller.quit_app()
    
    def show_feedback(self, message, color, duration=2000):
        """Show temporary feedback near the bunny"""
        feedback = tk.Label(self.parent, text=message, font=("Segoe UI", 10, "bold"),
                           bg=color, fg='white', bd=2, relief=tk.RAISED, padx=12, pady=6)
        feedback.place(x=self.bunny.x + 20, y=self.bunny.y - 80)
        
        def fade_out():
            try:
                feedback.destroy()
            except:
                pass
        
        self.parent.after(duration, fade_out)
# ============================================
# BUNZI BUNNY MAIN CLASS
# ============================================

# ============================================
# BUNZI BUNNY MAIN CLASS
# ============================================

# ============================================
# BUNZI BUNNY MAIN CLASS
# ============================================

class BunziBunny:
    def __init__(self):
        self.config = BunziConfig()
        self.vocab = BunziVocabulary()
        self.learner = BunziLearner()
        self.email = BunziEmail(self.config)
        
        self.root = tk.Tk()
        self.root.title("🐰 Bunzi Bunny 🐰")
        self.root.overrideredirect(self.config.get("windowless_mode"))
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#1a1a2e')
        self.root.attributes('-transparentcolor', '#1a1a2e')
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        if not self.config.get("windowless_mode"):
            self.window_x = self.screen_width - 450
            self.window_y = self.screen_height - 580
            self.root.geometry(f"420x550+{self.window_x}+{self.window_y}")
        
        self.is_running = True
        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
        self.evil_mode_active = False
        self.voice_listening = False
        self.repeat_mode_enabled = self.config.get("repeat_mode_enabled")
        
        self.voice = BunziVoice(self.config)
        self.browser = BrowserManager(self.config)
        self.microphone = VoiceInput()
        self.microphone.set_root(self.root)
        
        self.setup_ui()
        self.animate_bunny()
        self.start_background_tasks()
        
        # Keyboard shortcut for microphone (Ctrl+M)
        if self.config.get("mic_shortcut_enabled"):
            self.root.bind('<Control-m>', lambda e: self.toggle_microphone())
            self.root.bind('<Control-M>', lambda e: self.toggle_microphone())
            self.status_label.config(text="🐰 Press Ctrl+M to talk to me!")
        else:
            self.status_label.config(text="🐰 Mic shortcut disabled in config")
        
        # Animation state for listening
        self.is_listening = False
        self.listening_ear_angle = 0
        self.listening_head_tilt = 0
        
        # Auto-feeder and auto-sleeper (automatic triggers)
        self.start_auto_care()
        
        # Start carrot dragging system
        self.start_carrot_drag_system()
        
        self.root.after(1500, lambda: self.speak_text("Hi there! I'm Bunzi Bunny! Drag a carrot to me to feed me!"))
    
    def start_carrot_drag_system(self):
        """Create draggable carrot for feeding"""
        self.carrot_image = None
        self.carrot_drag_id = None
        self.carrot_x = 0
        self.carrot_y = 0
        
        # Create a floating carrot that can be dragged
        self.carrot_btn = tk.Label(self.root, text="🥕", font=("Segoe UI Emoji", 32),
                                    bg='#1a1a2e', cursor="fleur")
        self.carrot_btn.place(x=self.screen_width - 80, y=self.screen_height - 80)
        
        # Bind drag events for carrot
        self.carrot_btn.bind('<Button-1>', self.start_carrot_drag)
        self.carrot_btn.bind('<B1-Motion>', self.drag_carrot)
        self.carrot_btn.bind('<ButtonRelease-1>', self.drop_carrot)
        
        # Also add keyboard shortcut for giving carrot (Ctrl+C)
        self.root.bind('<Control-c>', lambda e: self.give_carrot())
        self.root.bind('<Control-C>', lambda e: self.give_carrot())
    
    def start_carrot_drag(self, event):
        """Start dragging the carrot"""
        self.carrot_drag_id = True
        self.carrot_drag_x = event.x
        self.carrot_drag_y = event.y
        self.carrot_btn.config(bg='#ffaa00')
    
    def drag_carrot(self, event):
        """Drag the carrot around"""
        if self.carrot_drag_id:
            x = self.carrot_btn.winfo_x() + event.x - self.carrot_drag_x
            y = self.carrot_btn.winfo_y() + event.y - self.carrot_drag_y
            self.carrot_btn.place(x=x, y=y)
            
            # Check if carrot is near bunny (feeding range)
            bunny_x = self.bunny.x
            bunny_y = self.bunny.y
            carrot_center_x = x + 20
            carrot_center_y = y + 20
            
            # Calculate distance to bunny
            distance = math.sqrt((carrot_center_x - bunny_x) ** 2 + (carrot_center_y - bunny_y) ** 2)
            
            if distance < 80:
                # Feed the bunny!
                self.give_carrot()
                # Reset carrot position
                self.carrot_btn.place(x=self.screen_width - 80, y=self.screen_height - 80)
                self.carrot_drag_id = False
    
    def drop_carrot(self, event):
        """Stop dragging carrot"""
        self.carrot_drag_id = False
        self.carrot_btn.config(bg='#1a1a2e')
        # Reset carrot position if not fed
        self.carrot_btn.place(x=self.screen_width - 80, y=self.screen_height - 80)
    
    def start_auto_care(self):
        """Automatically manage hunger and sleep"""
        def auto_care_loop():
            while self.is_running:
                time.sleep(30)
                if not self.evil_mode_active:
                    if hasattr(self.bunny, 'hunger') and self.bunny.hunger < 30:
                        self.give_carrot()
                    if hasattr(self.bunny, 'energy') and self.bunny.energy < 20 and self.bunny.state != self.bunny.STATE_SLEEPING:
                        self.put_bunny_to_bed()
                    if hasattr(self.bunny, 'hunger'):
                        self.bunny.hunger = max(0, self.bunny.hunger - random.randint(1, 3))
                    if hasattr(self.bunny, 'energy'):
                        self.bunny.energy = max(0, self.bunny.energy - random.randint(0, 2))
        
        threading.Thread(target=auto_care_loop, daemon=True).start()
    
    def give_carrot(self):
        """Give a carrot to the bunny"""
        if hasattr(self.bunny, 'feed_carrot'):
            response = self.bunny.feed_carrot()
            self.speak_text(response)
            self.add_chat_message(f"🐰 Bunzi: {response}")
            self.bunny.add_particle(self.bunny.x, self.bunny.y, "heart", 8)
            # Flash effect on carrot
            self.carrot_btn.config(bg='#00ff00')
            self.root.after(300, lambda: self.carrot_btn.config(bg='#1a1a2e'))
    
    def put_bunny_to_bed(self):
        """Put the bunny to sleep"""
        if hasattr(self.bunny, 'put_to_bed'):
            response = self.bunny.put_to_bed()
            self.speak_text(response)
            self.add_chat_message(f"🐰 Bunzi: {response}")
            self.root.after(10000, self.wake_bunny)
    
    def wake_bunny(self):
        """Wake the bunny up"""
        if hasattr(self.bunny, 'wake_up'):
            response = self.bunny.wake_up()
            if response:
                self.speak_text(response)
                self.add_chat_message(f"🐰 Bunzi: {response}")
    
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Only show UI elements in windowed mode
        if not self.config.get("windowless_mode"):
            self.top_bar = tk.Frame(self.main_frame, bg='#2d2d44', height=35)
            self.top_bar.pack(fill=tk.X)
            self.top_bar.pack_propagate(False)
            
            self.menu_btn = tk.Button(self.top_bar, text="☰", font=("Arial", 11),
                bg='#2d2d44', fg='white', bd=0, padx=12, pady=5, command=self.show_menu, cursor="hand2")
            self.menu_btn.pack(side=tk.LEFT, padx=5)
            
            self.chat_btn = tk.Button(self.top_bar, text="💬", font=("Arial", 11),
                bg='#2d2d44', fg='white', bd=0, padx=12, pady=5, command=self.toggle_chat, cursor="hand2")
            self.chat_btn.pack(side=tk.LEFT, padx=2)
            
            self.mic_btn = tk.Button(self.top_bar, text="🎤", font=("Arial", 11),
                bg='#2d2d44', fg='white', bd=0, padx=12, pady=5, command=self.toggle_microphone, cursor="hand2")
            self.mic_btn.pack(side=tk.LEFT, padx=2)
            
            self.web_toggle = tk.Button(self.top_bar, text="🌐", font=("Arial", 10),
                bg='#00cc44' if self.config.get("web_search_enabled") else '#444444', fg='white', bd=0, padx=8, pady=5,
                command=self.toggle_web_search, cursor="hand2")
            self.web_toggle.pack(side=tk.LEFT, padx=2)
            
            self.repeat_toggle = tk.Button(self.top_bar, text="🔁", font=("Arial", 10),
                bg='#00cc44' if self.repeat_mode_enabled else '#444444', fg='white', bd=0, padx=8, pady=5,
                command=self.toggle_repeat_mode, cursor="hand2")
            self.repeat_toggle.pack(side=tk.LEFT, padx=2)
            
            self.close_btn = tk.Button(self.top_bar, text="✕", font=("Arial", 10, "bold"),
                bg='#e94560', fg='white', bd=0, padx=12, pady=5, command=self.quit_app, cursor="hand2")
            self.close_btn.pack(side=tk.RIGHT, padx=5)
            
            self.title_label = tk.Label(self.top_bar, text="🐰 Bunzi Bunny", font=("Segoe UI", 10, "bold"),
                bg='#2d2d44', fg='#ff69b4')
            self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.bubble_frame = tk.Frame(self.main_frame, bg='white', bd=2, relief=tk.RAISED)
        self.bubble_text = tk.Label(self.bubble_frame, 
            text="🐰 Hi! I'm Bunzi! Drag the carrot 🥕 to me to feed me!",
            font=("Segoe UI", 10), bg='white', fg='#333333', wraplength=320)
        self.bubble_text.pack(padx=12, pady=10)
        
        self.bunny_canvas = tk.Canvas(self.main_frame, width=self.screen_width if self.config.get("windowless_mode") else 280, 
                                       height=self.screen_height if self.config.get("windowless_mode") else 240, 
                                       bg='#1a1a2e', highlightthickness=0)
        
        if self.config.get("windowless_mode"):
            self.bunny_canvas.pack(fill=tk.BOTH, expand=True)
            self.bunny_canvas.config(width=self.screen_width, height=self.screen_height)
            self.bunny = FreeRoamingBunny(self.bunny_canvas, self.config)
            self.bunny.root = self.root
        else:
            self.bunny_canvas.pack(pady=5)
            self.bunny = FreeRoamingBunny(self.bunny_canvas, self.config)
        
        self.chat_frame = tk.Frame(self.main_frame, bg='#0d0d1a', bd=1, relief=tk.SUNKEN)
        self.chat_visible = False
        
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, height=6, width=45,
            bg='#0d0d1a', fg='#00ff41', font=("Courier", 9), wrap=tk.WORD)
        self.chat_display.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        self.chat_entry_frame = tk.Frame(self.chat_frame, bg='#0d0d1a')
        self.chat_entry_frame.pack(pady=5, padx=5, fill=tk.X)
        
        self.chat_entry = tk.Entry(self.chat_entry_frame, bg='#1a1a2e', fg='white', 
                                    font=("Segoe UI", 10), insertbackground='white')
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_entry.bind('<Return>', self.send_chat_message)
        
        self.send_btn = tk.Button(self.chat_entry_frame, text="Send", command=self.send_chat_message,
            bg='#e94560', fg='white', bd=0, padx=15, pady=3, cursor="hand2")
        self.send_btn.pack(side=tk.RIGHT)
        
        self.status_label = tk.Label(self.main_frame, 
            text="🐰 Drag the carrot 🥕 to me to feed me! Press Ctrl+M for microphone!", 
            font=("Segoe UI", 8), bg='#1a1a2e', fg='#888888', wraplength=350)
        self.status_label.pack(pady=5)
        
        self.bunny_canvas.bind('<Button-1>', self.on_bunny_click)
        self.bunny_canvas.bind('<Double-Button-1>', self.on_bunny_pet)
        
        if not self.config.get("windowless_mode"):
            self.top_bar.bind('<Button-1>', self.start_drag)
            self.top_bar.bind('<B1-Motion>', self.do_drag)
            self.top_bar.bind('<ButtonRelease-1>', self.stop_drag)
    
    def show_menu(self):
        # Only show menu in windowed mode
        if self.config.get("windowless_mode"):
            return
        menu = tk.Menu(self.root, tearoff=0, bg='#2d2d44', fg='white')
        menu.add_command(label="🐰 Say Hello", command=lambda: self.speak_text(random.choice(self.vocab.RESPONSES["greeting"])))
        menu.add_command(label="💪 Encouragement", command=lambda: self.speak_text(random.choice(self.vocab.RESPONSES["compliment"])))
        menu.add_command(label="📝 Fun Fact", command=lambda: self.speak_text(random.choice(self.vocab.RESPONSES["fun_fact"])))
        menu.add_command(label="😂 Tell a Joke", command=lambda: self.speak_text(random.choice(self.vocab.RESPONSES["joke"])))
        menu.add_command(label="🥕 Give Carrot", command=self.give_carrot)
        menu.add_command(label="🛏️ Put to Bed", command=self.put_bunny_to_bed)
        menu.add_command(label="😈 Evil Mode", command=self.activate_evil_mode)
        menu.add_command(label="🎮 Play Mini Game", command=self.play_minigame)
        menu.add_command(label="📊 System Status", command=self.show_system_status)
        menu.add_command(label="👋 Wave", command=lambda: self.bunny.wave())
        menu.add_separator()
        menu.add_command(label="🌐 Web Search: " + ("ON" if self.config.get("web_search_enabled") else "OFF"), command=self.toggle_web_search)
        menu.add_command(label="🔁 Repeat Mode: " + ("ON" if self.repeat_mode_enabled else "OFF"), command=self.toggle_repeat_mode)
        menu.add_separator()
        menu.add_command(label="🎤 Toggle Microphone", command=self.toggle_microphone)
        menu.add_command(label="🔊 Toggle Voice", command=self.toggle_voice)
        menu.add_separator()
        menu.add_command(label="❌ Quit Bunzi", command=self.quit_app)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def toggle_chat(self):
        if self.chat_visible:
            self.chat_frame.pack_forget()
            self.chat_visible = False
        else:
            self.chat_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
            self.chat_visible = True
    
    def toggle_web_search(self):
        new_state = not self.config.get("web_search_enabled")
        self.config.set("web_search_enabled", new_state)
        self.browser.enabled = new_state
        if not self.config.get("windowless_mode"):
            self.web_toggle.config(bg='#00cc44' if new_state else '#444444')
        self.show_speech_bubble(f"Web search {'ON' if new_state else 'OFF'}", 1500)
    
    def toggle_repeat_mode(self):
        self.repeat_mode_enabled = not self.repeat_mode_enabled
        if not self.config.get("windowless_mode"):
            self.repeat_toggle.config(bg='#00cc44' if self.repeat_mode_enabled else '#444444')
        self.show_speech_bubble(f"Repeat mode {'ON' if self.repeat_mode_enabled else 'OFF'}", 1500)
    
    def toggle_microphone(self):
        if not self.voice_listening:
            self.voice_listening = True
            if hasattr(self, 'mic_btn') and not self.config.get("windowless_mode"):
                self.mic_btn.config(bg='#e94560')
            if hasattr(self, 'bunny'):
                self.bunny.set_listening(True)
            self.microphone.listen_background(self.process_voice_command)
            self.show_speech_bubble("🎤 Listening... Speak now!", 2000)
            self.status_label.config(text="🎤 Listening... Speak clearly!")
        else:
            self.voice_listening = False
            self.microphone.stop_listening()
            if hasattr(self, 'mic_btn') and not self.config.get("windowless_mode"):
                self.mic_btn.config(bg='#2d2d44')
            if hasattr(self, 'bunny'):
                self.bunny.set_listening(False)
            self.show_speech_bubble("Microphone off", 1500)
            self.status_label.config(text="🐰 Microphone off. Press Ctrl+M to start listening!")
    
    def process_voice_command(self, text):
        self.add_chat_message(f"🎤 You: {text}")
        
        if self.repeat_mode_enabled:
            self.speak_text(f"You said: {text}")
            self.add_chat_message(f"🐰 Bunzi: You said: {text}")
        else:
            self.process_intelligent_response(text)
        
        self.bunny.add_particle(140, 120, "sparkle", 5)
    
    def process_intelligent_response(self, text):
        category = self.vocab.analyze_message(text)
        
        if category:
            response = self.vocab.get_response(category)
            self.speak_text(response)
            self.add_chat_message(f"🐰 Bunzi: {response}")
            self.bunny.set_emotion("happy")
            self.learner.learn_from_interaction(text, response)
        elif self.config.get("web_search_enabled") and len(text) > 3:
            self.speak_text(f"Searching for {text}...")
            self.add_chat_message(f"🔍 Searching: {text}")
            self.browser.search_web(text)
            self.bunny.set_emotion("excited")
        else:
            response = random.choice(self.vocab.RESPONSES["confused"])
            self.speak_text(response)
            self.add_chat_message(f"🐰 Bunzi: {response}")
            self.bunny.set_emotion("confused")
    
    def send_chat_message(self, event=None):
        message = self.chat_entry.get().strip()
        if message:
            self.add_chat_message(f"🐰 You: {message}")
            self.chat_entry.delete(0, tk.END)
            self.process_intelligent_response(message)
    
    def add_chat_message(self, message):
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
    
    def speak_text(self, text):
        self.bunny.set_talking(True)
        self.show_speech_bubble(text, 3000)
        self.voice.speak(text)
        # Keep talking animation longer based on text length
        duration = max(len(text) * 40, 1500)
        self.root.after(duration, lambda: self.bunny.set_talking(False))
        # Force animation update
        self.bunny.update_drawing()
    
    def show_speech_bubble(self, text, duration=3000):
        self.bubble_text.config(text=text)
        self.bubble_frame.place(x=50, y=40, width=340, height=60)
        
        def hide_bubble():
            self.bubble_frame.place_forget()
        
        self.root.after(duration, hide_bubble)
    
    def on_bunny_click(self, event):
        responses = ["Hey! Watch the fur!", "Boop!", "That tickles!", "Hehe!"]
        self.speak_text(random.choice(responses))
        self.bunny.set_emotion("surprised")
        self.root.after(1000, lambda: self.bunny.set_emotion("happy"))
    
    def on_bunny_pet(self, event):
        responses = ["Hehe that tickles!", "More pets please!", "I love when you pet me!", "Purrr~"]
        self.speak_text(random.choice(responses))
        self.bunny.set_emotion("happy")
        self.show_speech_bubble("❤️ Purrrr~ ❤️", 1500)
    
    def activate_evil_mode(self):
        self.evil_mode_active = True
        self.bunny.set_emotion("evil")
        self.speak_text("Mwahahaha! Your desktop is MINE!")
        self.show_speech_bubble("😈 EVIL MODE ACTIVATED! 😈", 3000)
        
        def flash():
            for _ in range(3):
                self.root.configure(bg='#ff0000')
                self.root.update()
                time.sleep(0.1)
                self.root.configure(bg='#1a1a2e')
                self.root.update()
                time.sleep(0.1)
        
        threading.Thread(target=flash, daemon=True).start()
        self.root.after(8000, self.disable_evil_mode)
    
    def disable_evil_mode(self):
        self.evil_mode_active = False
        self.bunny.set_emotion("happy")
        self.speak_text("Just kidding! I'm still your friend!")
        self.show_speech_bubble("❤️ Friendly bunny is back! ❤️", 3000)
    
    def play_minigame(self):
        self.show_speech_bubble("Let's play! Click the moving carrot!", 2000)
        
        score = 0
        game_window = tk.Toplevel(self.root)
        game_window.title("Bunzi's Carrot Catch!")
        game_window.geometry("300x400")
        game_window.configure(bg='#1a1a2e')
        
        score_label = tk.Label(game_window, text=f"Score: {score}", font=("Arial", 14), 
                               bg='#1a1a2e', fg='#00ff41')
        score_label.pack(pady=10)
        
        carrot_btn = tk.Button(game_window, text="🥕", font=("Arial", 24), 
                               bg='orange', fg='orange', cursor="hand2")
        carrot_btn.pack(pady=50)
        
        time_left = 10
        time_label = tk.Label(game_window, text=f"Time: {time_left}", 
                              font=("Arial", 12), bg='#1a1a2e', fg='white')
        time_label.pack(pady=10)
        
        def move_carrot():
            if time_left > 0:
                x = random.randint(50, 250)
                y = random.randint(100, 300)
                carrot_btn.place(x=x, y=y)
                game_window.after(800, move_carrot)
        
        def catch_carrot():
            nonlocal score
            score += 1
            score_label.config(text=f"Score: {score}")
            move_carrot()
        
        def update_timer():
            nonlocal time_left
            if time_left > 0:
                time_left -= 1
                time_label.config(text=f"Time: {time_left}")
                game_window.after(1000, update_timer)
            else:
                carrot_btn.config(state=tk.DISABLED)
                self.show_speech_bubble(f"Game Over! Score: {score}!", 3000)
                if score >= 8:
                    self.bunny.set_emotion("excited")
                    self.speak_text("You're amazing!")
        
        carrot_btn.config(command=catch_carrot)
        move_carrot()
        update_timer()
    
    def show_system_status(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        status = f"CPU: {cpu}%\nMemory: {memory}%"
        if battery:
            status += f"\nBattery: {battery.percent}%"
        
        self.show_speech_bubble(status, 4000)
        self.voice.speak(f"Your CPU is at {cpu} percent, memory at {memory} percent")
    
    def toggle_voice(self):
        self.voice.enabled = not self.voice.enabled
        self.config.set("voice_enabled", self.voice.enabled)
        status = "on" if self.voice.enabled else "off"
        self.show_speech_bubble(f"Voice {status}!", 1500)
    
    def start_background_tasks(self):
        def random_talk():
            while self.is_running:
                time.sleep(random.randint(60, 120))
                if not self.evil_mode_active and not self.voice_listening and random.random() < 0.3:
                    self.speak_text(random.choice(self.vocab.RESPONSES["greeting"]))
        
        def monitor_system():
            while self.is_running:
                cpu = psutil.cpu_percent()
                if cpu > 85 and not self.evil_mode_active:
                    self.speak_text("Your CPU is working really hard!")
                time.sleep(30)
        
        threading.Thread(target=random_talk, daemon=True).start()
        threading.Thread(target=monitor_system, daemon=True).start()
    
    def animate_bunny(self):
        if not self.is_running:
            return
        self.bunny.animate()
        
        if self.evil_mode_active:
            self.status_label.config(text="😈 EVIL MODE ACTIVE! 😈", fg='#ff0000')
        elif self.voice_listening:
            self.status_label.config(text="🎤 Listening... Speak now!", fg='#00ff41')
        else:
            self.status_label.config(text="🐰 Drag the carrot 🥕 to me! Press Ctrl+M for mic!", fg='#888888')
        
        self.root.after(50, self.animate_bunny)
    
    def start_drag(self, event):
        if event.widget in [self.close_btn, self.menu_btn, self.chat_btn, self.mic_btn, self.send_btn, self.chat_entry]:
            return
        self.dragging = True
        self.drag_x = event.x
        self.drag_y = event.y
    
    def do_drag(self, event):
        if self.dragging:
            x = self.root.winfo_x() + event.x - self.drag_x
            y = self.root.winfo_y() + event.y - self.drag_y
            self.root.geometry(f"+{x}+{y}")
    
    def stop_drag(self, event):
        self.dragging = False
    
    def quit_app(self):
        self.is_running = False
        if self.voice_listening:
            self.microphone.stop_listening()
        self.voice.speak("Bye bye! I'll miss you!")
        self.root.after(1000, self.root.quit)
    
    def run(self):
        self.root.mainloop()


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    packages = ['pyttsx3', 'Pillow', 'psutil', 'requests', 'beautifulsoup4', 'speechrecognition', 'pyaudio']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    app = BunziBunny()
    app.run()