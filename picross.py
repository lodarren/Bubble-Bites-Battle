import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
GRID_SIZE = 5  # 5x5 grid
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Picross")

# Example solution grid (1 for filled, 0 for empty)
solution_grid = [
    [1, 0, 1, 0, 1],
    [0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
]

# Player's current state
player_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Font for displaying row/column clues
font = pygame.font.SysFont(None, 36)


def draw_grid():
    """Draw the grid and current state."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE, row * CELL_SIZE

            # Draw cell background
            if player_grid[row][col] is True:
                color = BLUE
            elif player_grid[row][col] is False:
                color = GRAY
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw grid lines
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)


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
    return player_grid == solution_grid


# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle cell toggle
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            if row < GRID_SIZE and col < GRID_SIZE:
                if player_grid[row][col] is None:
                    player_grid[row][col] = True
                elif player_grid[row][col] is True:
                    player_grid[row][col] = False
                else:
                    player_grid[row][col] = None

    # Draw everything
    draw_grid()
    draw_clues()

    # Check win condition
    if check_win():
        win_text = font.render("You Win!", True, BLACK)
        screen.blit(win_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
