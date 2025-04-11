import cv2
import numpy as np

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

def is_button_clicked(x, y, position, size):
    """Check if a point (x,y) is inside a button"""
    button_x, button_y = position
    button_w, button_h = size
    return (button_x <= x <= button_x + button_w and 
            button_y <= y <= button_y + button_h) 