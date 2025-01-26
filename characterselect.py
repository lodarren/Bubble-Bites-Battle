import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Init Images
bg = pygame.image.load('art\\bg_character_select.png')

P1_SELECT = "None"
P2_SELECT = "None"

# Test Image
def draw_bg():
    screen.blit(bg, (0,0))
    pygame.display.update()

def slide(image, direction):
    if direction == "right":
        image = pygame.transform.flip(image, True, False)
    else:
        pass

    


# Main function
def character_select_screen():
    active = True
    while active:
        for event in pygame.event.get(): 
            pressed_keys = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT:
                running = False

        # TODO Helper to take inputs of keys
        # TODO Helper to blit character icons/grids
        # TODO Helper to slide selected characters onto screen
        # TODO Helper to show flavor text
        # TODO Helper to show ability text

        draw_bg()
        pygame.display.update()