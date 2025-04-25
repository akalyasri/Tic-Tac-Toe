import pygame
import sys
import time
import gameMaster as ttt

pygame.init()

# window size - might change later
size = width, height = 900, 700  

# colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = None  # in the begining, none
ai_turn = False

