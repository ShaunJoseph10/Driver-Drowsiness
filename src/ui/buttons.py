import cv2

# Stores button coordinates
button_positions = {}


def draw_buttons(frame):

    global button_positions

    h, w = frame.shape[:2]

    button_width = 150
    button_height = 45
    gap = 20

    total_width = (button_width * 5) + (gap * 4)

    start_x = (w - total_width) // 2
    y = h - 60

    buttons = [
        ("LOGS", (70, 130, 180)),
        ("SCREENSHOTS", (70, 130, 180)),
        ("REPORT", (70, 130, 180)),
        ("EXIT", (0, 0, 180))
    ]

    button_positions.clear()

    for text, color in buttons:

        x1 = start_x
        y1 = y
        x2 = x1 + button_width
        y2 = y1 + button_height

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        size = cv2.getTextSize(
            text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            2
        )[0]

        text_x = x1 + (button_width - size[0]) // 2
        text_y = y1 + (button_height + size[1]) // 2

        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        button_positions[text] = (x1, y1, x2, y2)

        start_x += button_width + gap


def get_clicked_button(x, y):

    for button, (x1, y1, x2, y2) in button_positions.items():

        if x1 <= x <= x2 and y1 <= y <= y2:
            return button

    return None