import math

UPPER_LIP = 13
LOWER_LIP = 14

LEFT_MOUTH = 78
RIGHT_MOUTH = 308


def distance(p1, p2):
    return math.hypot(
        p1[0] - p2[0],
        p1[1] - p2[1]
    )


def calculate_mar(
        landmarks,
        frame_width,
        frame_height):

    upper = landmarks[UPPER_LIP]
    lower = landmarks[LOWER_LIP]

    left = landmarks[LEFT_MOUTH]
    right = landmarks[RIGHT_MOUTH]

    vertical = distance(
        (
            upper.x * frame_width,
            upper.y * frame_height
        ),
        (
            lower.x * frame_width,
            lower.y * frame_height
        )
    )

    horizontal = distance(
        (
            left.x * frame_width,
            left.y * frame_height
        ),
        (
            right.x * frame_width,
            right.y * frame_height
        )
    )
    if horizontal == 0:
        return 0

    return vertical / horizontal