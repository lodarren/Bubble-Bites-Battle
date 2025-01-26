import pygame
import picross
import characterselect

# Initialize Pygame
pygame.init()


# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Picross")

# Can be one of: 
# - "CHARACTER_SELECT"
# - "PICROSS"
# - "END_SCREEN"
GAME_STATE = "CHARACTER_SELECT"

while True:
    while GAME_STATE == "CHARACTER_SELECT":
        characterselect.foo()
    while GAME_STATE == "PICROSS":
        picross.picross_game()
    while GAME_STATE == "END_SCREEN":
        pass
