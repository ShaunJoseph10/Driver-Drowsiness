from scipy.spatial import distance

def calculate_ear(eye_points):

    # Vertical distances
    vertical_1 = distance.euclidean(eye_points[1], eye_points[5])

    vertical_2 = distance.euclidean(eye_points[2], eye_points[4])

    # Horizontal distance
    horizontal = distance.euclidean(eye_points[0], eye_points[3])

    # EAR formula
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

    return ear