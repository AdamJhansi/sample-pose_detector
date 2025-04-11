import cv2
import time
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
        
        # Draw landmarks and detect exercises if pose is detected
        if results.pose_landmarks:
            # Draw landmarks
            pose_detector.draw_landmarks(frame, results.pose_landmarks)
            
            # Detect exercises
            pushup_angle = exercise_detector.detect_pushup(results.pose_landmarks.landmark)
            squat_angle = exercise_detector.detect_squat(results.pose_landmarks.landmark)
            
            # Get counts
            pushup_count, squat_count = exercise_detector.get_counts()
            
            # Display information
            cv2.putText(frame, f"Push-ups: {pushup_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Squats: {squat_count}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Push-up Angle: {int(pushup_angle)}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Squat Angle: {int(squat_angle)}", (10, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 190), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw close button
        draw_button(frame, "Close (Q)", (frame.shape[1] - 100, 20), (80, 30), (0, 0, 255))
        
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