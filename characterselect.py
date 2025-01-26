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

# Font
text_font = pygame.font.SysFont(None, 100)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255,127,80)
BLUE = (0, 0, 255)
image_paths = ["art/0_idle.png", "art/2_idle.png", "art/2_idle.png", "art/3_idle.png"]
images_raw = [pygame.image.load(path) for path in image_paths]


# Corresponds to player 1, player 2
player_select_flags = [False, False]

TILE_WIDTH = 240
TILE_HEIGHT = 135
NUMBER_OF_CHARACTERS = 4
images = [pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT)) for img in images_raw]
total_width = len(images) * TILE_WIDTH + (len(images) - 1) * 10 
start_x = (WINDOW_WIDTH - total_width) // 2
start_y = (WINDOW_HEIGHT - TILE_HEIGHT) // 4 * 3

# can be between 0-3, [player_1, player_2]
player_cursors = [0, 3]




# Test Image
def draw_bg():
    screen.blit(bg, (0,0))

def slide(image, direction):
    image = pygame.transform.scale(image, (1485, 810))
    if direction == "right":
        image = pygame.transform.flip(image, True, False)
        screen.blit(image, (WINDOW_WIDTH // 2, 0))
    elif direction == "left":
        screen.blit(image, (- 1 * WINDOW_WIDTH // 4, 0))

def update_cursor_position(player, value):
    if type(player_select_flags[player]) != bool:
        return
    
    player_cursors[player] += value
    
    if player_cursors[player] >= NUMBER_OF_CHARACTERS:
        player_cursors[player] = 0
    elif player_cursors[player] < 0:
        player_cursors[player] = NUMBER_OF_CHARACTERS - 1
    
def draw_tiles(): 
    x = start_x
    for img in images:
        screen
        pygame.draw.rect(screen, WHITE, (x, start_y, TILE_WIDTH, TILE_HEIGHT))
        screen.blit(img, (x, start_y))
        
        x += TILE_WIDTH + 10  # Move to the right, with spacing
    if type(player_select_flags[0]) == bool:
        pygame.draw.rect(screen, RED, (start_x + player_cursors[0] * TILE_WIDTH + 10 * player_cursors[0], start_y, TILE_WIDTH, TILE_HEIGHT), 5)
    else: 
        pygame.draw.rect(screen, YELLOW, (start_x + player_cursors[0] * TILE_WIDTH + 10 * player_cursors[0], start_y, TILE_WIDTH, TILE_HEIGHT), 5)
    
    if type(player_select_flags[1]) == bool:
        pygame.draw.rect(screen, BLUE, (start_x + player_cursors[1] * TILE_WIDTH + 10 * player_cursors[1], start_y, TILE_WIDTH, TILE_HEIGHT), 5)
    else: 
        pygame.draw.rect(screen, ORANGE, (start_x + player_cursors[1] * TILE_WIDTH + 10 * player_cursors[1], start_y, TILE_WIDTH, TILE_HEIGHT), 5)

def draw_ready_to_battle():
    if player_select_flags[0] and player_select_flags[1]:
        ready_to_battle_text = text_font.render("PRESS ENTER TO START BUBBLING", True, BLACK)
        screen.blit(ready_to_battle_text, ((WINDOW_WIDTH - ready_to_battle_text.get_size()[0]) // 2, (WINDOW_HEIGHT - ready_to_battle_text.get_size()[1]) // 2))
        
        
MOVEMENT_BUTTONS = {
    pygame.K_a : (0, -1),
    pygame.K_d : (0, 1),  
    pygame.K_LEFT : (1, -1),
    pygame.K_RIGHT : (1, 1), 
}

SELECT_BUTTONS = {
    pygame.K_g : (0, True),
    pygame.K_h : (0, False),  
    pygame.K_KP1 : (1, True),
    pygame.K_KP2 : (1, False), 
}

def select_character(player_index, select_type):
    global player_select_flags
    if select_type:
        player_select_flags[player_index] = str(player_cursors[player_index])
        print(f"PLAYER {player_index} SELECTED {player_cursors[player_index]}")
    else:
        player_select_flags[player_index] = False
        print(f"PLAYER {player_index} UNSELECTED {player_cursors[player_index]}")
        

################################
def draw_descriptions():
    print('STUB')


################################
# Main function
def character_select_screen():
    running = True
    while running:
        for event in pygame.event.get(): 
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in MOVEMENT_BUTTONS:
                print(f"Key {pygame.key.name(event.key)} pressed")
                update_cursor_position(*MOVEMENT_BUTTONS[event.key])
            elif event.type == pygame.KEYDOWN and event.key in SELECT_BUTTONS:
                select_character(*SELECT_BUTTONS[event.key])
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if player_select_flags[0] and player_select_flags[1]:
                    running = False
                    print('DONE')
                    return player_select_flags

        draw_bg()
        slide(images_raw[player_cursors[0]], 'left')
        slide(images_raw[player_cursors[1]], 'right')
        draw_tiles()
        draw_descriptions()
        draw_ready_to_battle()

        pygame.display.update()

# Helper to take inputs of keys  DONE
# Helper to blit character icons/grids DONE
# Helper to slide selected characters onto screen DONE
# TODO Helper to show flavor text
# TODO Helper to show ability text
