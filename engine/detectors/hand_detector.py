import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        detections = []

        if not results.multi_hand_landmarks:
            return detections

        h, w, _ = frame.shape

        for hand_landmarks in results.multi_hand_landmarks:
            xs = [lm.x for lm in hand_landmarks.landmark]
            ys = [lm.y for lm in hand_landmarks.landmark]

            x1, y1 = int(min(xs) * w), int(min(ys) * h)
            x2, y2 = int(max(xs) * w), int(max(ys) * h)

            detections.append({
                "label": "hand",
                "confidence": 1.0,
                "bbox": (x1, y1, x2, y2),
                "center": (
                    (x1 + x2) // 2,
                    (y1 + y2) // 2
                )
            })

        return detections
