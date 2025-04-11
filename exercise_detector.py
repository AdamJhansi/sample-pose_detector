import mediapipe as mp
from utils import calculate_angle

class ExerciseDetector:
    def __init__(self):
        # Push-up states and thresholds
        self.pushup_state = "up"  # "up" or "down"
        self.pushup_count = 0
        self.pushup_angle = 0
        self.pushup_threshold_up = 140  # Lebih rendah dari sebelumnya (160)
        self.pushup_threshold_down = 100  # Lebih tinggi dari sebelumnya (90)
        self.pushup_stability_threshold = 10  # Lebih toleran terhadap gerakan
        self.last_pushup_angle = 0
        
        # Squat states and thresholds
        self.squat_state = "up"  # "up" or "down"
        self.squat_count = 0
        self.squat_angle = 0
        self.squat_threshold_up = 140  # Lebih rendah dari sebelumnya (160)
        self.squat_threshold_down = 100  # Lebih tinggi dari sebelumnya (90)
        self.squat_stability_threshold = 10  # Lebih toleran terhadap gerakan
        self.last_squat_angle = 0
        
        # Stability check
        self.stable_frames = 0
        self.required_stable_frames = 3  # Lebih sedikit frame yang dibutuhkan
        
    def detect_pushup(self, landmarks):
        """Detect push-up movement and count repetitions"""
        if not landmarks:
            return 0
            
        # Get required landmarks
        left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x,
                        landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y]
        left_elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].x,
                     landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].y]
        left_wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST].x,
                     landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST].y]
        
        right_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x,
                         landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y]
        right_elbow = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].x,
                      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].y]
        right_wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].x,
                      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].y]
        
        # Calculate angles for both arms
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Use average angle of both arms
        self.pushup_angle = (left_angle + right_angle) / 2
        
        # Check if body is in proper push-up position
        left_hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP].x,
                   landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP].y]
        right_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP].x,
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP].y]
        
        # Calculate body angle to ensure proper form
        body_angle = calculate_angle(left_shoulder, left_hip, right_hip)
        
        # Lebih toleran terhadap posisi tubuh (dalam 20 derajat)
        if abs(body_angle - 180) > 20:
            return self.pushup_angle
        
        # Check for stable movement
        angle_change = abs(self.pushup_angle - self.last_pushup_angle)
        if angle_change < self.pushup_stability_threshold:
            self.stable_frames += 1
        else:
            self.stable_frames = 0
        
        # Update state and count if movement is stable
        if self.stable_frames >= self.required_stable_frames:
            if self.pushup_state == "up" and self.pushup_angle < self.pushup_threshold_down:
                self.pushup_state = "down"
            elif self.pushup_state == "down" and self.pushup_angle > self.pushup_threshold_up:
                self.pushup_state = "up"
                self.pushup_count += 1
        
        self.last_pushup_angle = self.pushup_angle
        return self.pushup_angle
        
    def detect_squat(self, landmarks):
        """Detect squat movement and count repetitions"""
        if not landmarks:
            return 0
            
        # Get required landmarks
        left_hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP].x,
                   landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP].y]
        left_knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE].x,
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE].y]
        left_ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE].x,
                     landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE].y]
        
        right_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP].x,
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP].y]
        right_knee = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE].x,
                     landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE].y]
        right_ankle = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE].x,
                      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE].y]
        
        # Calculate angles for both legs
        left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_angle = calculate_angle(right_hip, right_knee, right_ankle)
        
        # Use average angle of both legs
        self.squat_angle = (left_angle + right_angle) / 2
        
        # Check if body is in proper squat position
        left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x,
                        landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y]
        right_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x,
                         landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y]
        
        # Calculate body angle to ensure proper form
        body_angle = calculate_angle(left_shoulder, left_hip, right_hip)
        
        # Lebih toleran terhadap posisi tubuh (dalam 30 derajat)
        if abs(body_angle - 180) > 30:
            return self.squat_angle
        
        # Check for stable movement
        angle_change = abs(self.squat_angle - self.last_squat_angle)
        if angle_change < self.squat_stability_threshold:
            self.stable_frames += 1
        else:
            self.stable_frames = 0
        
        # Update state and count if movement is stable
        if self.stable_frames >= self.required_stable_frames:
            if self.squat_state == "up" and self.squat_angle < self.squat_threshold_down:
                self.squat_state = "down"
            elif self.squat_state == "down" and self.squat_angle > self.squat_threshold_up:
                self.squat_state = "up"
                self.squat_count += 1
        
        self.last_squat_angle = self.squat_angle
        return self.squat_angle
        
    def reset_counts(self):
        """Reset all counts and states"""
        self.pushup_count = 0
        self.squat_count = 0
        self.pushup_state = "up"
        self.squat_state = "up"
        self.stable_frames = 0
        
    def get_counts(self):
        """Get current counts for both exercises"""
        return self.pushup_count, self.squat_count 