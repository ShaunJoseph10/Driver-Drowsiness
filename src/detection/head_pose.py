import math

def get_head_pose(face_landmarks, frame_w, frame_h):
    landmarks = face_landmarks.landmark

    nose = landmarks[1]
    chin = landmarks[152]
    left_eye = landmarks[33]
    right_eye = landmarks[263]

    nose_x = nose.x * frame_w
    nose_y = nose.y * frame_h

    left_x = left_eye.x * frame_w
    right_x = right_eye.x * frame_w

    left_y = left_eye.y * frame_h
    right_y = right_eye.y * frame_h

    chin_y = chin.y * frame_h

    # Scale reference: distance between eyes
    eye_dist = math.hypot(right_x - left_x, right_y - left_y)
    if eye_dist == 0:
        return "CENTER"

    # Horizontal yaw offset (normalized by eye distance)
    face_center_x = (left_x + right_x) / 2.0
    norm_yaw = (nose_x - face_center_x) / eye_dist

    # Vertical pitch ratio: distance(nose, eyes) / distance(chin, nose)
    eye_center_y = (left_y + right_y) / 2.0
    nose_eye_dist = nose_y - eye_center_y
    chin_nose_dist = chin_y - nose_y

    # 1. YAW (LEFT / RIGHT from user perspective)
    if norm_yaw > 0.14:
        return "LEFT"
    if norm_yaw < -0.14:
        return "RIGHT"

    # 2. PITCH (UP / DOWN)
    if chin_nose_dist > 0:
        pitch_ratio = nose_eye_dist / chin_nose_dist
        if pitch_ratio > 1.05:
            return "DOWN"
        if pitch_ratio < 0.42:
            return "UP"

    # 3. ROLL (TILT LEFT / TILT RIGHT)
    eye_slope = (right_y - left_y) / eye_dist
    if eye_slope > 0.22:
        return "TILT RIGHT"
    if eye_slope < -0.22:
        return "TILT LEFT"

    return "CENTER"