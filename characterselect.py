import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
ORANGE = (255,127,80)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Init Images
bg = pygame.image.load('art/bg_character_select.png')

# Unit Images
bw_idle = pygame.image.load('art/0_idle.png')
bt_idle = pygame.image.load('art/2_idle.png')
bg_idle = pygame.image.load('art/3_idle.png')

# Vars
GRID1_OFFSET = (150, 150)  # Top-left corner of the first grid
GRID2_OFFSET = (1305, 150)  # Top-left corner of the second grid
GRID_SIZE = 4  # 5x5 grid
CELL_SIZE = 75



# Define areas for hovering and selecting
GRID_1_RECT = pygame.Rect(GRID1_OFFSET[0], GRID1_OFFSET[1], GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)

# Player selection tracking
player_grids = [
                [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                ]

def draw_grid():
    """Draw the grid and current state."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = GRID1_OFFSET[0] + col * CELL_SIZE, GRID1_OFFSET[1] + row * CELL_SIZE

            if player_grids[0][row][col] == 0:
                color = WHITE
            elif player_grids[0][row][col] == 1:
                color = BLACK
            else:
                color = ORANGE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw grid lines
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x, y = GRID2_OFFSET[0] + col * CELL_SIZE, GRID2_OFFSET[1] + row * CELL_SIZE

                if player_grids[1][row][col] == 0:
                    color = WHITE
                elif player_grids[1][row][col] == 1:
                    color = BLACK
                else:
                    color = ORANGE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw grid lines
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
    # Drawing the player cursor
    pygame.draw.rect(screen, YELLOW, (GRID1_OFFSET[0] + player_1_cursor[0] * CELL_SIZE, GRID1_OFFSET[1] + player_1_cursor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
    pygame.draw.rect(screen, YELLOW, (GRID2_OFFSET[0] + player_2_cursor[0] * CELL_SIZE, GRID2_OFFSET[1] + player_2_cursor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)


global P1_SELECT, P2_SELECT, p1_cursor, p2_cursor, image_rect, image_rect_2
P1_SELECT = None
P2_SELECT = None
p1_cursor = pygame.Rect(GRID1_OFFSET[0], GRID1_OFFSET[1], CELL_SIZE, CELL_SIZE)  # Player 1 cursor
p2_cursor = pygame.Rect(GRID1_OFFSET[0], GRID1_OFFSET[1], CELL_SIZE, CELL_SIZE)  # Player 2 cursor
image_rect = None
image_rect_2 = None

# Allows for multiple plays.
def reset():
    global P1_SELECT, P2_SELECT, p1_cursor, p2_cursor, image_rect, image_rect_2
    P1_SELECT = None
    P2_SELECT = None
    p1_cursor = pygame.Rect(GRID1_OFFSET[0], GRID1_OFFSET[1], CELL_SIZE, CELL_SIZE)
    p2_cursor = pygame.Rect(GRID2_OFFSET[0], GRID2_OFFSET[1], CELL_SIZE, CELL_SIZE)
    image_rect = None
    image_rect_2 = None

# Test Image
def draw_bg():
    screen.blit(bg, (0,0))

def draw_sprites():
    if image_rect:
        screen.blit(bt_idle, image_rect)
    if image_rect_2:
        screen.blit(flipped_bw_idle, image_rect_2)
        

def slide(image, direction):
    global image_rect, image_rect_2, flipped_bw_idle
    if direction == "right":
        flipped_bw_idle = pygame.transform.flip(image, True, False)
        image_rect_2 = flipped_bw_idle.get_rect()
        image_rect_2.left = WINDOW_WIDTH
    else:
        image_rect = image.get_rect()
        image_rect.right = 0

def move():
    global image_rect, image_rect_2
    if image_rect_2:
        if image_rect_2.left > 500: 
            image_rect_2.left -= 100
        else:
            image_rect_2.left = 500

    if image_rect:
        if image_rect.right < 1420: 
            image_rect.right += 100
        else:
            image_rect.right = 1420


def update():
    move()

# Main function
def character_select_screen():
    active = True
    while active:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:  # Detect key press
                if event.key == pygame.K_RIGHT:  # Right arrow key
                    slide(bw_idle, "right")
                elif event.key == pygame.K_LEFT:  # Left arrow key
                    slide(bw_idle, "left")

        move()
        update()
        draw_bg()
        draw_sprites()
        pygame.display.update()
        clock.tick(60)

# TODO Helper to blit character icons/grids
# TODO Helper to slide selected characters onto screen
# TODO Helper to show flavor text
# TODO Helper to show ability text
