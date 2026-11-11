"""
AI Virtual Mouse - Simple & Reliable Version
Hand tracking with basic gesture control
No voice (more stable, no internet required)
"""

import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Screen and webcam settings
SCREEN_W, SCREEN_H = pyautogui.size()
FRAME_MARGIN = 80
SMOOTHING = 5
CLICK_THRESHOLD = 30
CLICK_COOLDOWN = 0.5

prev_x, prev_y = 0.0, 0.0
last_click = 0.0
last_gesture_time = 0.0

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01

# Initialize modules
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def get_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.hypot(point1[0] - point2[0], point1[1] - point2[1])


def detect_pinch(thumb_pos, index_pos):
    """Detect if thumb and index finger are pinching"""
    distance = get_distance(thumb_pos, index_pos)
    return distance < CLICK_THRESHOLD, distance


def main():
    global prev_x, prev_y, last_click, last_gesture_time
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return
    
    print("=" * 60)
    print("🎯 AI Virtual Mouse - Simple & Reliable Version")
    print("=" * 60)
    print("✓ Gesture control enabled")
    print("✓ Fast, stable, no internet required")
    print("\nControls:")
    print("  q - Quit")
    print("  i - Toggle info panel")
    print("\nGesture controls:")
    print("  - Move finger to move cursor")
    print("  - Pinch to click")
    print("  - Extended fingers: point up to scroll up, down to scroll down")
    print("=" * 60 + "\n")
    
    fps_clock = time.time()
    fps_counter = 0
    fps = 0
    show_info = True
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
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
                
                ix, iy = int(index.x * w), int(index.y * h)
                tx, ty = int(thumb.x * w), int(thumb.y * h)
                
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
                cv2.line(frame, (ix, iy), (tx, ty), (0, 255, 255), 2)
                
                # Click detection
                is_pinching, distance = detect_pinch((tx, ty), (ix, iy))
                
                current_time = time.monotonic()
                
                if is_pinching:
                    cv2.putText(
                        frame, f"PINCH DETECTED - Distance: {distance:.0f}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 255), 2
                    )
                    
                    if current_time - last_click > CLICK_COOLDOWN:
                        pyautogui.click()
                        last_click = current_time
                        print("🖱️ Click detected!")
                
                # Scroll detection - based on hand orientation
                # Count extended fingers
                extended_fingers = 0
                
                # Check each finger if extended (tip above PIP joint)
                for finger_tip_idx, finger_pip_idx in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    tip = landmarks[finger_tip_idx]
                    pip = landmarks[finger_pip_idx]
                    if tip.y < pip.y - 0.05:
                        extended_fingers += 1
                
                # If 4+ fingers extended, detect scroll direction
                if extended_fingers >= 3 and current_time - last_gesture_time > 0.5:
                    # Get hand orientation
                    wrist = landmarks[0]
                    middle_tip = landmarks[12]
                    
                    # If wrist is below fingers, hand pointing up
                    if wrist.y > middle_tip.y + 0.1:
                        pyautogui.scroll(3)
                        print("⬆️ Scroll up!")
                        last_gesture_time = current_time
                        cv2.putText(frame, "SCROLL UP", (20, 70),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                  (0, 255, 0), 2)
                    # If wrist is above fingers, hand pointing down
                    elif wrist.y < middle_tip.y - 0.1:
                        pyautogui.scroll(-3)
                        print("⬇️ Scroll down!")
                        last_gesture_time = current_time
                        cv2.putText(frame, "SCROLL DOWN", (20, 70),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                  (0, 255, 0), 2)
            
            # Draw info panel
            if show_info:
                h_frame, w_frame = frame.shape[:2]
                
                # Mode indicator
                cv2.putText(frame, "Mode: GESTURE", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # FPS
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Hand detection status
                hand_color = (0, 255, 0) if hand_detected else (0, 0, 255)
                hand_text = "Hand: DETECTED" if hand_detected else "Hand: NOT DETECTED"
                cv2.putText(frame, hand_text, (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 2)
                
                # Controls
                controls = [
                    "Controls:",
                    "q - Quit",
                    "i - Toggle info",
                    "",
                    "Gestures:",
                    "Pinch - Click",
                    "4 Fingers - Scroll"
                ]
                
                y_offset = 30
                for i, control in enumerate(controls):
                    cv2.putText(frame, control, (w_frame - 200, y_offset + i * 22), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            cv2.imshow("AI Virtual Mouse - Simple", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("\n👋 Exiting...")
                break
            elif key == ord("i"):
                show_info = not show_info
                print(f"ℹ️ Info panel: {'ON' if show_info else 'OFF'}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("✓ Application closed")


if __name__ == "__main__":
    main()
