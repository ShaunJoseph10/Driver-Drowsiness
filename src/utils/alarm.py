import pygame
import threading
import os
import sys

pygame.mixer.init()

# Resource Path
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    # Go from src/utils -> project folder
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

alarm_path = os.path.join(
    BASE_DIR,
    "assets",
    "sounds",
    "mixkit-classic-alarm-995.wav"
)

print("Alarm Path:", alarm_path)

alarm_playing = False


def play_alarm():
    global alarm_playing

    if not alarm_playing:
        alarm_playing = True
        pygame.mixer.music.load(alarm_path)
        pygame.mixer.music.play(-1)


def stop_alarm():
    global alarm_playing

    pygame.mixer.music.stop()
    alarm_playing = False


def start_alarm_thread():
    threading.Thread(
        target=play_alarm,
        daemon=True
    ).start()