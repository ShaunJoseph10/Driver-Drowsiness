import os
import cv2
import csv
import time
import base64
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, jsonify

import mediapipe as mp
from src.detection.eye_detector import extract_eye_points
from src.detection.yawn_detector import calculate_mar
from src.detection.head_pose import get_head_pose
from src.utils.ear import calculate_ear
from src.utils.s3_uploader import upload_file_to_s3

app = Flask(__name__)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

EAR_THRESHOLD = 0.20
BLINK_THRESHOLD = 0.20
CLOSED_EYES_FRAMES = 5  # ~0.8s eyes closed in web stream

MAR_THRESHOLD = 0.40
YAWN_FRAMES = 4        # ~0.6s open mouth in web stream

# Global Session State
state = {
    "frame_counter": 0,
    "blink_count": 0,
    "blink_detected": False,
    "yawn_count": 0,
    "yawn_frames": 0,
    "status": "ACTIVE & ALERT",
    "head_direction": "CENTER",
    "last_capture_time": 0,
    "last_log_time": 0,
    "logs": []
}

logs_dir = "logs"
screenshots_dir = "screenshots"
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(screenshots_dir, exist_ok=True)

log_file = os.path.join(logs_dir, "drowsiness_log.csv")
if not os.path.exists(log_file):
    with open(log_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "EAR", "Event"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_frame", methods=["POST"])
def process_frame():
    try:
        data = request.json
        image_data = data.get("image")
        if not image_data:
            return jsonify({"error": "No image data"}), 400

        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid frame"}), 400

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        avg_ear = 0.0
        mar = 0.0
        drowsy_alert = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_points, right_eye_points = extract_eye_points(frame, face_landmarks)
                left_ear = calculate_ear(left_eye_points)
                right_ear = calculate_ear(right_eye_points)
                avg_ear = (left_ear + right_ear) / 2.0

                mar = calculate_mar(face_landmarks.landmark, w, h)
                state["head_direction"] = get_head_pose(face_landmarks, w, h)

                # --- 1. EYE CLOSURE, BLINK & DROWSINESS LOGIC ---
                if avg_ear < EAR_THRESHOLD:
                    state["frame_counter"] += 1
                else:
                    # If eyes were closed for short duration (1 to 4 frames), count as a normal BLINK
                    if 1 <= state["frame_counter"] < CLOSED_EYES_FRAMES:
                        state["blink_count"] += 1
                    state["frame_counter"] = 0
                    state["status"] = "ACTIVE & ALERT"

                # --- 2. YAWN DETECTION ---
                if mar > MAR_THRESHOLD:
                    state["yawn_frames"] += 1
                else:
                    if state["yawn_frames"] >= YAWN_FRAMES:
                        state["yawn_count"] += 1
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Log Yawn Event locally
                        with open(log_file, mode="a", newline="") as f:
                            csv.writer(f).writerow([timestamp, round(avg_ear, 3), "Yawn Detected"])
                        
                        # Sync Log to AWS S3
                        upload_file_to_s3(log_file, "logs/drowsiness_log.csv")
                        state["logs"].append({"timestamp": timestamp, "ear": round(avg_ear, 3), "event": "Yawn Detected"})
                    state["yawn_frames"] = 0

                # --- 3. DROWSINESS ALERT (5+ consecutive frames of closed eyes) ---
                if state["frame_counter"] >= CLOSED_EYES_FRAMES:
                    drowsy_alert = True
                    state["status"] = "DROWSY DETECTED!"
                    current_time = time.time()

                    # Save Screenshot & Upload to AWS S3 every 5s during alert
                    if current_time - state["last_capture_time"] > 5:
                        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"drowsy_{timestamp_str}.jpg"
                        filepath = os.path.join(screenshots_dir, filename)
                        cv2.imwrite(filepath, frame)
                        upload_file_to_s3(filepath, f"screenshots/{filename}")
                        state["last_capture_time"] = current_time

                    # Log Drowsiness Event to CSV & AWS S3
                    if current_time - state["last_log_time"] > 5:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        with open(log_file, mode="a", newline="") as f:
                            csv.writer(f).writerow([timestamp, round(avg_ear, 3), "Drowsiness Detected"])
                        upload_file_to_s3(log_file, "logs/drowsiness_log.csv")
                        state["logs"].append({"timestamp": timestamp, "ear": round(avg_ear, 3), "event": "Drowsiness Detected"})
                        state["last_log_time"] = current_time

        return jsonify({
            "status": state["status"],
            "ear": round(float(avg_ear), 2),
            "mar": round(float(mar), 2),
            "blinks": state["blink_count"],
            "yawns": state["yawn_count"],
            "head_pose": state["head_direction"],
            "drowsy_alert": drowsy_alert,
            "recent_logs": state["logs"][-5:]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
