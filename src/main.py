import cv2
import time
import csv
import os
import sys

from detection.head_pose import (
    get_head_pose
)

from datetime import datetime

from detection.eye_detector import (
    face_mesh,
    extract_eye_points
)

from detection.yawn_detector import (
    calculate_mar
)

from utils.ear import calculate_ear

from utils.constants import (
    EAR_THRESHOLD,
    CLOSED_EYES_FRAMES,
    BLINK_THRESHOLD
)

from utils.alarm import (
    start_alarm_thread,
    stop_alarm
)

            

# Open webcam
cap = cv2.VideoCapture(0)

cv2.namedWindow("Driver Drowsiness Detection System")

exit_button = None
exit_clicked = False


def mouse_callback(event, x, y, flags, param):

    global exit_clicked, exit_button

    if event == cv2.EVENT_LBUTTONDOWN:

        if exit_button is not None:

            x1, y1, x2, y2 = exit_button

            if x1 <= x <= x2 and y1 <= y <= y2:
                exit_clicked = True


cv2.setMouseCallback(
    "Driver Drowsiness Detection System",
    mouse_callback
)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Counters
frame_counter = 0
blink_count = 0
blink_detected = False

# Yawn Counters
yawn_count = 0
yawn_frames = 0

MAR_THRESHOLD = 0.40
YAWN_FRAMES = 15

# Screenshot control
last_capture_time = 0

# Log control
last_log_time = 0

# -----------------------------
# Log Folder (Works in EXE)
# -----------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(logs_dir, "drowsiness_log.csv")

# Create log file
if not os.path.exists(log_file):

    with open(
        log_file,
        mode="w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Timestamp",
                "EAR",
                "Event"
            ]
        )

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Mirror frame
    frame = cv2.flip(frame, 1)

    # RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Face Mesh
    results = face_mesh.process(
        rgb_frame
    )

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # Eyes
            left_eye_points, right_eye_points = extract_eye_points(
                frame,
                face_landmarks
            )

            # EAR
            left_ear = calculate_ear(
                left_eye_points
            )

            right_ear = calculate_ear(
                right_eye_points
            )

            avg_ear = (
                left_ear + right_ear
            ) / 2

            # Frame size
            frame_height, frame_width = frame.shape[:2]

            # MAR
            mar = calculate_mar(
                face_landmarks.landmark,
                frame_width,
                frame_height
            )

            # Head Pose
            head_direction = get_head_pose(
                face_landmarks,
                frame_width,
                frame_height
            )


            # Blink Detection
            if avg_ear < BLINK_THRESHOLD:

                blink_detected = True

            else:

                if blink_detected:

                    blink_count += 1
                    blink_detected = False

            # Yawn Detection
            if mar > MAR_THRESHOLD:

                yawn_frames += 1

            else:

                if yawn_frames >= YAWN_FRAMES:

                    yawn_count += 1

                    with open(
                        log_file,
                        mode="a",
                        newline=""
                    ) as file:

                        writer = csv.writer(file)

                        writer.writerow(
                            [
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                round(avg_ear, 3),
                                "Yawn Detected"
                            ]
                        )

                    print(
                        f"Yawn Detected | Total: {yawn_count}"
                    )

                yawn_frames = 0

            # Drowsiness Detection
            if avg_ear < EAR_THRESHOLD:

                frame_counter += 1

            else:

                frame_counter = 0
                stop_alarm()

            # EAR Display
            cv2.putText(
                frame,
                f"EAR: {avg_ear:.2f}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Blink Display
            cv2.putText(
                frame,
                f"Blinks: {blink_count}",
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

            # Yawn Count Display
            cv2.putText(
                frame,
                f"Yawns: {yawn_count}",
                (30, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            # Drowsiness Alert
            if frame_counter >= CLOSED_EYES_FRAMES:

                cv2.putText(
                    frame,
                    "DROWSINESS DETECTED!",
                    (80, 300),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                start_alarm_thread()

                current_time = time.time()

                if current_time - last_capture_time > 5:

                    # Create screenshots folder (works in EXE too)
                    screenshots_dir = os.path.join(BASE_DIR, "screenshots")
                    os.makedirs(screenshots_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                    filename = os.path.join(
                        screenshots_dir,
                        f"drowsy_{timestamp}.jpg"
                    )

                    cv2.imwrite(filename, frame)

                    print(f"Screenshot Saved: {filename}")

                    last_capture_time = current_time

                if current_time - last_log_time > 5:

                    with open(
                        log_file,
                        mode="a",
                        newline=""
                    ) as file:

                        writer = csv.writer(file)

                        writer.writerow(
                            [
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                round(avg_ear, 3),
                                "Drowsiness Detected"
                            ]
                        )

                    print("Event Logged")

                    last_log_time = current_time


    frame = cv2.resize(frame, (1280, 720))

    # Exit Button

    button_width = 220
    button_height = 55

    x1 = (frame.shape[1] - button_width) // 2
    y1 = frame.shape[0] - 80

    x2 = x1 + button_width
    y2 = y1 + button_height
    exit_button = (x1, y1, x2, y2)

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 0, 255),
        -1
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (255,255,255),
        2
    )

    text = "EXIT MONITORING"

    size = cv2.getTextSize(
        text,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        2
    )[0]

    text_x = x1 + (button_width - size[0]) // 2
    text_y = y1 + (button_height + size[1]) // 2

    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.imshow(
        "Driver Drowsiness Detection System",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or exit_clicked:
        break

cap.release()
cv2.destroyAllWindows()