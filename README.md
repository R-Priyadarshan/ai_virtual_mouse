# AI Virtual Mouse - Enhanced Edition

An AI-powered virtual mouse application with hand tracking, gesture control, and voice recognition. Control your computer cursor and perform actions using hand gestures and voice commands detected through MediaPipe and speech recognition.

## Features

### Gesture Control
- **Hand Tracking**: Real-time hand detection using MediaPipe
- **Cursor Control**: Move your mouse cursor by pointing with your index finger
- **Click Detection**: Perform clicks by pinching your thumb and index finger together
- **Double-Click**: Pinch twice quickly to double-click
- **Right-Click**: Use index and middle finger together for right-click
- **Scroll Gestures**: Use peace sign (two fingers) to scroll
- **Smooth Movement**: Smoothing algorithm for fluid cursor movement
- **Activity Area**: Visual indicator of the active tracking area on screen

### Voice Recognition
- **Voice Commands**: Control mouse with voice commands
- **Application Control**: Open, close, and minimize applications via voice
- **Multi-Mode**: Switch between gesture, voice, or both modes
- **Real-time Processing**: Simultaneous gesture and voice detection

### UI/UX
- **Mode Indicator**: See current control mode on screen
- **FPS Counter**: Monitor application performance
- **Hand Detection Status**: Visual feedback on hand detection
- **On-Screen Controls**: Keyboard shortcuts displayed on screen

## How It Works

The application uses computer vision, hand tracking, and machine learning to:

1. **Gesture Recognition**: Detect hand landmarks using MediaPipe's hand tracking model
2. **Cursor Control**: Map the position of your index fingertip to screen coordinates
3. **Mouse Actions**: Recognize gestures (pinch, double-click, scroll, right-click)
4. **Voice Processing**: Listen to voice commands and execute corresponding actions
5. **Real-time Feedback**: Display detected gestures and voice commands on screen

## Requirements

- Python 3.12+
- Webcam
- Windows/Mac/Linux

## Dependencies

- `opencv-python` - Computer vision library
- `mediapipe` - Hand tracking and pose estimation
- `pyautogui` - Mouse control automation
- `SpeechRecognition` - Voice command recognition
- `pydub` - Audio processing
- `psutil` - System process management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/R-Priyadarshan/ai_virtual_mouse.git
cd ai_virtual_mouse
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install opencv-python mediapipe pyautogui SpeechRecognition pydub psutil
```

## Usage

### 1. Original Version (Gesture Only)
Run the original virtual mouse with gesture control only:
```bash
python virtual_mouse.py
```

### 2. Enhanced Version (Gesture + Voice)
Run the enhanced version with gesture and voice recognition:
```bash
python virtual_mouse_enhanced.py
```

### Controls

**Keyboard Shortcuts:**
- `q` - Quit application
- `v` - Toggle voice mode on/off
- `g` - Gesture mode only
- `m` - Voice mode only
- `b` - Both gesture and voice modes
- `i` - Toggle info panel

**Gesture Controls:**
- Move your **index finger** to move the cursor
- **Pinch** (thumb + index) to click
- **Double pinch** (pinch twice) to double-click
- **Peace sign** (index + middle extended) to scroll up/down
- **Right pinch** (index + middle together) to right-click

**Voice Commands:**

*Mouse Control:*
- "click" - Left click
- "double click" - Double click
- "right click" - Right click
- "scroll up" - Scroll up
- "scroll down" - Scroll down

*Application Control:*
- "open [app name]" - Open application (e.g., "open chrome")
- "close window" - Close active window
- "minimize" - Minimize active window
- "maximize" - Maximize active window

Supported applications: Chrome, Firefox, Notepad, Calculator, Edge, Word, Excel, PowerPoint, VS Code, Python

## Configuration

Edit the constants in `virtual_mouse_enhanced.py` to customize behavior:

```python
SCREEN_W, SCREEN_H      # Screen resolution (auto-detected)
FRAME_MARGIN = 80       # Border margin for hand tracking area
SMOOTHING = 5           # Cursor smoothing factor (higher = smoother but slower)
CLICK_THRESHOLD = 30    # Distance between thumb and index for click (lower = more sensitive)
CLICK_COOLDOWN = 0.5    # Minimum time between clicks
```

## Files

- `virtual_mouse.py` - Original application with gesture control only
- `virtual_mouse_enhanced.py` - Enhanced version with gesture + voice
- `gesture_handler.py` - Gesture recognition module
- `voice_handler.py` - Voice command recognition module
- `hand_tracking.py` - Hand detection visualization
- `webcam_test.py` - Simple webcam test utility
- `USAGE_GUIDE.md` - Comprehensive usage guide

## Tips for Best Results

### Hand Detection
- Ensure good lighting for better hand detection
- Keep your hand within the purple rectangle shown on screen
- Adjust `CLICK_THRESHOLD` if pinch detection is too sensitive
- Lower `SMOOTHING` value for more responsive cursor movement

### Voice Recognition
- Speak clearly at normal volume
- Minimize background noise
- Ensure microphone is properly connected
- Maintain internet connection for Google Speech API

### General Usage
- Start with gesture-only mode for better performance
- Practice hand gestures in safe environment first
- Use voice for application control, gestures for precision
- Keep keyboard accessible for emergency exit (Ctrl+C)

## Safety

The fail-safe is disabled to allow full mouse control. Be careful with hand gestures, especially avoid sudden movements toward screen corners.

**Emergency Stop:** 
- Press `q` to quit
- Press `Ctrl+C` in terminal
- Close the window manually

