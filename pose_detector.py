import cv2
import mediapipe as mp
import time
import math
import numpy as np

class PoseDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        """Process a frame and return the results"""
        # Convert the BGR image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect poses
        results = self.pose.process(image)
        
        return results

    def draw_landmarks(self, image, landmarks):
        """Draw pose landmarks on the image"""
        if landmarks:
            self.mp_draw.draw_landmarks(
                image,
                landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        return image

    def close(self):
        """Close the pose detector"""
        self.pose.close()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Exercise states
PUSHUP_STATE = "none"  # none, up, down
SQUAT_STATE = "none"   # none, up, down
PUSHUP_COUNT = 0
SQUAT_COUNT = 0

def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def draw_button(frame, text, position, size=(100, 30), color=(0, 0, 255)):
    """Draw a button on the frame"""
    x, y = position
    w, h = size
    # Draw button background
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
    # Draw button border
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
    # Add text
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, (255, 255, 255), 2)

def detect_pushup(landmarks):
    """Detect push-up position"""
    global PUSHUP_STATE, PUSHUP_COUNT
    
    # Get relevant landmarks
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    
    # Calculate angle
    angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    
    # Check push-up state
    if angle > 160:
        PUSHUP_STATE = "up"
    elif angle < 90 and PUSHUP_STATE == "up":
        PUSHUP_STATE = "down"
        PUSHUP_COUNT += 1
    
    return angle

def detect_squat(landmarks):
    """Detect squat position"""
    global SQUAT_STATE, SQUAT_COUNT
    
    # Get relevant landmarks
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    
    # Calculate angle
    angle = calculate_angle(left_hip, left_knee, left_ankle)
    
    # Check squat state
    if angle > 160:
        SQUAT_STATE = "up"
    elif angle < 90 and SQUAT_STATE == "up":
        SQUAT_STATE = "down"
        SQUAT_COUNT += 1
    
    return angle

def main():
    prev_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Mirror the frame horizontally
        frame = cv2.flip(frame, 1)
            
        # Process the image and detect poses
        results = pose_detector.process_frame(frame)
        
        # Draw pose landmarks and detect exercises
        image = pose_detector.draw_landmarks(frame, results.pose_landmarks)
        
        # Detect exercises
        pushup_angle = detect_pushup(results.pose_landmarks.landmark)
        squat_angle = detect_squat(results.pose_landmarks.landmark)
        
        # Display exercise information
        cv2.putText(image, f'Push-ups: {PUSHUP_COUNT}', (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f'Squats: {SQUAT_COUNT}', (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f'Push-up Angle: {int(pushup_angle)}', (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f'Squat Angle: {int(squat_angle)}', (10, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Calculate and display FPS
        current_time = time.time()
        fps = 1.0 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(image, f'FPS: {int(fps)}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw close button
        draw_button(image, "Close (Q)", (image.shape[1] - 120, 10))
        
        # Display frame
        cv2.imshow('Exercise Detection', image)
        
        # Handle keyboard events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):  # Reset counters
            PUSHUP_COUNT = 0
            SQUAT_COUNT = 0
    
    cap.release()
    cv2.destroyAllWindows()
    pose_detector.close()

if __name__ == '__main__':
    pose_detector = PoseDetector()
    main() 