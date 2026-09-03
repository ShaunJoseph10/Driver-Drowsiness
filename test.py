import pygame
import time

pygame.mixer.init()

print("Mixer initialized")

pygame.mixer.music.load("assets/sounds/mixkit-classic-alarm-995.wav")

print("Sound loaded")

pygame.mixer.music.play()

print("Playing...")

time.sleep(10)