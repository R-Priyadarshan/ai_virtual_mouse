"""
Voice Recognition Module
Handles voice commands for mouse control and application management
"""

import threading
import subprocess
import psutil
import time

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False


class VoiceHandler:
    def __init__(self):
        self.recognizer = None
        self.microphone = None
        self.listening = False
        self.recognition_available = SPEECH_RECOGNITION_AVAILABLE
        
        # Voice command mappings
        self.commands = {
            "click": "click",
            "double click": "double_click",
            "right click": "right_click",
            "scroll up": "scroll_up",
            "scroll down": "scroll_down",
        }
        
        # Application commands
        self.app_commands = {
            "open": "open",
            "close": "close",
            "minimize": "minimize",
            "maximize": "maximize",
            "close window": "close",
            "minimize window": "minimize",
        }
        
        self.last_command_time = 0.0
        self.command_cooldown = 1.0  # Prevent too many commands
        
        if self.recognition_available:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                print("✓ Voice recognition initialized")
            except Exception as e:
                print(f"✗ Voice initialization error: {e}")
                self.recognition_available = False
    
    def listen(self):
        """Listen for voice command and return recognized text"""
        if not self.recognition_available or not self.recognizer:
            return None
        
        try:
            with self.microphone as source:
                # Reduce noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio with longer timeout
                audio = self.recognizer.listen(source, timeout=3.0, phrase_time_limit=3.0)
            
            # Recognize speech with multiple attempts
            try:
                text = self.recognizer.recognize_google(audio, language='en-US').lower()
                if text and len(text) > 0:
                    return text
                return None
            except sr.UnknownValueValue:
                return None
            except sr.RequestError as e:
                return None
        
        except sr.RequestError:
            return None
        except Exception:
            return None
    
    def get_voice_command(self):
        """Get voice command from user"""
        current_time = time.monotonic()
        
        # Check cooldown
        if current_time - self.last_command_time < self.command_cooldown:
            return None
        
        text = self.listen()
        if not text:
            return None
        
        self.last_command_time = current_time
        
        # Check for mouse control commands
        for voice_cmd, action in self.commands.items():
            if voice_cmd in text:
                return action
        
        # Check for app commands
        for voice_cmd, action in self.app_commands.items():
            if voice_cmd in text:
                # Extract app name if available
                words = text.split()
                if "open" in text:
                    # Find app name after "open"
                    open_idx = words.index("open")
                    if open_idx + 1 < len(words):
                        app_name = " ".join(words[open_idx + 1:])
                        return f"open:{app_name}"
                return action
        
        return None
    
    def execute_voice_action(self, action):
        """Execute action from voice command"""
        if not action:
            return
        
        if action == "click":
            return "click"
        elif action == "double_click":
            return "double_click"
        elif action == "right_click":
            return "right_click"
        elif action == "scroll_up":
            return "scroll_up"
        elif action == "scroll_down":
            return "scroll_down"
        elif action == "close":
            self.close_active_window()
        elif action == "minimize":
            self.minimize_active_window()
        elif action == "maximize":
            self.maximize_active_window()
        elif action.startswith("open:"):
            app_name = action.split(":", 1)[1]
            self.open_application(app_name)
        
        return None
    
    @staticmethod
    def close_active_window():
        """Close the active window"""
        try:
            # Get active window and close it
            subprocess.run("taskkill /FI \"STATUS eq RUNNING\" /IM explorer.exe", 
                          shell=True, check=False, capture_output=True)
            # More graceful: send Alt+F4
            subprocess.run("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys('%{F4}')\"",
                          shell=True, check=False, capture_output=True)
            print("Closing active window...")
        except Exception as e:
            print(f"Error closing window: {e}")
    
    @staticmethod
    def minimize_active_window():
        """Minimize the active window"""
        try:
            subprocess.run("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys('%~ ')\"",
                          shell=True, check=False, capture_output=True)
            print("Minimizing active window...")
        except Exception as e:
            print(f"Error minimizing window: {e}")
    
    @staticmethod
    def maximize_active_window():
        """Maximize the active window"""
        try:
            subprocess.run("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys('{F5}')\"",
                          shell=True, check=False, capture_output=True)
            print("Maximizing active window...")
        except Exception as e:
            print(f"Error maximizing window: {e}")
    
    @staticmethod
    def open_application(app_name):
        """Open an application by name"""
        app_name = app_name.strip().lower()
        
        app_paths = {
            "chrome": "chrome",
            "firefox": "firefox",
            "notepad": "notepad",
            "calc": "calc",
            "calculator": "calc",
            "edge": "msedge",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "vs code": "code",
            "visual studio": "devenv",
            "python": "python",
        }
        
        executable = app_paths.get(app_name, app_name)
        
        try:
            subprocess.Popen(executable)
            print(f"Opening {app_name}...")
        except Exception as e:
            print(f"Could not open {app_name}: {e}")
    
    @staticmethod
    def start_listening_thread(callback):
        """Start listening in a separate thread"""
        def listen_loop():
            while True:
                try:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break
        
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
        return thread
