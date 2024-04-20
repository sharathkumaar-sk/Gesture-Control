# Gesture-Control


## Purpose

This project provides a virtual mouse controlled by hand gestures, offering hands-free interaction with your computer. It offers essential mouse functions like cursor movement, clicking, and even video playback control in VLC media player.
<p align="center">
  <img src="https://github.com/sharathkumaar-sk/Gesture_Control/assets/163333516/797b6014-1871-47b2-85fa-bb6087ccd808" width="400" height="300" />
  <img src="https://github.com/sharathkumaar-sk/Gesture_Control/assets/163333516/d6181ab2-e5c7-4ea7-b5e2-24e9a575aa90" width="400" height="300" />
</p>

## Key Features

- **Hand Detection and Landmark Tracking:** Utilizes the MediaPipe library for real-time hand detection and landmark tracking, ensuring accurate gesture recognition.
- **Mouse Control:** Maps hand gestures to intuitive mouse actions:
  - Index finger position controls cursor movement.
  - Distance between thumb and index finger triggers clicks.
- **Video Control Integration:** Detects VLC media player window and enables play/pause control using a specific hand gesture.
- **Visual Feedback:** Displays the webcam feed with hand landmarks for improved user experience and debugging.

## Code Structure

- **HandTrackingModule.py:** Encapsulates hand detection and landmark processing logic.
- **main.py:**
  - Initializes HandTrackingModule, webcam, and necessary variables.
  - Continuously reads frames from the webcam.
  - Detects hands and landmarks using HandTrackingModule.
  - Implements mouse control logic based on hand gestures.
  - Checks for VLC media player window and enables video control if present.
  - Displays the frame with hand landmarks for visualization.
  - Exits on 'Esc' key press.

## Libraries Used

- **OpenCV (cv2):** Real-time image processing and computer vision.
- **MediaPipe:** Hand detection and tracking.
- **pyautogui:** Simulating mouse and keyboard actions.
- **pygetwindow:** Detecting and interacting with windows.
- **math:** Mathematical calculations (e.g., distance, speed).
- **time:** Time-related functions (e.g., pausing execution).

  

https://github.com/sharathkumaar-sk/Gesture-Control/assets/163333516/0fbd578f-1d3b-4a80-a122-faf8c118bfac

## Getting Started

### Install Required Libraries

```bash
pip install opencv-python mediapipe pyautogui pygetwindow
```

## Download the Project

Clone this repository or download the zip file.

```bash
git clone [https://github.com/sharathkumaar-sk/Gesture-Control.git]
```

## Run the Script

```bash
python main.py
```
Execute the main code That will launch the real-time interface for controlling using your webcam.

**Contributing:**

We welcome contributions! Please feel free to submit pull requests or open issues for any enhancements or bug fixes.

**License:**

This project is licensed under the MIT License. See the LICENSE file for details.
