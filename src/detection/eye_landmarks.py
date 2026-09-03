import cv2
import mediapipe as mp

# Initialize Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# Webcam
cap = cv2.VideoCapture(0)

# LEFT eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]

# RIGHT eye landmark indices
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

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

    # If landmarks detected
    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # Draw LEFT eye points
            for idx in LEFT_EYE:

                landmark = face_landmarks.landmark[idx]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Draw RIGHT eye points
            for idx in RIGHT_EYE:

                landmark = face_landmarks.landmark[idx]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

    # Show frame
    cv2.imshow("Eye Landmarks", frame)

    # Exit on Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()