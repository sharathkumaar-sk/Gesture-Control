import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=2, min_detection_con=0.5, min_track_con=0.5):
        self.max_hands = max_hands
        self.min_detection_con = min_detection_con
        self.min_track_con = min_track_con
        self.prev_index_tip = [0, 0]
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_hands,
            min_detection_confidence=self.min_detection_con,
            min_tracking_confidence=self.min_track_con,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.lm_list = []  # Add an empty list to store landmarks

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1),
                    connection_drawing_spec=self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1)
                )
                self.find_position(img, hand_landmarks)  # Store landmarks

        return img

    def find_position(self, img, hand_landmarks=None, draw=True):
        lm_list = []
        if hand_landmarks is not None:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.prev_index_tip = [cx, cy]
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

            self.lm_list = lm_list  # Store landmarks as an attribute

        return lm_list

    def find_distance(self, p1, p2, img, draw=True):
        lm_list = self.find_position(img, draw=False)  # Get hand landmarks using find_position
        x1, y1 = lm_list[p1][1], lm_list[p1][2]
        x2, y2 = lm_list[p2][1], lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def fingers_up(self):
        fingers = [0, 0, 0, 0, 0]

        # Thumb
        if self.lm_list[4][1] < self.lm_list[3][1]:
            fingers[0] = 1

        # 4 Fingers
        for id in range(1, 5):
            if self.lm_list[4 * id][2] < self.lm_list[4 * id - 2][2]:
                fingers[id] = 1

        return fingers
