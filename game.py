import pygame
import sys
import time
import ttt

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

# asking user for size of board they want to play
def get_board_size():
    while True:
        try:
            size_input = int(input("Enter the size of the Tic-Tac-Toe board (nxn): "))
            if size_input < 3:
                print("The board size should be at least 3x3.")
            else:
                return size_input
        except ValueError:
            print("Please enter a valid integer.")

# creating board based on user input
board_size = get_board_size()  # board size from the user
board = ttt.initial_state(board_size)  # pass the size to your gameMaster's initial state


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # user chooses player
    if user is None:

        # create title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
        
        # create button
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)


