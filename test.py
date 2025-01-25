import pyglet
from pyglet.shapes import Rectangle

window = pyglet.window.Window(800, 600, "Picross")
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()

ROWS, COLS = 10, 10
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]  # 0: empty, 1: filled, -1: marked
CELL_SIZE = 40  # Size of each cell in pixels


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = (255, 255, 255) if grid[row][col] == 0 else (0, 0, 0)
            rect = Rectangle(x, y, CELL_SIZE, CELL_SIZE, color=color, batch=batch)
            rect.opacity = 200  # Make it slightly transparent

@window.event
def on_draw():
    window.clear()
    draw_grid()
    batch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        if grid[row][col] == 0:  # Empty cell
            grid[row][col] = 1  # Fill it
        elif grid[row][col] == 1:  # Filled cell
            grid[row][col] = -1  # Mark it
        else:  # Marked cell
            grid[row][col] = 0  # Reset it

row_clues = [[3], [1, 1], [5], [], [4]]
col_clues = [[2], [3], [1, 1], [3], [5]]

# Render clues
def draw_clues():
    for i, clue in enumerate(row_clues):
        label = pyglet.text.Label(
            text=" ".join(map(str, clue)),
            x=-50, y=i * CELL_SIZE + CELL_SIZE // 2,
            anchor_x="right", anchor_y="center",
            batch=batch
        )
    for i, clue in enumerate(col_clues):
        label = pyglet.text.Label(
            text=" ".join(map(str, clue)),
            x=i * CELL_SIZE + CELL_SIZE // 2, y=600,
            anchor_x="center", anchor_y="bottom",
            batch=batch
        )

solution = [
    [0, 1, 1, 1, 0],
    [1, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
]

def check_solution():
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1 and solution[r][c] != 1:
                return False
    return True

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ENTER:
        if check_solution():
            print("Congratulations! Puzzle solved!")
        else:
            print("Incorrect solution. Try again!")
