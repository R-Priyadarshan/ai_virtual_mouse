
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

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

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

        # Active movement area
        cv2.rectangle(
            frame,
            (FRAME_MARGIN, FRAME_MARGIN),
            (w - FRAME_MARGIN, h - FRAME_MARGIN),
            (255, 0, 255),
            2
        )

        if results.multi_hand_landmarks:
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
            target_x = (ix - FRAME_MARGIN) / (
                w - 2 * FRAME_MARGIN
            ) * SCREEN_W

            target_y = (iy - FRAME_MARGIN) / (
                h - 2 * FRAME_MARGIN
            ) * SCREEN_H

            target_x = max(0, min(SCREEN_W - 1, target_x))
            target_y = max(0, min(SCREEN_H - 1, target_y))

            # Smooth cursor movement
            curr_x = prev_x + (target_x - prev_x) / SMOOTHING
            curr_y = prev_y + (target_y - prev_y) / SMOOTHING

            pyautogui.moveTo(int(curr_x), int(curr_y))
            prev_x, prev_y = curr_x, curr_y

            # Thumb-index pinch distance
            distance = math.hypot(ix - tx, iy - ty)

            cv2.circle(frame, (ix, iy), 8, (0, 255, 0), -1)
            cv2.circle(frame, (tx, ty), 8, (255, 0, 0), -1)
            cv2.line(frame, (ix, iy), (tx, ty), (0, 255, 255), 2)

            if distance < CLICK_THRESHOLD:
                cv2.putText(
                    frame, "PINCH DETECTED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 255), 2
                )

                now = time.monotonic()

                if now - last_click > CLICK_COOLDOWN:
                    pyautogui.click()
                    last_click = now

        cv2.imshow("AI Virtual Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
