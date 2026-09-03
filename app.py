import os
import cv2
import base64
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Import existing detection utilities
from src.detection.eye_detector import face_mesh
from src.utils.ear import calculate_ear
from src.detection.yawn_detector import calculate_mar
from src.detection.head_pose import get_head_pose
from src.utils.constants import EAR_THRESHOLD
from src.utils.s3_uploader import upload_file_to_s3

app = Flask(__name__)

# Global state / counters per frame request
CLOSED_EYES_THRESHOLD = 15
MAR_THRESHOLD = 0.40

# In-memory session tracking
state = {
    "eye_closed_counter": 0,
    "yawn_counter": 0,
    "blink_counter": 0,
    "status": "NORMAL",
    "last_s3_upload": 0
}

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

        # Decode base64 image from browser webcam
        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid frame"}), 400

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        ear = 0.0
        mar = 0.0
        drowsy_alert = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract Eye Points
                left_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in [33, 160, 158, 133, 153, 144]]
                right_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in [362, 385, 387, 263, 373, 380]]
                
                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                ear = (left_ear + right_ear) / 2.0

                # Drowsiness Logic
                if ear < EAR_THRESHOLD:
                    state["eye_closed_counter"] += 1
                else:
                    if state["eye_closed_counter"] > 2:
                        state["blink_counter"] += 1
                    state["eye_closed_counter"] = 0

                if state["eye_closed_counter"] >= CLOSED_EYES_THRESHOLD:
                    drowsy_alert = True
                    state["status"] = "DROWSY WARNING!"

                    # Save screenshot locally & upload to AWS S3
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"drowsy_{timestamp}.jpg"
                    filepath = os.path.join("screenshots", filename)
                    os.makedirs("screenshots", exist_ok=True)
                    cv2.imwrite(filepath, frame)
                    upload_file_to_s3(filepath, f"screenshots/{filename}")
                else:
                    state["status"] = "ACTIVE & ALERT"

        return jsonify({
            "status": state["status"],
            "ear": round(ear, 2),
            "blinks": state["blink_counter"],
            "drowsy_alert": drowsy_alert
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
