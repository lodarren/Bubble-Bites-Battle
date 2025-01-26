import pygame
import sys
import endgame
import random
import puzzles

# Initialize Pygame
pygame.init()


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
DAS_DELAY = 5
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
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
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
    pygame.draw.rect(screen, RED, pygame.Rect(METER1_OFFSET[0], METER1_OFFSET[1], WINDOW_WIDTH // 2 * player_meters[0], 3 * CELL_SIZE))
    pygame.draw.rect(screen, BLUE, pygame.Rect(METER2_OFFSET[0] + (WINDOW_WIDTH // 2 * (1 - player_meters[1])), METER2_OFFSET[1], WINDOW_WIDTH // 2 * player_meters[1], 3 * CELL_SIZE))
    


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
    
# Ultimate attack
def player_ult(character, player):
    global player_meters
    if player_meters[player] == 1: 
        print(f'PLAYER {player} SUPER')
        player_meters[player] = 0
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
        player_meters[1] += 0.2
    elif player == 1: 
        player_scores[1] += 1
        player_meters[0] += 0.2
    
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

def picross_game():
    running = True
    while running:
        screen.fill(WHITE)
        current_time = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get(): 
            pressed_keys = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key in MOVEMENT_BUTTONS:
                if event.key not in key_states_movement:
                    key_states_movement[event.key] = current_time
                    last_action_time_movement[event.key] = 0
                    print(f"Key {pygame.key.name(event.key)} pressed")
                    #update_cursor_position(*MOVEMENT_BUTTONS[event.key])
                    
                    for placement_key in PLACEMENT_BUTTONS:
                        if pressed_keys[placement_key]:
                            update_square_running(player_grids[PLACEMENT_BUTTONS[placement_key][0]], player_positions[PLACEMENT_BUTTONS[placement_key][0]], PLACEMENT_BUTTONS[placement_key][1])
                    
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
                update_square(player_grids[PLACEMENT_BUTTONS[event.key][0]], player_positions[PLACEMENT_BUTTONS[event.key][0]], PLACEMENT_BUTTONS[event.key][1])
                print(player_grids[PLACEMENT_BUTTONS[event.key][0]])

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
                    update_square_running(player_grids[PLACEMENT_BUTTONS[placement_key][0]], player_positions[PLACEMENT_BUTTONS[placement_key][0]], PLACEMENT_BUTTONS[placement_key][1])
            
            if elapsed >= DAS_DELAY:
                time_since_last_action = current_time - last_action_time_movement[key]
                if time_since_last_action >= DAS_INTERVAL:
                    print(f"Action triggered for key: {pygame.key.name(key)}")
                    update_cursor_position(*MOVEMENT_BUTTONS[key])
                    last_action_time_movement[key] = current_time 

        # Draw everything
        draw_grid()
        draw_meter()
        draw_clues()
        draw_score()
        

        # Check win condition
        global player_1_win_flag, player_2_win_flag
        if check_win(player_grids[0], solution_grid_1) and not player_1_win_flag:
            player_1_win_flag = True
            update_scores(0)
            restart_puzzle(0)
            print(player_grids[0])
            player_1_win_flag = False
        elif check_win(player_grids[1], solution_grid_2) and not player_2_win_flag:
            player_2_win_flag = True
            update_scores(1)
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
                    print("i ran")
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


# TODO Build the UI
# TODO Get the supers/ADD/Destroy
# TODO Get the game to for loop to get multiple games
# TODO TIMER