import cv2
import time
import numpy as np
from pose_detector import PoseDetector
from exercise_detector import ExerciseDetector
from utils import draw_button, is_button_clicked

def main():
    # Initialize components
    pose_detector = PoseDetector()
    exercise_detector = ExerciseDetector()
    
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Initialize FPS calculation
    prev_time = 0
    fps = 0
    
    # Create window and set mouse callback
    cv2.namedWindow('Pose Detection')
    
    # Flag to track if close button was clicked
    close_clicked = False
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal close_clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            if is_button_clicked(x, y, (param.shape[1] - 100, 20), (80, 30)):
                close_clicked = True
    
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Mirror the frame horizontally
        frame = cv2.flip(frame, 1)
        
        # Set mouse callback with current frame
        cv2.setMouseCallback('Pose Detection', mouse_callback, frame)
        
        # Process frame for pose detection
        results = pose_detector.process_frame(frame)
        
        # Create overlay for information display
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (300, 250), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Draw landmarks and detect exercises if pose is detected
        if results.pose_landmarks:
            # Draw landmarks
            pose_detector.draw_landmarks(frame, results.pose_landmarks)
            
            # Detect exercises
            pushup_angle = exercise_detector.detect_pushup(results.pose_landmarks.landmark)
            squat_angle = exercise_detector.detect_squat(results.pose_landmarks.landmark)
            
            # Get counts
            pushup_count, squat_count = exercise_detector.get_counts()
            
            # Display information with better formatting
            # Push-up information
            cv2.putText(frame, "Push-up Counter", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Count: {pushup_count}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {int(pushup_angle)}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Squat information
            cv2.putText(frame, "Squat Counter", (10, 130), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Count: {squat_count}", (10, 160), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {int(squat_angle)}", (10, 190), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Status information
            status_color = (0, 255, 0)  # Green for good detection
            status_text = "Pose Detected"
        else:
            status_color = (0, 0, 255)  # Red for no detection
            status_text = "No Pose Detected"
        
        # Display status
        cv2.putText(frame, status_text, (10, 220), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 250), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw close button with better styling
        button_text = "Exit (Q)"
        button_pos = (frame.shape[1] - 100, 20)
        button_size = (80, 30)
        
        # Draw button background
        cv2.rectangle(frame, button_pos, 
                     (button_pos[0] + button_size[0], button_pos[1] + button_size[1]),
                     (0, 0, 255), -1)
        
        # Draw button border
        cv2.rectangle(frame, button_pos, 
                     (button_pos[0] + button_size[0], button_pos[1] + button_size[1]),
                     (255, 255, 255), 2)
        
        # Add text to button
        text_size = cv2.getTextSize(button_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = button_pos[0] + (button_size[0] - text_size[0]) // 2
        text_y = button_pos[1] + (button_size[1] + text_size[1]) // 2
        cv2.putText(frame, button_text, (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display frame
        cv2.imshow('Pose Detection', frame)
        
        # Check for key presses or close button click
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or close_clicked:
            break
        elif key == ord('r'):
            exercise_detector.reset_counts()
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pose_detector.close()

if __name__ == "__main__":
    main() 