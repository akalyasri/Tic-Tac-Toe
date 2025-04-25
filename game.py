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

    # adding a background
    for y in range(height):
        color = (y * 255 // height, y * 255 // height, y * 255 // height)
        pygame.draw.line(screen, color, (0, y), (width, y))


    # user chooses player
    if user is None:

        # create title
        title_text = "Play Tic-Tac-Toe"
        title = largeFont.render(title_text, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        
        # adding a shadow effect
        shadow = largeFont.render(title_text, True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=titleRect.center)
        shadow_rect.move_ip(2, 2)
        screen.blit(shadow, shadow_rect)
        screen.blit(title, titleRect)

        
        # create button
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        
        mouse = pygame.mouse.get_pos()
        hoverX = playXButton.collidepoint(mouse)
        pygame.draw.rect(screen, (200, 200, 200) if hoverX else white, playXButton, border_radius=10)


        screen.blit(playX, playXRect)

        # making front end a bit fancier
        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center

        hoverO = playOButton.collidepoint(mouse)
        pygame.draw.rect(screen, (200, 200, 200) if hoverO else white, playOButton, border_radius=10)
        screen.blit(playO, playORect)

        # check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:
        # dynamically adjust the tile size - based on window size and board size

        margin = 20  # the space between the tiles and the window edges
        tile_size = min((width - 2 * margin) / board_size, (height - 2 * margin) / board_size)
        
        # position of the top left corner of the board (center the board on the screen)
        tile_origin = ((width - board_size * tile_size) / 2, (height - board_size * tile_size) / 2)

        tiles = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board, board_size)
        player = ttt.player(board)

        # display title
        if game_over:
            winner = ttt.check_winner(board, board_size)
            if winner is None:
                title_text = f"Game Over: Tie."
            else:
                title_text = f"Game Over: {winner} wins."
        elif user == player:
            title_text = f"Play as {user}"
        else:
            title_text = f"Thinking..."
        title = largeFont.render(title_text, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        
        # adding a soft glow
        shadow = largeFont.render(title_text, True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=titleRect.center)
        shadow_rect.move_ip(2, 2)
        screen.blit(shadow, shadow_rect)
        screen.blit(title, titleRect)


        # check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board, board_size)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(board_size):
                for j in range(board_size):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state(board_size)
                    ai_turn = False

    pygame.display.flip()

