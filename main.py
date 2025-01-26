import pygame
import picross
import characterselect

# Initialize Pygame
pygame.init()
pygame.mixer.init(44100, -16, 2, 4096)
pygame.mixer.music.load("music\start0.wav")


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

VOLUME = 1.0
pygame.mixer.music.set_volume(VOLUME)

while True:
    while GAME_STATE == "CHARACTER_SELECT":
        pygame.mixer.music.play(-1,0,0)
        characterselect.character_select_screen()
    while GAME_STATE == "PICROSS":
        pygame.mixer.music.play(-1,0,0)
        picross.picross_game()
    while GAME_STATE == "END_SCREEN":
        pass
