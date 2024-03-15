import cv2
import pyautogui
from HandTrackingModule import HandDetector
import math
import time
import pygetwindow as gw

# Initialize HandDetector
hand_detector = HandDetector()

# Open the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for previous index finger position
prev_index_tip = (0, 0)

# Video control variables
video_playing = False
media_player_title = "VLC media player"

while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Use HandDetector to find hands and landmarks
    frame_with_hands = hand_detector.find_hands(frame)

    # Check if lm_list has elements
    if len(hand_detector.lm_list) >= 9:
        # Get thumb and index finger positions
        thumb_tip = hand_detector.lm_list[4]
        index_tip = hand_detector.lm_list[8]

        # Calculate distance between thumb and index finger
        distance = math.hypot(index_tip[1] - thumb_tip[1], index_tip[2] - thumb_tip[2])

        # Mouse control based on thumb and index finger
        sensitivity = 2  # Adjust as needed
        if not video_playing:
            # Normal mouse click when no video playback
            pyautogui.moveTo(index_tip[1] * sensitivity, index_tip[2] * sensitivity)
            if distance < 20:
                pyautogui.click()
        else:
            # Calculate speed of index finger movement
            speed_threshold = 10  # Adjust as needed
            current_index_tip = (index_tip[1], index_tip[2])
            speed = math.hypot(current_index_tip[0] - prev_index_tip[0], current_index_tip[1] - prev_index_tip[1])

            # Video control if a video is playing
            if distance < 20 and speed < speed_threshold:
                # Toggle play/pause by sending space key
                media_player_window[0].activate()
                pyautogui.press('space')
                time.sleep(0.2)
            # Update previous index finger position
            prev_index_tip = current_index_tip

    # Display the frame with hand landmarks
    cv2.imshow('Hand Gesture Mouse Control', frame_with_hands)

    # Check if VLC media player window is present
    media_player_window = gw.getWindowsWithTitle(media_player_title)
    if media_player_window:
        video_playing = True
    else:
        video_playing = False

    # Exit when 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
