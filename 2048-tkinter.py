import random
import tkinter as tk
from tkinter import messagebox

# Constants
GRID_SIZE = 4
CELL_SIZE = 80
BACKGROUND_COLOR = "#222222"
EMPTY_CELL_COLOR = "#444444"
FONT = ("Verdana", 40, "bold")
TITLE_FONT = ("Verdana", 60, "bold")
PADDING = 20
GRID_PADDING = 10

# Function to create a new grid
def create_grid(size):
    grid = [[0] * size for _ in range(size)]
    return grid

# Function to add a new tile to the grid
def add_new_tile(grid):
    size = len(grid)
    empty_cells = []
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 0:
                empty_cells.append((i, j))
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Function to initialize the game
def start_game():
    global grid, score, high_score
    grid = create_grid(GRID_SIZE)
    score = 0
    high_score = 0
    add_new_tile(grid)
    add_new_tile(grid)
    update_grid()
    update_scores()

# Function to update the grid
def update_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = grid[i][j]
            cell_color = get_tile_color(cell_value)
            cell_text = str(cell_value) if cell_value else ""
            tiles[i][j].configure(text=cell_text, bg=cell_color)

# Function to update the scores
def update_scores():
    score_label.configure(text=f"Score: {score}")
    high_score_label.configure(text=f"High Score: {high_score}")

# Function to get the tile color based on the value
def get_tile_color(value):
    colors = {
        0: EMPTY_CELL_COLOR,
        2: "#9c8061",
        4: "#9c6742",
        8: "#f59563",
        16: "#f67c5f",
        32: "#f65e3b",
        64: "#edcf72",
        128: "#edcc61",
        256: "#edc850",
        512: "#edc53f",
        1024: "#edc22e",
        2048: "#edc22e",
    }
    return colors.get(value, "#ff0000")

# Function to handle key events
def key_pressed(event):
    key = event.keysym.lower()
    if key in ('w', 'up'):
        move_tiles('w')
    elif key in ('a', 'left'):
        move_tiles('a')
    elif key in ('s', 'down'):
        move_tiles('s')
    elif key in ('d', 'right'):
        move_tiles('d')
    add_new_tile(grid)
    update_grid()
    update_scores()
    if is_game_over():
        game_over()


# Function to move the tiles
def move_tiles(direction):
    if direction == 'w':
        move_up()
    elif direction == 'a':
        move_left()
    elif direction == 's':
        move_down()
    elif direction == 'd':
        move_right()

def move_up():
    for j in range(GRID_SIZE):
        for i in range(1, GRID_SIZE):
            move_tile(i, j, -1, 0)

def move_left():
    for i in range(GRID_SIZE):
        for j in range(1, GRID_SIZE):
            move_tile(i, j, 0, -1)

def move_down():
    for j in range(GRID_SIZE):
        for i in range(GRID_SIZE - 2, -1, -1):
            move_tile(i, j, 1, 0)

def move_right():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 2, -1, -1):
            move_tile(i, j, 0, 1)

# Function to move a single tile in a given direction
def move_tile(i, j, di, dj):
    while 0 <= i + di < GRID_SIZE and 0 <= j + dj < GRID_SIZE:
        if grid[i + di][j + dj] == 0:
            grid[i + di][j + dj] = grid[i][j]
            grid[i][j] = 0
            i, j = i + di, j + dj
        elif grid[i + di][j + dj] == grid[i][j]:
            grid[i + di][j + dj] *= 2
            grid[i][j] = 0
            global score
            score += grid[i + di][j + dj]
            break
        else:
            break

# Function to check if the game is over
def is_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if i > 0 and grid[i][j] == grid[i - 1][j]:
                return False
            if j > 0 and grid[i][j] == grid[i][j - 1]:
                return False
    return True

# Function to end the game
def game_over():
    global high_score
    if score > high_score:
        high_score = score
    messagebox.showinfo("Game Over", f"Score: {score}\nHigh Score: {high_score}")
    game_window.destroy()

# Create the game window
game_window = tk.Tk()
game_window.title("2048")
game_window.configure(bg=BACKGROUND_COLOR)

# Create the title label
title_label = tk.Label(game_window, text="2048", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg="#ffffff")
title_label.pack(pady=PADDING)

# Create the score labels
score_frame = tk.Frame(game_window, bg=BACKGROUND_COLOR)
score_frame.pack()

score_label = tk.Label(score_frame, text="Score: 0", font=FONT, bg=BACKGROUND_COLOR, fg="#ffffff")
score_label.pack(side=tk.LEFT, padx=PADDING)

high_score_label = tk.Label(score_frame, text="High Score: 0", font=FONT, bg=BACKGROUND_COLOR, fg="#ffffff")
high_score_label.pack(side=tk.RIGHT, padx=PADDING)

# Create the frame to hold the tiles
grid_frame = tk.Frame(game_window, bg=BACKGROUND_COLOR)
grid_frame.pack()

# Create the tiles as labels in the grid frame
tiles = []
for i in range(GRID_SIZE):
    grid_frame.columnconfigure(i, weight=1, minsize=CELL_SIZE)
    grid_frame.rowconfigure(i, weight=1, minsize=CELL_SIZE)
    row = []
    for j in range(GRID_SIZE):
        tile_label = tk.Label(grid_frame, width=6, height=3, font=FONT, bg=EMPTY_CELL_COLOR, fg="#ffffff")
        tile_label.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING, sticky="nsew")
        row.append(tile_label)
    tiles.append(row)

# Create the "Created by capt_ph03nix" tag label
tag_label = tk.Label(game_window, text="Created by capt_ph03nix", font=("Verdana", 10), bg=BACKGROUND_COLOR, fg="#ffffff")
tag_label.pack(side=tk.BOTTOM, pady=PADDING)

# Configure the grid frame to resize with the window
game_window.grid_rowconfigure(0, weight=1)
game_window.grid_columnconfigure(0, weight=1)

# Add padding to the bottom of the game window
game_window.configure(pady=PADDING)

# Start the game
start_game()

# Bind the key press event to the game window
game_window.bind("<Key>", key_pressed)

# Run the game
game_window.mainloop()

# Function to move a single tile in a given direction with animation
def move_tile(i, j, di, dj):
    # Calculate the target position for the tile
    target_i, target_j = i, j
    while 0 <= target_i + di < GRID_SIZE and 0 <= target_j + dj < GRID_SIZE and grid[target_i + di][target_j + dj] == 0:
        target_i, target_j = target_i + di, target_j + dj

    # If the tile doesn't need to move, return
    if target_i == i and target_j == j:
        return

    # Update the tile's position gradually with a time delay
    step_i, step_j = di, dj
    while i != target_i or j != target_j:
        game_window.update_idletasks()  # Update the window
        grid[i][j], grid[i + di][j + dj] = grid[i + di][j + dj], grid[i][j]
        i, j = i + di, j + dj
        update_grid()
        game_window.after(50)  # Add a small delay (50 milliseconds)