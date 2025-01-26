import pygame
import time
import random

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
bg = pygame.image.load('source/art/bg_character_select.png')

# Font
text_font = pygame.font.SysFont(None, 50)

image_paths = ["source/art/0_idle.png", "source/art/1_idle.png", "source/art/2_idle.png", "source/art/3_idle.png"]
images_raw = [pygame.image.load(path) for path in image_paths]

pop = pygame.mixer.Sound('source/music/pop.mp3')
pop.set_volume(1.0)
c_jump = pygame.mixer.Sound('source/music/c_jump.wav')
c_downer = pygame.mixer.Sound('source/music/c_downer.wav')
surprise = pygame.mixer.Sound('source/music/surprise.ogg')
quick_surprise = pygame.mixer.Sound('source/music/quick_surprise.ogg')

# Corresponds to player 1, player 2
player_select_flags = [False, False]

TILE_WIDTH = 240
TILE_HEIGHT = 135
NUMBER_OF_CHARACTERS = 4
images = [pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT)) for img in images_raw]
total_width = len(images) * TILE_WIDTH + (len(images) - 1) * 10 
start_x = (WINDOW_WIDTH - total_width) // 2
start_y = (WINDOW_HEIGHT - TILE_HEIGHT) // 4 * 3

# Box dimensions (Rightside)
box_width = 860
box_height = 200
box_x = WINDOW_WIDTH - box_width - 20  # 20px padding from the right
box_y = WINDOW_HEIGHT - box_height - 20 # 20px padding from the bottom
rect_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)  # Surface with alpha
rect_surface.fill((0, 0, 0, 0))  # Clear the surface (fully transparent)


# Rox dimensions (Leftside Box)
rox_x = 20  # 20px padding from the right
rox_y = WINDOW_HEIGHT - box_height - 20 # 20px padding from the bottom

# Possible Texts
des = {
0: "The raging beast - Bubble Waffle \nDon't mess with Bubble Waffle, \nhe tastes extra aggresive today! \n Skill - Blow up your foe's board!",
1: "The tricksters - Bubble Chocolates \nWant double the trouble? \nBubble Chocolate twins are here!\n Skill - Switch your board with the foe!",
2: "The shy pop - Bubble Tea \nOne cute matcha bubble tea with the \nbest pearls in town, please!\n Skill - Random Powerup!",
3: "The bubble queen - Bubble Gum \nThe sassiest pink bubble gum from the \nsweetest gumball machine you'll ever meet!\n Skill - Autosolves 3 rows!"
}

# can be between 0-3, [player_1, player_2]
player_cursors = [0, 3]

# Initial zoom settings
zoom_factor = 1
zooming = False
zoom_start_time = 0
zoom_duration = 1.5

# Test Image
def draw_bg():
    zoomed_bg = pygame.transform.scale(bg, (int(WINDOW_WIDTH * zoom_factor), int(WINDOW_HEIGHT * zoom_factor)))
    x_offset = (zoomed_bg.get_width() - WINDOW_WIDTH) // 2
    y_offset = (zoomed_bg.get_height() - WINDOW_HEIGHT) // 2
    screen.blit(zoomed_bg, (-x_offset, -y_offset))

def slide(image, direction):
    image = pygame.transform.scale(image, (1485, 810))
    if direction == "right":
        image = pygame.transform.flip(image, True, False)
        screen.blit(image, (WINDOW_WIDTH // 2 - 150, 0))
    elif direction == "left":
        screen.blit(image, (- 1 * WINDOW_WIDTH // 4 + 150, 0))

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
    pygame.K_j : (1, -1),
    pygame.K_l : (1, 1), 
}

SELECT_BUTTONS = {
    pygame.K_f : (0, True),
    pygame.K_g : (0, False),  
    pygame.K_SEMICOLON : (1, True),
    pygame.K_QUOTE : (1, False), 
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
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=10)
    pygame.draw.rect(screen, WHITE, (rox_x, rox_y, box_width, box_height), border_radius=10)
    draw_words()

def draw_words():
    lines = des[player_cursors[1]].splitlines()
    line_height = text_font.get_linesize()  # Get the height of each line
    for i, line in enumerate(lines):
        # Render each line
        text_surface = text_font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(box_x + box_width // 2, box_y + 40 + i * line_height))
        screen.blit(text_surface, text_rect)

    lines_2 = des[player_cursors[0]].splitlines()
    line_height = text_font.get_linesize()  # Get the height of each line
    for i, line in enumerate(lines_2):
        # Render each line
        text_surface_2 = text_font.render(line, True, BLACK)
        text_rect_2 = text_surface_2.get_rect(center=(box_width // 2 + 20, box_y + 40 + i * line_height))
        screen.blit(text_surface_2, text_rect_2)

################################
# Main function
def character_select_screen():
    global zooming, zoom_factor, zoom_start_time, player_index
    running = True
    while running:
        for event in pygame.event.get(): 
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in MOVEMENT_BUTTONS:
                print(f"Key {pygame.key.name(event.key)} pressed")
                if player_select_flags[0] and player_select_flags[1]:
                    quick_surprise.play()
                else:
                    pop.play()
                update_cursor_position(*MOVEMENT_BUTTONS[event.key])
            elif event.type == pygame.KEYDOWN and event.key in SELECT_BUTTONS:
                rng = random.randint(1,10)
                select_character(*SELECT_BUTTONS[event.key])
                if rng != 4:
                    c_downer.play()
                else:
                    surprise.play()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if player_select_flags[0] and player_select_flags[1] and zooming == False:
                    c_jump.play()
                    # Start zoom effect when Enter is pressed
                    zooming = True
                    zoom_start_time = time.time()  # Capture time when Enter is pressed
                    
        
        if zooming:
            elapsed_time = time.time() - zoom_start_time
            if elapsed_time < zoom_duration:
                zoom_factor = 1 + (elapsed_time / zoom_duration)  # Gradually zoom in
            else:
                zoom_factor = 2  # Max zoom after 1.5 seconds
                zooming = False  # Stop zooming after the effect is finished
                running = False
                print('DONE')
                return player_select_flags

        if zooming:
            draw_bg()
        else:
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
