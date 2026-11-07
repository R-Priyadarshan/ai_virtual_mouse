# AI Virtual Mouse

An AI-powered virtual mouse application that uses hand tracking via webcam to control your computer cursor. Control your mouse movements and perform clicks using hand gestures detected through MediaPipe.

## Features

- **Hand Tracking**: Real-time hand detection using MediaPipe
- **Cursor Control**: Move your mouse cursor by pointing with your index finger
- **Click Detection**: Perform clicks by pinching your thumb and index finger together
- **Smooth Movement**: Smoothing algorithm for fluid cursor movement
- **Activity Area**: Visual indicator of the active tracking area on screen

## How It Works

The application uses computer vision and machine learning to:

1. Detect hand landmarks using MediaPipe's hand tracking model
2. Map the position of your index fingertip to screen coordinates
3. Move the mouse cursor to follow your finger
4. Detect pinch gestures (thumb and index finger together) to trigger mouse clicks

## Requirements

- Python 3.12+
- Webcam
- Windows/Mac/Linux

## Dependencies

- `opencv-python` - Computer vision library
- `mediapipe` - Hand tracking and pose estimation
- `pyautogui` - Mouse control automation

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
pip install opencv-python mediapipe pyautogui
```

## Usage

### 1. Test Your Webcam
Start with the webcam test to ensure your camera is working:
```bash
python webcam_test.py
```
Press 'q' to quit.

### 2. Hand Tracking Demo
View hand landmarks and tracking:
```bash
python hand_tracking.py
```
This shows real-time hand detection with joint landmarks highlighted.
Press 'q' to quit.

### 3. Virtual Mouse
Launch the full virtual mouse application:
```bash
python virtual_mouse.py
```

**Controls:**
- Move your **index finger** to move the cursor
- **Pinch** your thumb and index finger together to click
- Press 'q' to quit the application

## Configuration

Edit the constants in `virtual_mouse.py` to customize behavior:

- `SCREEN_W, SCREEN_H` - Screen resolution
- `FRAME_MARGIN` - Border margin for hand tracking area
- `SMOOTHING` - Cursor smoothing factor (higher = smoother but slower response)
- `CLICK_THRESHOLD` - Distance between thumb and index finger to trigger click
- `CLICK_COOLDOWN` - Minimum time between clicks (prevents accidental double-clicks)

## Files

- `virtual_mouse.py` - Main application with cursor control and click detection
- `hand_tracking.py` - Hand detection and landmark visualization
- `webcam_test.py` - Simple webcam test utility

## Safety

The application includes a failsafe mechanism (`pyautogui.FAILSAFE = True`). Move your mouse to the top-left corner of the screen to emergency stop if needed.

## Tips

- Ensure good lighting for better hand detection
- Keep your hand within the purple rectangle shown on screen
- Adjust `CLICK_THRESHOLD` if pinch detection is too sensitive or not sensitive enough
- Lower `SMOOTHING` value for more responsive cursor movement

## License

Open source - feel free to use and modify!

## Author

R-Priyadarshan

