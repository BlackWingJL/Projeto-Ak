import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("musicas/Haruka Mirai.mp3")  # Substitua pelo caminho do seu arquivo
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    time.sleep(1)