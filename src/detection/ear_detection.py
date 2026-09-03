import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance

# Initialize Face Mesh
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# LEFT eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]

# RIGHT eye landmark indices
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Function to calculate EAR
def calculate_ear(eye_points):

    # Vertical distances
    vertical_1 = distance.euclidean(eye_points[1], eye_points[5])
    vertical_2 = distance.euclidean(eye_points[2], eye_points[4])

    # Horizontal distance
    horizontal = distance.euclidean(eye_points[0], eye_points[3])

    # EAR formula
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

    return ear

# Open webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Flip frame
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            left_eye_points = []
            right_eye_points = []

            # LEFT eye points
            for idx in LEFT_EYE:

                landmark = face_landmarks.landmark[idx]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                left_eye_points.append((x, y))

                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # RIGHT eye points
            for idx in RIGHT_EYE:

                landmark = face_landmarks.landmark[idx]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                right_eye_points.append((x, y))

                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

            # Calculate EAR
            left_ear = calculate_ear(left_eye_points)
            right_ear = calculate_ear(right_eye_points)

            avg_ear = (left_ear + right_ear) / 2

            # Display EAR
            cv2.putText(
                frame,
                f"EAR: {avg_ear:.2f}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    # Show frame
    cv2.imshow("EAR Detection", frame)

    # Quit on Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()