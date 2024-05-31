import cv2
import pyautogui
import math
import time
import pygetwindow as gw
import threading
from HandTrackingModule import HandDetector 

# Initialize HandDetector
hand_detector = HandDetector()

# Open the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for previous index finger position
prev_index_tip = (0, 0)

# Video control variables
video_playing = False
media_player_title = "VLC media player"
sensitivity = 2  # Adjust as needed
distance_threshold = 20  # Adjust as needed
speed_threshold = 10  # Adjust as needed

# Lock for thread safety
lock = threading.Lock()

def hand_detection():
    global frame, video_playing
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        # Use HandDetector to find hands and landmarks
        frame_with_hands = hand_detector.find_hands(frame)

        # Check if lm_list has elements
        with lock:
            if len(hand_detector.lm_list) >= 9:
                # Get thumb and index finger positions
                thumb_tip = hand_detector.lm_list[4]
                index_tip = hand_detector.lm_list[8]

                # Calculate distance between thumb and index finger
                distance = math.hypot(index_tip[1] - thumb_tip[1], index_tip[2] - thumb_tip[2])

                # Debug output
                print(f"Thumb Tip: {thumb_tip}, Index Tip: {index_tip}, Distance: {distance}")

                # Update video_playing variable
                media_player_window = gw.getWindowsWithTitle(media_player_title)
                video_playing = bool(media_player_window)
                print(f"Video Playing: {video_playing}")

        # Display the frame with hand landmarks
        cv2.imshow('Hand Gesture Mouse Control', frame_with_hands)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def mouse_control():
    global prev_index_tip, video_playing
    while cap.isOpened():
        with lock:
            if len(hand_detector.lm_list) >= 9:
                # Get thumb and index finger positions
                thumb_tip = hand_detector.lm_list[4]
                index_tip = hand_detector.lm_list[8]

                # Calculate distance between thumb and index finger
                distance = math.hypot(index_tip[1] - thumb_tip[1], index_tip[2] - thumb_tip[2])

                # Mouse control based on thumb and index finger
                if not video_playing:
                    # Normal mouse click when no video playback
                    pyautogui.moveTo(index_tip[1] * sensitivity, index_tip[2] * sensitivity)
                    if distance < distance_threshold:
                        pyautogui.click()
                else:
                    # Calculate speed of index finger movement
                    current_index_tip = (index_tip[1], index_tip[2])
                    speed = math.hypot(current_index_tip[0] - prev_index_tip[0], current_index_tip[1] - prev_index_tip[1])

                    # Video control if a video is playing
                    if distance < distance_threshold and speed < speed_threshold:
                        # Toggle play/pause by sending space key
                        def control_video_player():
                            media_player_window = gw.getWindowsWithTitle(media_player_title)
                            if media_player_window:
                                media_player_window[0].activate()
                                pyautogui.press('space')
                                time.sleep(0.2)

                        video_control_thread = threading.Thread(target=control_video_player)
                        video_control_thread.start()

                    # Update previous index finger position
                    prev_index_tip = current_index_tip

        time.sleep(0.0)

# Start hand detection and mouse control threads
hand_detection_thread = threading.Thread(target=hand_detection)
mouse_control_thread = threading.Thread(target=mouse_control)

hand_detection_thread.start()
mouse_control_thread.start()

hand_detection_thread.join()
mouse_control_thread.join()
