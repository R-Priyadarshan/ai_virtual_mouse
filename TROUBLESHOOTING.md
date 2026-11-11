# Troubleshooting Guide

## Voice Not Working

### Root Causes:
1. **No Internet Connection** - Google Speech API requires internet
2. **Microphone Not Detected** - PyAudio can't find your microphone
3. **Microphone is Muted** - System or app-level mute
4. **Google API Issues** - Service unavailable or too many requests

### Solutions:

#### 1. Check Internet Connection
```powershell
# Test connectivity
Test-NetConnection -ComputerName google.com -Port 443
```
If this fails, connect to internet and try again.

#### 2. Check Microphone Detection
```powershell
# List audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); print([p.get_device_info_by_index(i)['name'] for i in range(p.get_device_count())])"
```

#### 3. Reinstall PyAudio
```powershell
.\.venv312\Scripts\pip.exe uninstall PyAudio
.\.venv312\Scripts\pip.exe install PyAudio
```

#### 4. Use Simple Version (No Voice)
If voice keeps failing, use the reliable simple version:
```powershell
.\.venv312\Scripts\python.exe virtual_mouse_simple.py
```

## Peace Sign & Scroll Not Working

### Root Causes:
1. **Gesture not clear enough** - Fingers not clearly extended
2. **Hand orientation wrong** - Peace sign upside down
3. **Distance threshold too strict** - Gesture recognition too sensitive

### Solutions:

#### 1. Make Clear Gesture
- **Peace Sign**: Hold index and middle fingers UP and APART
- Point them toward camera (not sideways)
- Fold ring and pinky fingers DOWN
- Make gesture slow and deliberate

#### 2. Scroll Gesture
- Extend all 4 fingers (index, middle, ring, pinky)
- Point UP to scroll up
- Point DOWN to scroll down
- Hold for 1 second

#### 3. Test in Simple Mode
The simple version has better scroll detection:
```powershell
.\.venv312\Scripts\python.exe virtual_mouse_simple.py
```

#### 4. Adjust Detection Sensitivity
Edit `gesture_handler.py` and increase thresholds:
```python
# Line ~88 - Make detection more lenient
index_extended = index_tip.y < index_pip.y - 0.03  # Was 0.05
middle_extended = middle_tip.y < middle_pip.y - 0.03
```

## Hand Not Detected

### Root Causes:
1. **Poor lighting** - Camera can't see hand clearly
2. **Hand outside frame** - Not visible in camera
3. **Background interference** - Complex background confuses detection
4. **Camera resolution too low** - Webcam quality issue

### Solutions:

#### 1. Improve Lighting
- Use well-lit environment
- Position light source facing you
- Avoid backlighting
- Use daylight or bright lamp

#### 2. Position Hand Correctly
- Stay 30-80cm from camera
- Keep hand within purple rectangle
- Make sure entire hand is visible
- Avoid extreme angles

#### 3. Simplify Background
- Use plain, solid-color wall
- Remove busy backgrounds
- Move away from patterned surfaces

#### 4. Check Camera Quality
```powershell
.\.venv312\Scripts\python.exe webcam_test.py
```
If video is blurry or dark, you may need a better webcam.

## Cursor Jumps Around

### Root Causes:
1. **Hand detection unstable** - Lighting or hand visibility issues
2. **Smoothing too low** - Cursor updates too fast
3. **Detection sensitivity wrong** - Finger positions inaccurate

### Solutions:

#### 1. Increase Smoothing
Edit `virtual_mouse.py` or `virtual_mouse_simple.py`:
```python
SMOOTHING = 10  # Higher = smoother (was 5)
```

#### 2. Improve Lighting
- Better lighting makes detection more stable
- Avoid shadows on hand

#### 3. Increase Detection Confidence
Edit the Hands configuration:
```python
with mp_hands.Hands(
    min_detection_confidence=0.8,  # Higher threshold
    min_tracking_confidence=0.8
) as hands:
```

## Application Crashes

### Common Errors:

#### "Could not open webcam"
- Webcam is in use by another application
- Close other apps using camera (Zoom, Teams, etc.)
- Restart computer

#### "No module named cv2"
```powershell
.\.venv312\Scripts\pip.exe install --upgrade opencv-python
```

#### "No module named mediapipe"
```powershell
.\.venv312\Scripts\pip.exe install --upgrade mediapipe
```

## Performance Issues

### Slow FPS

#### Solutions:
1. **Close other applications** - Free up CPU
2. **Lower detection confidence**:
```python
min_detection_confidence=0.6,  # Lower = faster but less accurate
```

3. **Use simple version** - Faster than enhanced version
```powershell
.\.venv312\Scripts\python.exe virtual_mouse_simple.py
```

4. **Check CPU usage** - Open Task Manager
   - Close unnecessary background processes

## Which Version to Use?

| Version | Best For | Requires |
|---------|----------|----------|
| **simple.py** | Reliable gesture control | None (offline) |
| **virtual_mouse.py** | Original gesture only | None (offline) |
| **enhanced.py** | Gesture + voice | Microphone + Internet |

### Decision Tree:
1. **Want voice?** → Use `virtual_mouse_enhanced.py`
2. **Voice not working?** → Use `virtual_mouse_simple.py`
3. **Want minimal features?** → Use `virtual_mouse.py`

## Still Not Working?

### Try This:
1. **Restart application** - Close and run again
2. **Restart computer** - Full restart sometimes helps
3. **Update Python**: `python -m pip install --upgrade pip`
4. **Fresh install**:
   ```powershell
   .\.venv312\Scripts\pip.exe install --upgrade opencv-python mediapipe pyautogui
   ```

### Debug Mode:
Run in debug to see detailed output:
```powershell
.\.venv312\Scripts\python.exe -u virtual_mouse_simple.py
```

## Getting Help

**When reporting issues, include:**
1. Which version you're using
2. Exact error message
3. Your system (Windows version)
4. What you were trying to do
5. Steps to reproduce

**Check the USAGE_GUIDE.md** for more details on gestures and commands.
