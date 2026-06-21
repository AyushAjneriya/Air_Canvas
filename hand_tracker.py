import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

class HandTracker:
    def __init__(self, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Initializes the HandTracker using the modern MediaPipe Tasks API (compatible with Python 3.12).
        Downloads the required 'hand_landmarker.task' asset file if not present locally.
        """
        # Resolve target model path inside the same directory as this file
        model_filename = "hand_landmarker.task"
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), model_filename)

        # Download model from Google storage if missing
        if not os.path.exists(self.model_path):
            print("MediaPipe Hand Landmarker model file is missing.")
            print("Downloading 'hand_landmarker.task' from Google CDN, please wait...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("Model downloaded successfully!")
            except Exception as e:
                print(f"Error downloading the model file: {e}")
                raise e

        # Initialize the modern HandLandmarker detector
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_tracking_confidence
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Runs hand landmarker detection and draws the joint skeleton overlay on the image.
        """
        h, w, c = img.shape
        # Tasks API requires an mp.Image object created from RGB data
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run hand detection
        self.results = self.detector.detect(mp_image)

        # Draw the hand skeletal joints and connections using OpenCV
        if draw and self.results.hand_landmarks:
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),          # Thumb
                (5, 6), (6, 7), (7, 8),                  # Index
                (9, 10), (10, 11), (11, 12),             # Middle
                (13, 14), (14, 15), (15, 16),            # Ring
                (17, 18), (18, 19), (19, 20),            # Pinky
                (0, 5), (5, 9), (9, 13), (13, 17), (0, 17) # Palm
            ]
            for hand_lms in self.results.hand_landmarks:
                # Draw connection lines (BGR Red)
                for conn in connections:
                    pt1_norm = hand_lms[conn[0]]
                    pt2_norm = hand_lms[conn[1]]
                    pt1 = (int(pt1_norm.x * w), int(pt1_norm.y * h))
                    pt2 = (int(pt2_norm.x * w), int(pt2_norm.y * h))
                    cv2.line(img, pt1, pt2, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Draw joint points (BGR Green)
                for lm in hand_lms:
                    pt = (int(lm.x * w), int(lm.y * h))
                    cv2.circle(img, pt, 4, (0, 255, 0), cv2.FILLED, cv2.LINE_AA)
        
        return img

    def get_landmarks_and_tips(self, frame_width, frame_height):
        """
        Extracts landmarks list, and scaled pixel coordinates for index and middle fingertips.
        """
        landmarks = []
        index_tip = None
        middle_tip = None

        if self.results and self.results.hand_landmarks and len(self.results.hand_landmarks) > 0:
            hand_lms = self.results.hand_landmarks[0]
            landmarks = hand_lms

            # Index tip (8)
            index_lm = hand_lms[8]
            index_tip = (int(index_lm.x * frame_width), int(index_lm.y * frame_height))

            # Middle tip (12)
            middle_lm = hand_lms[12]
            middle_tip = (int(middle_lm.x * frame_width), int(middle_lm.y * frame_height))

        return landmarks, index_tip, middle_tip
