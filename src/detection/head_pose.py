import cv2
import numpy as np


def get_head_pose(face_landmarks, frame_w, frame_h):

    landmarks = face_landmarks.landmark

    nose = landmarks[1]
    chin = landmarks[152]

    left_eye = landmarks[33]
    right_eye = landmarks[263]

    left_mouth = landmarks[61]
    right_mouth = landmarks[291]

    nose_x = nose.x * frame_w
    nose_y = nose.y * frame_h

    left_x = left_eye.x * frame_w
    right_x = right_eye.x * frame_w

    left_y = left_eye.y * frame_h
    right_y = right_eye.y * frame_h

    chin_y = chin.y * frame_h

    face_center_x = (left_x + right_x) / 2
    horizontal_offset = nose_x - face_center_x

    eye_center_y = (left_y + right_y) / 2
    vertical_offset = nose_y - eye_center_y

    eye_slope = right_y - left_y

    # LEFT / RIGHT
    if horizontal_offset > 25:
        return "RIGHT"

    if horizontal_offset < -25:
        return "LEFT"

    # UP / DOWN
    if vertical_offset > 80:
        return "DOWN"

    if vertical_offset < 40:
        return "UP"

    # TILT
    if eye_slope > 15:
        return "TILT RIGHT"

    if eye_slope < -15:
        return "TILT LEFT"

    return "CENTER"