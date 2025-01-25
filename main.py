import pygame
import sys
import endgame
import characterselect
import picross
import random


# Initialize Pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
GRID1_OFFSET = (150, 150)  # Top-left corner of the first grid
GRID2_OFFSET = (1305, 150)  # Top-left corner of the second grid
GRID_SIZE = 7  # 5x5 grid
CELL_SIZE = 75

# DAS Constants
DAS_DELAY = 300
DAS_INTERVAL = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
ORANGE = (255,127,80)
YELLOW = (255, 255, 0)

# Variables
# Init as 0, 1
PLAY_STATE = 0

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Picross")