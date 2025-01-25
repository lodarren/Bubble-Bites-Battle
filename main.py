import pyglet
from pyglet.window import key, mouse

# Grid settings
GRID_SIZE = 5  # 5x5 grid
CELL_SIZE = 50  # Size of each cell
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE + 150  # Extra space for clues
WINDOW_HEIGHT = CELL_SIZE * GRID_SIZE

# Colors
GRID_COLOR = (200, 200, 200, 255)
FILLED_COLOR = (50, 150, 50, 255)
EMPTY_COLOR = (255, 255, 255, 255)
HOVER_COLOR = (200, 200, 250, 255)

# Puzzle (1 = filled, 0 = empty)
PUZZLE = [
    [1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 1],
    [1, 1, 0, 1, 0],
]

# Hints (row and column)
ROW_HINTS = [[2], [2], [2], [3], [1, 1]]
COL_HINTS = [[2], [1, 2], [1, 1], [1, 1], [3]]

# Pyglet window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Picross")

# Store cell states (None = unmarked, True = filled, False = empty)
cell_states = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Current hovered cell
hovered_cell = None


def draw_grid():
    """Draw the grid and cell states."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = WINDOW_HEIGHT - (row + 1) * CELL_SIZE

            # Determine cell color
            if hovered_cell == (row, col):
                color = HOVER_COLOR
            elif cell_states[row][col] is True:
                color = FILLED_COLOR
            elif cell_states[row][col] is False:
                color = EMPTY_COLOR
            else:
                color = (255, 255, 255, 255)

            # Draw the cell
            pyglet.graphics.draw(
                4, pyglet.gl.GL_QUADS,
                ("v2f", [x, y, x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE, x, y + CELL_SIZE]),
                ("c4B", color * 4)
            )

            # Draw the cell border
            pyglet.graphics.draw(
                4, pyglet.gl.GL_LINE_LOOP,
                ("v2f", [x, y, x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE, x, y + CELL_SIZE]),
                ("c4B", GRID_COLOR * 4)
            )


def draw_hints():
    """Draw row and column hints."""
    # Row hints
    for i, hints in enumerate(ROW_HINTS):
        x = GRID_SIZE * CELL_SIZE + 10
        y = WINDOW_HEIGHT - (i * CELL_SIZE + CELL_SIZE // 2)
        label = pyglet.text.Label(
            " ".join(map(str, hints)),
            font_size=12, x=x, y=y, anchor_x="left", anchor_y="center"
        )
        label.draw()

    # Column hints
    for i, hints in enumerate(COL_HINTS):
        x = i * CELL_SIZE + CELL_SIZE // 2
        y = WINDOW_HEIGHT - GRID_SIZE * CELL_SIZE - 20
        label = pyglet.text.Label(
            "\n".join(map(str, hints)),
            font_size=12, x=x, y=y, anchor_x="center", anchor_y="top"
        )
        label.draw()


@window.event
def on_draw():
    """Render the game."""
    window.clear()
    draw_grid()
    draw_hints()


@window.event
def on_mouse_motion(x, y, dx, dy):
    """Update hovered cell."""
    global hovered_cell
    col = x // CELL_SIZE
    row = (WINDOW_HEIGHT - y) // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        hovered_cell = (row, col)
    else:
        hovered_cell = None


@window.event
def on_mouse_press(x, y, button, modifiers):
    """Handle cell marking."""
    if hovered_cell:
        row, col = hovered_cell
        if button == mouse.LEFT:
            cell_states[row][col] = not cell_states[row][col]
        elif button == mouse.RIGHT:
            cell_states[row][col] = False


def run():
    pyglet.app.run()


if __name__ == "__main__":
    run()
