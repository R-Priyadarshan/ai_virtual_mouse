
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not detected")
    exit()

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to capture frame")
        break

    frame = cv2.flip(frame, 1)
    cv2.imshow("AI Virtual Mouse - Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
