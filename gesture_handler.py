"""
Gesture Recognition Module
Handles various hand gestures like pinch, double-click, drag, etc.
"""

import math
import time


class GestureHandler:
    def __init__(self, click_threshold=30, double_click_time=0.3):
        self.click_threshold = click_threshold
        self.double_click_time = double_click_time
        
        self.last_click_time = 0.0
        self.pinch_start_time = 0.0
        self.is_pinching = False
        self.pinch_start_pos = (0, 0)
        
        # For tracking gesture state
        self.last_gesture = None
        self.gesture_cooldown = 0.3
        self.last_gesture_time = 0.0
    
    def get_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])
    
    def detect_pinch(self, thumb_pos, index_pos):
        """Detect if thumb and index finger are pinching"""
        distance = self.get_distance(thumb_pos, index_pos)
        return distance < self.click_threshold, distance
    
    def detect_double_click(self):
        """Detect if two pinches happened within double_click_time"""
        current_time = time.monotonic()
        time_since_last = current_time - self.last_click_time
        
        if time_since_last < self.double_click_time:
            return True
        return False
    
    def detect_drag(self, thumb_pos, index_pos, current_pos):
        """Detect drag gesture (pinch + movement)"""
        is_pinching, distance = self.detect_pinch(thumb_pos, index_pos)
        
        if is_pinching and not self.is_pinching:
            # Start of pinch
            self.pinch_start_time = time.monotonic()
            self.pinch_start_pos = current_pos
            self.is_pinching = True
            return "drag_start", current_pos
        
        elif is_pinching and self.is_pinching:
            # During pinch - check if movement
            movement_distance = self.get_distance(self.pinch_start_pos, current_pos)
            if movement_distance > 20:  # Minimum movement threshold
                return "dragging", current_pos
            return None, None
        
        elif not is_pinching and self.is_pinching:
            # End of pinch
            self.is_pinching = False
            return "drag_end", current_pos
        
        return None, None
    
    def detect_scroll_gesture(self, hand_landmarks, frame_height):
        """Detect scroll gesture based on hand orientation"""
        # Get wrist and middle finger positions
        wrist = hand_landmarks[0]
        middle_finger_tip = hand_landmarks[12]
        
        # Calculate vertical distance
        vertical_distance = wrist.y - middle_finger_tip.y
        
        if vertical_distance > 0.15:  # Hand pointing up
            return "scroll_up"
        elif vertical_distance < -0.15:  # Hand pointing down
            return "scroll_down"
        
        return None
    
    def detect_right_click_gesture(self, thumb_pos, index_pos, middle_pos):
        """Detect right-click gesture (index and middle fingers together, thumb extended)"""
        index_middle_dist = self.get_distance(index_pos, middle_pos)
        thumb_index_dist = self.get_distance(thumb_pos, index_pos)
        
        # If index and middle are close, but thumb is far, it's right-click
        if index_middle_dist < self.click_threshold and thumb_index_dist > self.click_threshold * 2:
            return True
        return False
    
    def detect_peace_sign(self, hand_landmarks):
        """Detect peace sign (index and middle extended, other fingers folded)"""
        # Get finger tips
        index_tip = hand_landmarks[8]
        middle_tip = hand_landmarks[12]
        ring_tip = hand_landmarks[16]
        pinky_tip = hand_landmarks[20]
        
        # Get base of fingers
        index_base = hand_landmarks[6]
        middle_base = hand_landmarks[10]
        ring_base = hand_landmarks[14]
        pinky_base = hand_landmarks[18]
        
        # Check if index and middle are extended
        index_extended = index_tip.y < index_base.y - 0.1
        middle_extended = middle_tip.y < middle_base.y - 0.1
        
        # Check if ring and pinky are folded
        ring_folded = ring_tip.y > ring_base.y - 0.05
        pinky_folded = pinky_tip.y > pinky_base.y - 0.05
        
        if index_extended and middle_extended and ring_folded and pinky_folded:
            return True
        return False
    
    def detect_ok_sign(self, thumb_pos, index_pos, hand_landmarks):
        """Detect OK sign (thumb and index touching, other fingers extended)"""
        thumb_index_dist = self.get_distance(thumb_pos, index_pos)
        
        # Thumb and index should be close
        if thumb_index_dist < 40:
            # Check if other fingers are extended
            middle_tip = hand_landmarks[12]
            middle_base = hand_landmarks[10]
            
            if middle_tip.y < middle_base.y - 0.1:
                return True
        
        return False
    
    def get_gesture(self, thumb_pos, index_pos, hand_landmarks, current_pos):
        """Main gesture detection method"""
        current_time = time.monotonic()
        
        # Check cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Check for pinch (click)
        is_pinching, distance = self.detect_pinch(thumb_pos, index_pos)
        
        if is_pinching:
            if self.detect_double_click():
                self.last_gesture_time = current_time
                self.last_click_time = 0.0  # Reset for next double-click
                return "double_click"
            else:
                self.last_click_time = current_time
                self.last_gesture_time = current_time
                return "click"
        
        # Check for right-click
        if self.detect_right_click_gesture(thumb_pos, index_pos, 
                                          (int(hand_landmarks[12].x * 1000), 
                                           int(hand_landmarks[12].y * 1000))):
            self.last_gesture_time = current_time
            return "right_click"
        
        # Check for peace sign (scroll up)
        if self.detect_peace_sign(hand_landmarks):
            self.last_gesture_time = current_time
            return "peace_sign"
        
        # Check for OK sign
        if self.detect_ok_sign(thumb_pos, index_pos, hand_landmarks):
            self.last_gesture_time = current_time
            return "ok_sign"
        
        return None
