# AI Virtual Mouse - Usage Guide

## Quick Start

### Option 1: Original Version (Gesture Only)
```bash
python virtual_mouse.py
```
Use hand gestures to control your mouse.

### Option 2: Enhanced Version (Gesture + Voice)
```bash
python virtual_mouse_enhanced.py
```
Use hand gestures and/or voice commands to control your mouse.

## Gesture Controls

### Basic Gestures
- **Move Cursor**: Point your index finger at the camera
- **Click**: Pinch thumb and index finger together
- **Double-Click**: Pinch twice quickly (within 0.3 seconds)
- **Right-Click**: Touch index and middle finger together

### Advanced Gestures
- **Scroll Up**: Make a "peace sign" with index and middle fingers extended
- **Scroll Down**: Same as above (direction is detected automatically)
- **Drag**: Hold pinch while moving your hand

### Tips for Better Gesture Recognition
1. **Lighting**: Ensure good lighting for accurate hand detection
2. **Hand Position**: Keep your hand within the purple rectangle on screen
3. **Gestures**: Make clear, deliberate hand positions
4. **Distance**: Stay 30-80cm away from the camera
5. **Background**: Neutral background works better

## Voice Commands

### Mouse Control
| Command | Action |
|---------|--------|
| "click" | Left mouse click |
| "double click" | Double click |
| "right click" | Right mouse click |
| "scroll up" | Scroll up |
| "scroll down" | Scroll down |

### Application Control
| Command | Action |
|---------|--------|
| "open chrome" | Open Google Chrome |
| "open firefox" | Open Firefox |
| "open notepad" | Open Notepad |
| "open calculator" | Open Calculator |
| "open edge" | Open Microsoft Edge |
| "close window" | Close active window |
| "minimize" | Minimize active window |
| "maximize" | Maximize active window |

### Supported Applications
- Chrome
- Firefox
- Notepad
- Calculator
- Edge (Microsoft)
- Word
- Excel
- PowerPoint
- VS Code
- Python

### Voice Tips
1. **Clear Speech**: Speak clearly and at normal pace
2. **Microphone**: Ensure microphone is working and not muted
3. **Noise**: Minimize background noise for better recognition
4. **Volume**: Speak at conversational volume
5. **Internet**: Voice recognition requires internet connection (uses Google API)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `v` | Toggle voice mode |
| `g` | Gesture mode only |
| `m` | Voice mode only |
| `b` | Both gesture and voice |
| `i` | Toggle info panel |

## Modes

### Gesture Mode (g)
- Only hand gestures are active
- Voice recognition is disabled
- Faster performance
- **Use when**: You don't have a microphone or prefer hand control

### Voice Mode (m)
- Only voice commands are active
- Gesture recognition is disabled
- **Use when**: Your hands are busy or you prefer voice

### Both Modes (b)
- Both gesture and voice commands are active
- Slower performance
- Most flexibility
- **Use when**: You want maximum control options

## Customization

### Adjust Sensitivity

Edit `virtual_mouse_enhanced.py`:
```python
CLICK_THRESHOLD = 30  # Lower = more sensitive pinch detection
SMOOTHING = 5         # Higher = smoother but slower response
FRAME_MARGIN = 80     # Tracking area size
```

## Troubleshooting

### Voice Not Working
1. Check microphone is connected and working
2. Ensure PyAudio is installed: `pip install PyAudio`
3. Check internet connection (for speech recognition)
4. Try speaking louder and more clearly

### Hand Not Detected
1. Improve lighting
2. Move closer to camera (30-80cm)
3. Use neutral background
4. Ensure hand is fully visible

### Cursor Jumps Around
1. Reduce SMOOTHING value (lower = faster response)
2. Improve lighting
3. Reduce camera distance slightly

### Application Won't Open
1. Make sure application is installed on your system
2. Check if application name matches supported list
3. Try full path: "open C:/Program Files/app.exe"

## Performance Tips

1. **Reduce Resolution**: Lower camera resolution for faster processing
2. **Use Gesture Only**: Disable voice to save CPU
3. **Reduce FPS**: More CPU available for other tasks
4. **Close Other Apps**: Free up system resources

## Safety

### Fail-Safe Disabled
- The fail-safe is disabled in enhanced mode for full control
- **Be careful**: Don't point hands at corners unexpectedly
- Emergency exit: Press `Alt+Tab` then close window

### Recommended Usage
- Always keep keyboard within reach
- Start with gesture-only mode
- Practice in safe environment first
- Keep caffeine nearby for long sessions 😊

## Advanced Usage

### Combining Gestures and Voice
The strongest use case is combining both:
1. Use **gestures** for precise mouse movement and clicking
2. Use **voice** for application control and shortcuts

Example workflow:
```
"open chrome"              # Voice: open application
(move finger to address bar)  # Gesture: move cursor
"click"                    # Voice: click on search box
(type your search)         # Keyboard: natural input
"scroll down"              # Voice: scroll results
(move finger to link)      # Gesture: position cursor
"click"                    # Gesture: pinch to click
```

### Custom Voice Commands
Edit `voice_handler.py` to add custom commands:
```python
self.commands = {
    "click": "click",
    "double click": "double_click",
    "your_command": "your_action",  # Add here
}
```

## Keyboard Input

You can still use your keyboard for typing:
- The application doesn't interfere with keyboard input
- Use voice or gestures for mouse control
- Type normally for text input

## Accessibility

This application is useful for:
- **Accessibility**: Control computer without traditional input devices
- **Accessibility**: Reduce repetitive strain from clicking
- **Presentations**: Hands-free navigation
- **Gaming**: Alternative control method
- **Cooking**: Hands-free operation (dirty hands)
- **Physical therapy**: Safe, non-contact interaction

## FAQ

**Q: Can I use this without internet?**
A: Gestures work offline. Voice needs internet for Google Speech API.

**Q: Does this work with multiple monitors?**
A: Yes, it maps to your full screen resolution automatically.

**Q: Can I control other people's computers?**
A: No, it's designed for local use only.

**Q: Is this slow?**
A: Gesture mode runs at 30+ FPS on most machines. Voice adds ~1-2 seconds latency.

**Q: Can I improve accuracy?**
A: Yes - better lighting, steady hand position, and practice help greatly.

## Resources

- [MediaPipe Hand Tracking](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [SpeechRecognition Documentation](https://github.com/Uberi/speech_recognition)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)

## Contributing

Want to add features? Ideas:
- Eye tracking for cursor control
- Custom gesture training
- Gesture recording and playback
- Multi-language voice support
- Machine learning gesture classifier

## License

Open source - feel free to use and modify!
