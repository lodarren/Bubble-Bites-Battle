import pygame
import sys
import endgame
import random
import puzzles

# Initialize Pygame
pygame.init()

# Music & SFX
pop = pygame.mixer.Sound('source/music/pop.mp3')
pin = pygame.mixer.Sound('source/music/pin.mp3')
soap = pygame.mixer.Sound('source/music/bubl.wav')
clang = pygame.mixer.Sound('source/music/clang.wav')
debuff = pygame.mixer.Sound('source/music/debuff.wav')
crit = pygame.mixer.Sound('source/music/crit.wav')
charge = pygame.mixer.Sound('source/music/charge.wav')
bomb = pygame.mixer.Sound('source/music/bomb.wav')

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
GRID1_OFFSET = (150, 150)  # Top-left corner of the first grid
GRID2_OFFSET = (1305, 150)  # Top-left corner of the second grid
GRID_SIZE = 7  # 5x5 grid
CELL_SIZE = 75

# Meter offsets
METER1_OFFSET = (0, WINDOW_HEIGHT - 3 * CELL_SIZE)
METER2_OFFSET = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 3 * CELL_SIZE)

# Score Offsets
SCORE1_OFFSET = (0, 0)
SCORE2_OFFSET = (0, 0)

# Score Offsets
SCORE1_OFFSET = (WINDOW_WIDTH // 2 - 175, 75)
SCORE2_OFFSET = (WINDOW_WIDTH // 2 + 150, 75)

# DAS Constants
DAS_DELAY = 0
DAS_INTERVAL = 100

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
pygame.display.set_caption("Picross")

# Timer settings
TIMER_DURATION = 180  # Countdown duration in seconds
start_ticks = pygame.time.get_ticks()  # Record the start time

# Example solution grid (1 for filled, 0 for empty)
solution_grid_1 = [
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
]
solution_grid_2 = [
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
]

# Player's current state

player_1_cursor = [0, 0]
player_2_cursor = [0, 0]

player_1_win_flag = False
player_2_win_flag = False

# TODO Fill in the characters
player_1_character = None
player_2_character = None

player_positions = [player_1_cursor, player_2_cursor]
player_grids = [
                [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)], 
                [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                ]
player_meters = [1, 1]
player_scores = [0, 0]
player_characters = [player_1_character, player_2_character]

# 0 for player 1, 1 for player 2
winner = 0

# 0 := false, 1 := true
sudden_death_flag = False

# Font for displaying row/column clues
font = pygame.font.SysFont(None, 36)
score_font = pygame.font.SysFont(None, 100)
timer_font = pygame.font.SysFont(None, 150)


# Bubbles can either be 0 : Not filled, 1 : Filled, 2 : Crossed
def draw_grid():
    """Draw the grid and current state."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = GRID1_OFFSET[0] + col * CELL_SIZE, GRID1_OFFSET[1] + row * CELL_SIZE

            if player_grids[0][row][col] == 0:
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            elif player_grids[0][row][col] == 1:
                screen.blit(pygame.image.load('source/art/b8.png'), (x, y))
            else:
                screen.blit(pygame.image.load('source/art/p12.png'), (x, y))
            

            # Draw grid lines
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x, y = GRID2_OFFSET[0] + col * CELL_SIZE, GRID2_OFFSET[1] + row * CELL_SIZE

                if player_grids[1][row][col] == 0:
                    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                elif player_grids[1][row][col] == 1:
                    screen.blit(pygame.image.load('source/art/b8.png'), (x, y))
                else:
                    screen.blit(pygame.image.load('source/art/p12.png'), (x, y))

                # Draw grid lines
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
    # Drawing the player cursor
    pygame.draw.rect(screen, YELLOW, (GRID1_OFFSET[0] + player_1_cursor[0] * CELL_SIZE, GRID1_OFFSET[1] + player_1_cursor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
    pygame.draw.rect(screen, YELLOW, (GRID2_OFFSET[0] + player_2_cursor[0] * CELL_SIZE, GRID2_OFFSET[1] + player_2_cursor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)


def draw_clues():
    # Draw row clues for grid 1
    for row_idx, row in enumerate(solution_grid_1):
        clue = get_clue(row)
        text = font.render(" ".join(map(str, clue)), True, BLACK)
        screen.blit(text, (GRID1_OFFSET[0] - CELL_SIZE * 1.25, row_idx * CELL_SIZE + GRID1_OFFSET[1] + CELL_SIZE//2))

    # Draw column clues for grid 1
    for col_idx in range(GRID_SIZE):
        column = [solution_grid_1[row][col_idx] for row in range(GRID_SIZE)]
        clue = get_clue(column)
        text = font.render(" ".join(map(str, clue)), True, BLACK)
    
        for i, number in enumerate(clue):
            # Render each number as text
            text = font.render(str(number), True, BLACK)
            
            # Draw each number at a different Y position (vertically)
            screen.blit(text, (col_idx * CELL_SIZE + GRID1_OFFSET[0] + CELL_SIZE // 2, GRID1_OFFSET[1] - CELL_SIZE * 1.25  + i * CELL_SIZE / len(clue)))
            
    # Draw row clues for grid 2
    for row_idx, row in enumerate(solution_grid_2):
        clue = get_clue(row)
        text = font.render(" ".join(map(str, clue)), True, BLACK)
        screen.blit(text, (GRID2_OFFSET[0] - CELL_SIZE * 1.25, row_idx * CELL_SIZE + GRID2_OFFSET[1] + CELL_SIZE//2))
        
    # Draw column clues for grid 2
    for col_idx in range(GRID_SIZE):
        column = [solution_grid_2[row][col_idx] for row in range(GRID_SIZE)]
        clue = get_clue(column)
        text = font.render(" ".join(map(str, clue)), True, BLACK)
    
        for i, number in enumerate(clue):
            # Render each number as text
            text = font.render(str(number), True, BLACK)
            
            # Draw each number at a different Y position (vertically)
            screen.blit(text, (col_idx * CELL_SIZE + GRID2_OFFSET[0] + CELL_SIZE // 2, GRID2_OFFSET[1] - CELL_SIZE * 1.25  + i * CELL_SIZE / len(clue)))


def draw_meter(): 
    # Load the progression meter sprites
    
    # THis is too hard to code, i need just the rectangle
    bar_meter_1 = pygame.image.load(player_1_character['progression_meter_sprite'])
    bar_meter_2 = pygame.image.load(player_2_character['progression_meter_sprite'])

    # Player 1 progression meter scaling and display
    if player_meters[0] < 1:
        # Scale the bar based on the player's progression meter
        scaled_bar_1 = pygame.transform.scale(bar_meter_1, (player_meters[0] * WINDOW_WIDTH // 2, 3 * CELL_SIZE))
        screen.blit(scaled_bar_1, (METER1_OFFSET[0], METER1_OFFSET[1]))
    else:
        # Player 1 has full meter, use the charged sprite
        screen.blit(pygame.image.load(player_1_character['charged_meter_sprite']), (METER1_OFFSET[0], METER1_OFFSET[1]))
    
    # Player 2 progression meter scaling and display
    if player_meters[1] < 1:
        # Scale the bar based on the player's progression meter
        scaled_bar_2 = pygame.transform.scale(bar_meter_2, (player_meters[1] * WINDOW_WIDTH // 2, 3 * CELL_SIZE))
        screen.blit(scaled_bar_2, (METER2_OFFSET[0] + (WINDOW_WIDTH // 2 * (1 - player_meters[1])), METER2_OFFSET[1]))
    else:
        # Player 2 has full meter, use the charged sprite
        screen.blit(pygame.image.load(player_2_character['charged_meter_sprite']), (METER2_OFFSET[0], METER2_OFFSET[1]))

    character_1_img = pygame.image.load(player_1_character['neutral_sprite'])
    character_2_img = pygame.image.load(player_2_character['neutral_sprite'])

    character_2_img = pygame.transform.flip(character_2_img, True, False)

    character_1_img = pygame.transform.scale(character_1_img, (192 * 2, 108 * 2))
    character_2_img = pygame.transform.scale(character_2_img, (192 * 2, 108 * 2))
        
    # Draw bars for both players (background bars)
    screen.blit(pygame.transform.scale(pygame.image.load(player_1_character['bar_sprite']), (WINDOW_WIDTH // 2, 3 * CELL_SIZE)), (METER1_OFFSET[0], METER1_OFFSET[1]))
    screen.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load(player_2_character['bar_sprite']), (WINDOW_WIDTH // 2, 3 * CELL_SIZE)), True, False), (METER2_OFFSET[0], METER2_OFFSET[1]))
    
    screen.blit(character_1_img, (- CELL_SIZE, METER1_OFFSET[1]))
    screen.blit(character_2_img, (WINDOW_WIDTH - 4 *  CELL_SIZE, METER2_OFFSET[1]))
    
    '''
    pygame.draw.rect(screen, RED, pygame.Rect(METER1_OFFSET[0], METER1_OFFSET[1], WINDOW_WIDTH // 2 * player_meters[0], 3 * CELL_SIZE))
    pygame.draw.rect(screen, BLUE, pygame.Rect(METER2_OFFSET[0] + (WINDOW_WIDTH // 2 * (1 - player_meters[1])), METER2_OFFSET[1], WINDOW_WIDTH // 2 * player_meters[1], 3 * CELL_SIZE))
    '''


def draw_score():
    score_1_text = score_font.render(str(player_scores[0]), True, BLACK)
    screen.blit(score_1_text, SCORE1_OFFSET)
    score_2_text = score_font.render(str(player_scores[1]), True, BLACK)
    screen.blit(score_2_text, SCORE2_OFFSET)


def get_clue(line):
    """Get the clue numbers for a row or column."""
    clue = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        elif count > 0:
            clue.append(count)
            count = 0
    if count > 0:
        clue.append(count)
    return clue if clue else [0]


def check_win(player_grid, solution_grid):
    """Check if the player has completed the puzzle correctly."""
    
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE):
            if solution_grid[r][c] == 1 and player_grid[r][c] != 1:
                return False
            elif solution_grid[r][c] == 0 and player_grid[r][c] == 1:
                return False
    
    return True

# Updates the cursor position, axis = 0 is x axis, axis = 1 is y axis.
def update_cursor_position(axis, value, player):
    player_positions[player][axis] += value
    
    if player_positions[player][axis] >= GRID_SIZE:
        player_positions[player][axis] = 0
    elif player_positions[player][axis] < 0:
        player_positions[player][axis] = GRID_SIZE - 1

    #print(player_positions[player])
        
bubble_animations = {}  # Stores ongoing bubble animations by (x, y)
pin_animations = {}  # Stores ongoing pin animations by (x, y)
soap_animations = {}

def spawn_bubble(x, y, grid_idx):
    gridoffset = (0, 0)
    if grid_idx == 0:
        gridoffset = GRID1_OFFSET
    else:
        gridoffset = GRID2_OFFSET
    # Starting position and frame tracking
    x, y = gridoffset[0] + x * CELL_SIZE, gridoffset[1] + y * CELL_SIZE
    bubble_animations[(x, y)] = {'idx': 1, 'last_update_time': pygame.time.get_ticks(), 'despawning': False}

def despawn_bubble(x, y, grid_idx):
    gridoffset = (0, 0)
    if grid_idx == 0:
        gridoffset = GRID1_OFFSET
    else:
        gridoffset = GRID2_OFFSET
    # Starting position and frame tracking for despawning
    x, y = gridoffset[0] + x * CELL_SIZE, gridoffset[1] + y * CELL_SIZE
    bubble_animations[(x, y)] = {'idx': 8, 'last_update_time': pygame.time.get_ticks(), 'despawning': True}

def spawn_pin(x, y, grid_idx):
    gridoffset = (0, 0)
    if grid_idx == 0:
        gridoffset = GRID1_OFFSET
    else:
        gridoffset = GRID2_OFFSET
    # Starting position and frame tracking
    x, y = gridoffset[0] + x * CELL_SIZE, gridoffset[1] + y * CELL_SIZE
    pin_animations[(x, y)] = {'idx': 1, 'last_update_time': pygame.time.get_ticks(), 'despawning': False}

def despawn_pin(x, y, grid_idx):
    gridoffset = (0, 0)
    if grid_idx == 0:
        gridoffset = GRID1_OFFSET
    else:
        gridoffset = GRID2_OFFSET
    # Starting position and frame tracking for despawning
    x, y = gridoffset[0] + x * CELL_SIZE, gridoffset[1] + y * CELL_SIZE
    pin_animations[(x, y)] = {'idx': 1, 'last_update_time': pygame.time.get_ticks(), 'despawning': True}

def spawn_soap(x, y, grid_idx):
    gridoffset = (0, 0)
    if grid_idx == 0:
        gridoffset = GRID1_OFFSET
    else:
        gridoffset = GRID2_OFFSET
    # Starting position and frame tracking for despawning
    x, y = gridoffset[0] + x * CELL_SIZE, gridoffset[1] + y * CELL_SIZE
    soap_animations[(x, y)] = {'idx': 1, 'last_update_time': pygame.time.get_ticks(), 'despawning': True}

def update_animations():
    # Update bubble animations
    for (x, y), animation in list(bubble_animations.items()):
        current_time = pygame.time.get_ticks()
        if current_time - animation['last_update_time'] >= 100:  # Update every 100ms
            screen.blit(pygame.image.load(f'source/art/b{int(animation["idx"])}.png'), (x, y))
            pygame.display.update()
            animation['last_update_time'] = current_time  # Update time
            if animation['despawning']:
                animation['idx'] -= 2
                if animation['idx'] <= 0:
                    del bubble_animations[(x, y)]  # Remove animation when finished
            else:
                animation['idx'] += 2
                if animation['idx'] >= 8:
                    del bubble_animations[(x, y)]  # Remove animation when finished

    # Update pin animations
    for (x, y), animation in list(pin_animations.items()):
        current_time = pygame.time.get_ticks()
        if current_time - animation['last_update_time'] >= 100:  # Update every 100ms
            screen.blit(pygame.image.load(f'source/art/p{int(animation["idx"])}.png'), (x, y))
            pygame.display.update()
            animation['last_update_time'] = current_time  # Update time
            if animation['despawning']:
                animation['idx'] -= 2
                if animation['idx'] <= 0:
                    del pin_animations[(x, y)]  # Remove animation when finished
            else:
                animation['idx'] += 2
                if animation['idx'] >= 12:
                    del pin_animations[(x, y)]  # Remove animation when finished
    
    # Update soap animations
    for (x, y), animation in list(pin_animations.items()):
        current_time = pygame.time.get_ticks()
        if current_time - animation['last_update_time'] >= 100:  # Update every 100ms
            screen.blit(pygame.image.load(f'source/art/s{int(animation["idx"])}.png'), (x, y))
            pygame.display.update()
            animation['last_update_time'] = current_time  # Update time
            animation['idx'] += 2
            if animation['idx'] >= 10:
                del pin_animations[(x, y)]  # Remove animation when finished


# Updates grid[r][c] with the specified mark        
def update_square(grid_idx, position, mark):

    grid = player_grids[grid_idx]
    
    if grid[position[1]][position[0]] == 0 and mark == 1:
        # bubble spawn
        spawn_bubble(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 1
        
    elif grid[position[1]][position[0]] == 0 and mark == 2:
        # pin spawn
        spawn_pin(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 2
        
    elif grid[position[1]][position[0]] == 1 and mark == 1:
        # bubble despawn
        despawn_bubble(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 0
        
    elif grid[position[1]][position[0]] == 1 and mark == 2:
        # pin spawn
        spawn_pin(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 2
        
    elif grid[position[1]][position[0]] == 2 and mark == 1:
        # bubble spawn
        spawn_bubble(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 1
        
    elif grid[position[1]][position[0]] == 2 and mark == 2:
        # pin despawn 
        despawn_pin(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 0
        
    #print(f'Placed {mark} at {position}')

    
# Similar to update_square, but doesn't replace marked squares    
def update_square_running(grid_idx, position, mark): 
    grid = player_grids[grid_idx]
    
    if grid[position[1]][position[0]] == 0 and mark == 1:
        # bubble spawn
        spawn_bubble(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 1
        
    elif grid[position[1]][position[0]] == 0 and mark == 2:
        # pin spawn
        spawn_pin(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 2
        
    elif grid[position[1]][position[0]] == 1 and mark == 1:
        pass

    elif grid[position[1]][position[0]] == 1 and mark == 2:
        pass
        
    elif grid[position[1]][position[0]] == 2 and mark == 1:
        pass 
        
    elif grid[position[1]][position[0]] == 2 and mark == 2:
        # pin despawn 
        despawn_pin(position[0], position[1], grid_idx)
        grid[position[1]][position[0]] = 0
        
    #print(f'Placed {mark} at {position}')

# Ultimate animation
def ult_animation(player_idx, character_sprite):
    character_image = pygame.image.load(character_sprite)
    character_image = pygame.transform.scale(character_image, (1920, 1080))  # Resize if necessary
    
    character_1_img = pygame.image.load(player_1_character['hit_sprite'])
    character_2_img = pygame.image.load(player_2_character['hit_sprite'])

    character_2_img = pygame.transform.flip(character_2_img, True, False)

    character_1_img = pygame.transform.scale(character_1_img, (192 * 2, 108 * 2))
    character_2_img = pygame.transform.scale(character_2_img, (192 * 2, 108 * 2))
        
    
    if player_idx == 0:
        character_rect = character_image.get_rect()
        character_rect.topleft = (-960,0) 
        
        # Variables
        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fade_surface.fill(BLACK)
        fade_opacity = 0
        fade_speed = 10  # Higher value fades faster
        character_speed = 30

        # TODO: Sound effect here
        

        
        # Fade to black
        while fade_opacity < 255:
            #screen.fill(WHITE)
            fade_surface.set_alpha(fade_opacity)
            screen.blit(fade_surface, (0, 0))
            fade_opacity += fade_speed
            #pygame.display.flip()

        # Move character onto the screen
        while character_rect.left < -480:
            screen.fill(BLACK)
            screen.blit(character_image, character_rect)
            character_rect.x += character_speed

            screen.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load(player_2_character['bar_sprite']), (WINDOW_WIDTH // 2, 3 * CELL_SIZE)), True, False), (METER2_OFFSET[0], METER2_OFFSET[1]))
            screen.blit(character_2_img, (WINDOW_WIDTH - 4 *  CELL_SIZE, METER2_OFFSET[1]))
            pygame.display.flip()
    else:
        character_image = pygame.transform.flip(character_image, True, False) 
        character_rect = character_image.get_rect()
        character_rect.topleft = (WINDOW_WIDTH // 2 + 480 - 240, 0) 
        
        # Variables
        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fade_surface.fill(BLACK)
        fade_opacity = 0
        fade_speed = 5  # Higher value fades faster
        character_speed = -30

        # TODO: Sound effect here
        
        # Fade to black
        while fade_opacity < 50:
            screen.fill(WHITE)
            fade_surface.set_alpha(fade_opacity)
            screen.blit(fade_surface, (0, 0))
            fade_opacity += fade_speed
            pygame.display.flip()

        # Move character onto the screen
        while character_rect.left > WINDOW_WIDTH // 2 - 480:
            screen.fill(BLACK)
            fade_surface.set_alpha(50)
            screen.blit(character_image, character_rect)
            character_rect.x += character_speed

            screen.blit(pygame.transform.scale(pygame.image.load(player_1_character['bar_sprite']), (WINDOW_WIDTH // 2, 3 * CELL_SIZE)), (METER1_OFFSET[0], METER1_OFFSET[1]))
            screen.blit(character_1_img, (- CELL_SIZE, METER1_OFFSET[1]))
            pygame.display.flip()
    # Pause for a moment
    pygame.time.wait(100)
    
def destroy_grid(player):
    # TODO PUT EFFECTS
    bomb.play()
    player_grids[player] = [[2 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    

def random_powerup(player): 
    global player_scores
    charge.play()
    # Define the possible values and their corresponding probabilities
    values = [-2, -1, 1, 2]
    probabilities = [0.05, 0.4, 0.4, 0.15]

    # Get a random value based on the probabilities
    player_scores[player] += random.choices(values, probabilities)[0]
    
    
def reveal_grid(player):
    revealed_idx = random.randint(0, 4)
    # effect
    if player == 0:
        for r in range(revealed_idx, revealed_idx + 3):
            for c in range(GRID_SIZE):
                spawn_soap(r, c, 1)
                if solution_grid_1[r][c] == 1:
                    player_grids[player][r][c] = 1
                else:
                    player_grids[player][r][c] = 2
    else:
        for r in range(revealed_idx, revealed_idx + 3):
            for c in range(GRID_SIZE):
                spawn_soap(r, c, 1)
                if solution_grid_2[r][c] == 1:
                    player_grids[player][r][c] = 1
                else:
                    player_grids[player][r][c] = 2
    pygame.display.update()           
                    
    

def swap_puzzles():
    # play swap sound effect
    global solution_grid_1, solution_grid_2
    temp = solution_grid_1
    solution_grid_1 = solution_grid_2
    solution_grid_2 = temp
    
    temp = player_grids[0]
    player_grids[0] = player_grids[1]
    player_grids[1] = temp
    
def ult_effect(player, effect):
    if effect == 0:
        destroy_grid(abs(player - 1))
    elif effect == 1:
        swap_puzzles()
    elif effect == 2:
        random_powerup(player)
    elif effect == 3:
        reveal_grid(player)
    
# Ultimate attack
def player_ult(character, player):
    global player_meters
    if player_meters[player] == 1: 
        #print(f'PLAYER {player} SUPER')
        ult_animation(player, character['attack_sprite'])
        ult_effect(player, character['effect'])
        #player_meters[player] = 0
    else: 
        print('failed')

# TODO restart the puzzle
def restart_puzzle(player):
    global solution_grid_1, solution_grid_2
    '''
    if player == 0:     
        solution_grid_1 = puzzles.puzzles[random.randint(0, len(puzzles.puzzles) - 1)]
        player_grids[0] = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    else: 
        solution_grid_2 = puzzles.puzzles[random.randint(0, len(puzzles.puzzles) - 1)]
        player_grids[1] = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
    
    This is the random puzzle generator
    '''
    if player == 0:     
        solution_grid_1 = [[random.randint(0, 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        player_grids[0] = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    else: 
        solution_grid_2 = [[random.randint(0, 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        player_grids[1] = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
# Game loop
key_states_movement = {} # When a key is pressed
key_states_placement = {} # When a key is pressed
last_action_time_movement = {} # Tracks the last time an action occured
last_action_time_placement = {}

# (Axis, ValueToIncrement, 0 := player 1; 1 := player 2)
MOVEMENT_BUTTONS = {
    pygame.K_w : (1, -1, 0),
    pygame.K_s : (1, 1, 0), 
    pygame.K_a : (0, -1, 0),
    pygame.K_d : (0, 1, 0),  
    pygame.K_UP : (1, -1, 1), 
    pygame.K_DOWN : (1, 1, 1), 
    pygame.K_LEFT : (0, -1, 1),
    pygame.K_RIGHT : (0, 1, 1), 
}

# grid, mark
PLACEMENT_BUTTONS = {
    pygame.K_g : (0, 1), 
    pygame.K_h : (0, 2), 
    pygame.K_KP1 : (1, 1), 
    pygame.K_KP2 : (1, 2), 
}

def update_scores(player): 
    global player_scores, player_meters
    if player == 0:
        player_scores[0] += 1
        player_meters[1] += 0.5 * player_1_character['multiplier']
    elif player == 1: 
        player_scores[1] += 1
        player_meters[0] += 0.5 * player_2_character['multiplier']
    
    if player_meters[0] > 1: 
        player_meters[0] = 1
    elif player_meters[1] > 1:
        player_meters[1] = 1
        

def sudden_death_sequence(): 
    global sudden_death_flag 
    sudden_death_text_1 = font.render(f"SUDDEN DEATH!", True, BLACK)
    sudden_death_text_2 = font.render(f"FIRST TO FINISH WINS!", True, BLACK)
    screen.blit(sudden_death_text_1, (WINDOW_WIDTH // 2 - 80 , WINDOW_HEIGHT // 2 - 100))
    screen.blit(sudden_death_text_2, (WINDOW_WIDTH // 2 - 125 , WINDOW_HEIGHT // 2))
    sudden_death_flag = True


def game_end_sequence_sudden_death():
    if player_scores[0] > player_scores[1]:
        game_over_text = font.render("Player 1 Wins!", True, BLACK)
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 75 , WINDOW_HEIGHT // 2))
    else: 
        game_over_text = font.render("Player 2 Wins!", True, BLACK)
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 100))
    
    pygame.display.update()

def game_end_sequence_normal():
    game_over_text = font.render("Time's Up!", True, BLACK)
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(3000)
    
    if player_scores[0] > player_scores[1]:
        player_win_text = font.render("Player 1 Wins!", True, BLACK)
    else: 
        player_win_text = font.render("Player 2 Wins!", True, BLACK)
        
    screen.blit(player_win_text, (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 100))
    
    
    pygame.display.update()

def flash_screen(player_idx):
    if player_idx == 0:
        pygame.draw.rect(screen, YELLOW, (GRID1_OFFSET[0], GRID1_OFFSET[1], CELL_SIZE * 7, CELL_SIZE * 7))
    else:
        pygame.draw.rect(screen, YELLOW, (GRID2_OFFSET[0], GRID2_OFFSET[1], CELL_SIZE * 7, CELL_SIZE * 7))
    
    pygame.display.flip()
    
        
def picross_game():
    running = True
    while running:
        screen.blit(pygame.image.load("source/art/bg_light.png"), (0, 0))
        current_time = pygame.time.get_ticks()
        
        # Draw everything
        draw_grid()
        draw_meter()
        draw_clues()
        draw_score()
        update_animations()

        # Event handling
        for event in pygame.event.get(): 
            pressed_keys = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key in MOVEMENT_BUTTONS:
                if event.key not in key_states_movement:
                    key_states_movement[event.key] = current_time
                    last_action_time_movement[event.key] = 0
                    #print(f"Key {pygame.key.name(event.key)} pressed")
                    #update_cursor_position(*MOVEMENT_BUTTONS[event.key])
                    
                    for placement_key in PLACEMENT_BUTTONS:
                        if pressed_keys[placement_key]:
                            update_square_running(PLACEMENT_BUTTONS[placement_key][0], player_positions[PLACEMENT_BUTTONS[placement_key][0]], PLACEMENT_BUTTONS[placement_key][1])
                    
            elif event.type == pygame.KEYUP and event.key in MOVEMENT_BUTTONS:
                if event.key in key_states_movement:
                    del key_states_movement[event.key]
                    if event.key in last_action_time_movement:
                        del last_action_time_movement[event.key]
                    #print(f"Key {pygame.key.name(event.key)} released")
                    
        
            elif event.type == pygame.KEYDOWN and event.key in PLACEMENT_BUTTONS:  
                key_states_placement[event.key] = (current_time, player_positions[PLACEMENT_BUTTONS[event.key][0]])
                last_action_time_placement[event.key] = (0, player_positions[PLACEMENT_BUTTONS[event.key][0]])
                #print(f"Key {pygame.key.name(event.key)} pressed")
                update_square(PLACEMENT_BUTTONS[event.key][0], player_positions[PLACEMENT_BUTTONS[event.key][0]], PLACEMENT_BUTTONS[event.key][1])
                #print(player_grids[PLACEMENT_BUTTONS[event.key][0]])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    player_ult(player_1_character, 0)
                elif event.key == pygame.K_KP3:
                    player_ult(player_2_character, 1)
                
            
        
        for key, press_time in list(key_states_movement.items()):
            elapsed = current_time - press_time
            pressed_keys = pygame.key.get_pressed()
            for placement_key in PLACEMENT_BUTTONS:
                if pressed_keys[placement_key]:
                    update_square_running(PLACEMENT_BUTTONS[placement_key][0], player_positions[PLACEMENT_BUTTONS[placement_key][0]], PLACEMENT_BUTTONS[placement_key][1])
            
            if elapsed >= DAS_DELAY:
                time_since_last_action = current_time - last_action_time_movement[key]
                if time_since_last_action >= DAS_INTERVAL:
                    #print(f"Action triggered for key: {pygame.key.name(key)}")
                    update_cursor_position(*MOVEMENT_BUTTONS[key])
                    last_action_time_movement[key] = current_time 
        

        # Check win condition
        global player_1_win_flag, player_2_win_flag
        if check_win(player_grids[0], solution_grid_1) and not player_1_win_flag:
            player_1_win_flag = True
            update_scores(0)
            flash_screen(0)
            restart_puzzle(0)
            #print(player_grids[0])
            player_1_win_flag = False
        elif check_win(player_grids[1], solution_grid_2) and not player_2_win_flag:
            player_2_win_flag = True
            update_scores(1)
            flash_screen(1)
            restart_puzzle(1)
            player_2_win_flag = False
            

        # Calculate the remaining time
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert ms to seconds
        remaining_time = max(TIMER_DURATION - elapsed_time, 0)  # Countdown timer
        
        timer_text = timer_font.render(f"{remaining_time}", True, BLACK)
        text_width, _ = timer_text.get_size()
        screen.blit(timer_text, ((WINDOW_WIDTH - text_width)//2, 50))  # Display at top-right corner

        
        # Check if the timer runs out
        if remaining_time <= 0:
            if player_scores[0] != player_scores[1] and running:
                if sudden_death_flag: 
                    game_end_sequence_sudden_death()
                else: 
                    game_end_sequence_normal()
                pygame.time.wait(3000)  # Wait for 3 seconds before quitting
                running = False
            elif remaining_time <= 0 and player_scores[0] == player_scores[1] and running:
                sudden_death_sequence()
            
        pygame.display.flip()
    
    return winner


def start_picross(character_1, character_2):
    global player_1_character, player_2_character
    
    player_1_character = character_1
    player_2_character = character_2

    picross_game()
    
    return #This is the character that wins
    

#start_picross(None, None)


#pygame.quit()
#sys.exit()


# CLOCK DONE
# Add score DONE
# Super animation when add/destroy
# meter scores DONE
# add sprites 
# add 7x7 picross puzzles DONE


# TODO Get the supers/ADD/Destroy
# TODO Get the game to for loop to get multiple games
# TODO TIMER