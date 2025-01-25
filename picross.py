import pygame
import sys
import endgame

# Initialize Pygame
pygame.init()

# Joystick initialization
pygame.joystick.init()
num_joysticks = pygame.joystick.get_count()
print(f"Number of joysticks connected: {num_joysticks}")
player_1_cursor = [0, 0]
player_2_cursor = [0, 0]
player_1_meter = 0
player_2_meter = 0

player_positions = [player_1_cursor, player_2_cursor]

'''
if num_joysticks > 0:
    player_1 = pygame.joystick.Joystick(0)
    player_1.init()
    player_1_cursor = [0, 0]
    player_1_meter = 0
    
if num_joysticks > 1: 
    player_2 = pygame.joystick.Joystick(1)
    player_2.init()
    player_2_cursor = [0, 0]
    player_2_meter = 0

# TODO FIX THIS
player_positions = [player_1_cursor]
'''

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
GRID_SIZE = 7  # 5x5 grid
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

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

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Picross")

# Example solution grid (1 for filled, 0 for empty)
solution_grid = [
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
]

# Player's current state
player_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Font for displaying row/column clues
font = pygame.font.SysFont(None, 36)


# Bubbles can either be 0 : Not filled, 1 : Filled, 2 : Crossed
def draw_grid():
    """Draw the grid and current state."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE, row * CELL_SIZE

            if player_grid[row][col] == 0:
                color = WHITE
            elif player_grid[row][col] == 1:
                color = BLACK
            else:
                color = ORANGE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw grid lines
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
    
    # Drawing the player cursor
    pygame.draw.rect(screen, YELLOW, (player_1_cursor[0] * CELL_SIZE, player_1_cursor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)


def draw_clues():
    """Draw the row and column clues."""
    # Calculate row clues
    for row_idx, row in enumerate(solution_grid):
        clue = get_clue(row)
        text = font.render(" ".join(map(str, clue)), True, BLACK)
        screen.blit(text, (WINDOW_WIDTH - 100, row_idx * CELL_SIZE + CELL_SIZE // 3))

    # Calculate column clues
    for col_idx in range(GRID_SIZE):
        column = [solution_grid[row][col_idx] for row in range(GRID_SIZE)]
        clue = get_clue(column)
        text = font.render(" ".join(map(str, clue)), True, BLACK)
        screen.blit(text, (col_idx * CELL_SIZE + CELL_SIZE // 4, WINDOW_HEIGHT - 50))


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


def check_win():
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

    print(player_positions[player])
        

# Updates grid[r][c] with the specified mark        
def update_square(grid, position, mark): 
    if grid[position[1]][position[0]] == mark: 
        grid[position[1]][position[0]] = 0
    else: 
        grid[position[1]][position[0]] = mark
        
    print(f'Placed {mark} at {position}')
    
    
# Similar to update_square, but doesn't replace marked squares    
def update_square_running(grid, position, mark): 
    if grid[position[1]][position[0]] == mark: 
        grid[position[1]][position[0]] = mark
    elif grid[position[1]][position[0]] == 2 and mark == 1:
        grid[position[1]][position[0]] == 2
    elif grid[position[1]][position[0]] == 1 and mark == 2:
        grid[position[1]][position[0]] == 1
    else: 
        grid[position[1]][position[0]] = mark
        
    print(f'Placed {mark} at {position}')
    


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
    pygame.K_l : (0, 3), 
    pygame.K_1 : (1, 1), 
    pygame.K_2 : (1, 2), 
    pygame.K_3 : (1, 3)
}

running = True
while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get(): 
        controller_index = 0
        
        pressed_keys = pygame.key.get_pressed()
        
        if event.type == pygame.QUIT:
            running = False
        # A key is pressed
        elif event.type == pygame.KEYDOWN and event.key in MOVEMENT_BUTTONS:
            if event.key not in key_states_movement:
                key_states_movement[event.key] = current_time
                last_action_time_movement[event.key] = 0
                print(f"Key {pygame.key.name(event.key)} pressed")
                update_cursor_position(*MOVEMENT_BUTTONS[event.key])
                
                for placement_key in PLACEMENT_BUTTONS:
                    if pressed_keys[placement_key]:
                        update_square(player_grid, player_1_cursor, PLACEMENT_BUTTONS[placement_key][1])
                
        elif event.type == pygame.KEYUP and event.key in MOVEMENT_BUTTONS:
            if event.key in key_states_movement:
                del key_states_movement[event.key]
                if event.key in last_action_time_movement:
                    del last_action_time_movement[event.key]
                print(f"Key {pygame.key.name(event.key)} released")
                
    
        elif event.type == pygame.KEYDOWN and event.key in PLACEMENT_BUTTONS:  
            key_states_placement[event.key] = (current_time, player_positions[PLACEMENT_BUTTONS[event.key][0]])
            last_action_time_placement[event.key] = (0, player_positions[PLACEMENT_BUTTONS[event.key][0]])
            print(f"Key {pygame.key.name(event.key)} pressed")
            # TODO: FIX THIS
            update_square(player_grid, player_1_cursor, PLACEMENT_BUTTONS[event.key][1])

        
        
    
    for key, press_time in list(key_states_movement.items()):
        elapsed = current_time - press_time
        pressed_keys = pygame.key.get_pressed()
        for placement_key in PLACEMENT_BUTTONS:
            if pressed_keys[placement_key]:
                update_square_running(player_grid, player_1_cursor, PLACEMENT_BUTTONS[placement_key][1])
        
        if elapsed >= DAS_DELAY:
            time_since_last_action = current_time - last_action_time_movement[key]
            if time_since_last_action >= DAS_INTERVAL:
                print(f"Action triggered for key: {pygame.key.name(key)}")
                update_cursor_position(*MOVEMENT_BUTTONS[key])
                last_action_time_movement[key] = current_time # update last action time
                

                
    
        

    # Draw everything
    draw_grid()
    draw_clues()

    # Check win condition
    if check_win():
        win_text = font.render("You Win!", True, BLACK)
        screen.blit(win_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
        #pygame.time.delay(10000)
        #exit()

    # Update display
    pygame.display.flip()


pygame.quit()
sys.exit()


# TODO get two grids
# TODO create random puzzles
# TODO get the cursor to work
# TODO Get the buttons to work

# TODO Build the UI
# TODO Get the supers/ADD/Destroy
# TODO Get the game to for loop to get multiple games
# TODO TIMER