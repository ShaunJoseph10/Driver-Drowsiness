import mediapipe as mp
import cv2

from utils.constants import LEFT_EYE, RIGHT_EYE

# Initialize MediaPipe Face Mesh

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

def extract_eye_points(frame, face_landmarks):

    h, w, _ = frame.shape

    left_eye_points = []
    right_eye_points = []

    # LEFT eye
    for idx in LEFT_EYE:

        landmark = face_landmarks.landmark[idx]

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        left_eye_points.append((x, y))

    # RIGHT eye
    for idx in RIGHT_EYE:

        landmark = face_landmarks.landmark[idx]

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        right_eye_points.append((x, y))

    return left_eye_points, right_eye_points