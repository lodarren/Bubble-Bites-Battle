import pygame


# Initialize Pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Init Images
image = pygame.image.load('test.png')

def foo():
    screen.blit(image, (0,0))
    pygame.display.update()
