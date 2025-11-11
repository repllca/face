import cv2 as cv
import mediapipe as mp

class LipDetector:
    def __init__(self, camera_index=0):
        self.cap = cv.VideoCapture(camera_index)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_lip_open_ratio(self):
        success, frame = self.cap.read()
        if not success:
            return None

        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0]
        top = landmarks.landmark[13]
        bottom = landmarks.landmark[14]
        return abs(top.y - bottom.y)

    def release(self):
        self.cap.release()
