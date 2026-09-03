import math

def calculate_ear(eye_points):
    # Vertical distances using built-in math.dist
    vertical_1 = math.dist(eye_points[1], eye_points[5])
    vertical_2 = math.dist(eye_points[2], eye_points[4])

    # Horizontal distance
    horizontal = math.dist(eye_points[0], eye_points[3])

    if horizontal == 0:
        return 0.0

    # EAR formula
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

    return ear