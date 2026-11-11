"""
AI Virtual Mouse - Enhanced Edition
Hand tracking with gesture control and voice recognition
"""

import cv2
import mediapipe as mp
import pyautogui
import math
import time
import threading
from gesture_handler import GestureHandler
from voice_handler import VoiceHandler

# Screen and webcam settings
SCREEN_W, SCREEN_H = pyautogui.size()
FRAME_MARGIN = 80
SMOOTHING = 5
CLICK_THRESHOLD = 30
CLICK_COOLDOWN = 0.5

prev_x, prev_y = 0.0, 0.0
last_click = 0.0

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01

# Initialize modules
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
gesture_handler = GestureHandler(click_threshold=CLICK_THRESHOLD)
voice_handler = VoiceHandler()

# State variables
voice_command = None
voice_command_lock = threading.Lock()
mode = "gesture"  # Can be "gesture", "voice", or "both"
show_info = True


def voice_recognition_thread():
    """Run voice recognition in a separate thread"""
    print("🎤 Voice recognition thread started (press 'v' to toggle)")
    while True:
        try:
            if mode in ["voice", "both"]:
                command = voice_handler.get_voice_command()
                if command:
                    with voice_command_lock:
                        global voice_command
                        voice_command = command
                        print(f"🎤 Voice command: {command}")
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Voice error: {e}")
            time.sleep(0.5)


def execute_gesture(gesture, current_x, current_y):
    """Execute mouse action based on gesture"""
    if gesture == "click":
        pyautogui.click()
        print("🖱️ Click")
    elif gesture == "double_click":
        pyautogui.click(clicks=2)
        print("🖱️ Double click")
    elif gesture == "right_click":
        pyautogui.click(button='right')
        print("🖱️ Right click")
    elif gesture == "scroll_up":
        pyautogui.scroll(5)
        print("🖱️ Scroll up")
    elif gesture == "scroll_down":
        pyautogui.scroll(-5)
        print("🖱️ Scroll down")


def execute_voice_action(action, current_x, current_y):
    """Execute action from voice command"""
    if action == "click":
        pyautogui.click()
        print("🎤→ Click")
    elif action == "double_click":
        pyautogui.click(clicks=2)
        print("🎤→ Double click")
    elif action == "right_click":
        pyautogui.click(button='right')
        print("🎤→ Right click")
    elif action == "scroll_up":
        pyautogui.scroll(5)
        print("🎤→ Scroll up")
    elif action == "scroll_down":
        pyautogui.scroll(-5)
        print("🎤→ Scroll down")


def draw_info_panel(frame, mode, fps, hand_detected):
    """Draw information panel on frame"""
    # Draw mode indicator
    mode_color = (0, 255, 0) if mode == "gesture" else (255, 0, 0) if mode == "voice" else (0, 165, 255)
    mode_text = f"Mode: {mode.upper()}"
    cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, mode_color, 2)
    
    # Draw FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Draw hand detection status
    hand_color = (0, 255, 0) if hand_detected else (0, 0, 255)
    hand_text = "Hand: DETECTED" if hand_detected else "Hand: NOT DETECTED"
    cv2.putText(frame, hand_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 2)
    
    # Draw controls
    h, w = frame.shape[:2]
    controls = [
        "Controls:",
        "q - Quit",
        "v - Toggle voice",
        "g - Gesture mode",
        "m - Voice mode",
        "b - Both mode"
    ]
    
    y_offset = 30
    for i, control in enumerate(controls):
        cv2.putText(frame, control, (w - 250, y_offset + i * 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)


def main():
    global prev_x, prev_y, last_click, voice_command, mode, show_info
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")
    
    # Start voice recognition thread
    voice_thread = threading.Thread(target=voice_recognition_thread, daemon=True)
    voice_thread.start()
    
    print("=" * 60)
    print("🎯 AI Virtual Mouse - Enhanced Edition")
    print("=" * 60)
    print("✓ Gesture control enabled")
    print("✓ Voice recognition enabled")
    print("\nControls:")
    print("  q - Quit")
    print("  v - Toggle voice (currently OFF)")
    print("  g - Gesture mode only")
    print("  m - Voice mode only")
    print("  b - Both modes")
    print("  i - Toggle info panel")
    print("\nGesture controls:")
    print("  - Move finger to move cursor")
    print("  - Pinch to click")
    print("  - Peace sign (two fingers) to scroll")
    print("\nVoice commands:")
    print("  'click', 'double click', 'right click'")
    print("  'scroll up', 'scroll down'")
    print("  'open [app]', 'close window', 'minimize'")
    print("=" * 60 + "\n")
    
    fps_clock = time.time()
    fps_counter = 0
    fps = 0
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            
            # Calculate FPS
            fps_counter += 1
            if time.time() - fps_clock > 1:
                fps = fps_counter
                fps_counter = 0
                fps_clock = time.time()
            
            # Draw active movement area
            cv2.rectangle(
                frame,
                (FRAME_MARGIN, FRAME_MARGIN),
                (w - FRAME_MARGIN, h - FRAME_MARGIN),
                (255, 0, 255),
                2
            )
            
            hand_detected = False
            
            if results.multi_hand_landmarks:
                hand_detected = True
                hand = results.multi_hand_landmarks[0]
                landmarks = hand.landmark
                
                mp_draw.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )
                
                # Finger coordinates
                index = landmarks[8]
                thumb = landmarks[4]
                middle = landmarks[12]
                
                ix, iy = int(index.x * w), int(index.y * h)
                tx, ty = int(thumb.x * w), int(thumb.y * h)
                mx, my = int(middle.x * w), int(middle.y * h)
                
                # Map camera coordinates to screen coordinates
                target_x = (ix - FRAME_MARGIN) / (w - 2 * FRAME_MARGIN) * SCREEN_W
                target_y = (iy - FRAME_MARGIN) / (h - 2 * FRAME_MARGIN) * SCREEN_H
                
                target_x = max(0, min(SCREEN_W - 1, target_x))
                target_y = max(0, min(SCREEN_H - 1, target_y))
                
                # Smooth cursor movement
                curr_x = prev_x + (target_x - prev_x) / SMOOTHING
                curr_y = prev_y + (target_y - prev_y) / SMOOTHING
                
                pyautogui.moveTo(int(curr_x), int(curr_y))
                prev_x, prev_y = curr_x, curr_y
                
                # Draw finger markers
                cv2.circle(frame, (ix, iy), 8, (0, 255, 0), -1)
                cv2.circle(frame, (tx, ty), 8, (255, 0, 0), -1)
                cv2.circle(frame, (mx, my), 8, (0, 0, 255), -1)
                cv2.line(frame, (ix, iy), (tx, ty), (0, 255, 255), 2)
                
                # Gesture detection
                if mode in ["gesture", "both"]:
                    gesture = gesture_handler.get_gesture(
                        (tx, ty), (ix, iy), landmarks, (curr_x, curr_y)
                    )
                    
                    if gesture:
                        execute_gesture(gesture, curr_x, curr_y)
                        cv2.putText(
                            frame, f"GESTURE: {gesture.upper()}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 0), 2
                        )
            
            # Handle voice commands
            if mode in ["voice", "both"]:
                with voice_command_lock:
                    if voice_command:
                        execute_voice_action(voice_command, prev_x, prev_y)
                        cv2.putText(
                            frame, f"VOICE: {voice_command.upper()}", (20, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 165, 255), 2
                        )
                        voice_command = None
            
            # Draw info panel
            if show_info:
                draw_info_panel(frame, mode, fps, hand_detected)
            
            cv2.imshow("AI Virtual Mouse - Enhanced", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("\n👋 Exiting...")
                break
            elif key == ord("v"):
                # Toggle voice
                if mode == "gesture":
                    mode = "both"
                    print("🎤 Voice enabled (mode: BOTH)")
                elif mode == "both":
                    mode = "gesture"
                    print("🔇 Voice disabled (mode: GESTURE)")
                elif mode == "voice":
                    mode = "both"
                    print("🎤 Both modes enabled")
            elif key == ord("g"):
                mode = "gesture"
                print("✋ Gesture mode only")
            elif key == ord("m"):
                mode = "voice"
                print("🎤 Voice mode only")
            elif key == ord("b"):
                mode = "both"
                print("🎤✋ Both modes enabled")
            elif key == ord("i"):
                show_info = not show_info
                print(f"ℹ️ Info panel: {'ON' if show_info else 'OFF'}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("✓ Application closed")


if __name__ == "__main__":
    main()
