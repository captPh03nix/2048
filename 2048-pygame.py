import pygame
import random

# Constants
GRID_SIZE = 4
CELL_SIZE = 80
BACKGROUND_COLOR = (34, 34, 34)
EMPTY_CELL_COLOR = (68, 68, 68)
FONT_SIZE = 40
TITLE_FONT_SIZE = 60
PADDING = 20

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
    global grid, score, high_score, font, title_font
    grid = create_grid(GRID_SIZE)
    score = 0
    high_score = 0
    add_new_tile(grid)
    add_new_tile(grid)
    font = pygame.font.Font(None, FONT_SIZE)
    title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
    draw_game()

# Function to update the grid
def update_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = grid[i][j]
            cell_color = get_tile_color(cell_value)
            cell_text = str(cell_value) if cell_value else ""
            cell_label = font.render(cell_text, True, cell_color)
            x_pos = PADDING + j * CELL_SIZE
            y_pos = PADDING * 2 + TITLE_FONT_SIZE + i * CELL_SIZE
            screen.blit(cell_label, (x_pos, y_pos))

# Function to get the tile color based on the value
def get_tile_color(value):
    colors = {
        0: EMPTY_CELL_COLOR,
        2: (156, 128, 97),
        4: (156, 103, 66),
        8: (245, 149, 99),
        16: (246, 124, 95),
        32: (246, 94, 59),
        64: (237, 207, 114),
        128: (237, 204, 97),
        256: (237, 200, 80),
        512: (237, 197, 63),
        1024: (237, 194, 46),
        2048: (237, 194, 46),
    }
    return colors.get(value, (255, 0, 0))

# Function to move a single tile in a given direction with animation
def move_tile(i, j, di, dj):
    # Calculate the target position for the tile
    target_i, target_j = i, j
    while 0 <= target_i + di < GRID_SIZE and 0 <= target_j + dj < GRID_SIZE and grid[target_i + di][target_j + dj] == 0:
        target_i, target_j = target_i + di, target_j + dj

    # If the tile doesn't need to move, return
    if target_i == i and target_j == j:
        return

    # Update the tile's position gradually with animation
    step_i, step_j = di, dj
    animation_speed = 8  # Increase for faster animation
    for _ in range(animation_speed):
        grid[i][j], grid[i + di][j + dj] = grid[i + di][j + dj], grid[i][j]
        i, j = i + di, j + dj
        draw_game()
        pygame.time.delay(50)  # Add a small delay (50 milliseconds)

# Function to move the tiles
def move_tiles(direction):
    if direction == 'w':
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                move_tile(i, j, -1, 0)
    elif direction == 'a':
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                move_tile(i, j, 0, -1)
    elif direction == 's':
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 2, -1, -1):
                move_tile(i, j, 1, 0)
    elif direction == 'd':
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 2, -1, -1):
                move_tile(i, j, 0, 1)

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
    pygame.display.set_caption("2048 - Game Over")
    pygame.time.delay(500)
    pygame.display.set_caption("2048")
    draw_game()

# Function to update the scores
def update_scores():
    score_label = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_label = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_label, (PADDING, PADDING + TITLE_FONT_SIZE))
    screen.blit(high_score_label, (PADDING + 200, PADDING + TITLE_FONT_SIZE))

# Function to draw the game screen
def draw_game():
    screen.fill(BACKGROUND_COLOR)
    title_label = title_font.render("2048", True, (255, 255, 255))
    screen.blit(title_label, (PADDING, PADDING))
    update_scores()
    update_grid()
    pygame.display.update()

# Initialize Pygame
pygame.init()

# Create the game window
window_width = GRID_SIZE * CELL_SIZE + PADDING * 2
window_height = GRID_SIZE * CELL_SIZE + PADDING * 3 + TITLE_FONT_SIZE
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("2048")

# Start the game
start_game()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key in (pygame.K_w, pygame.K_UP):
                move_tiles('w')
            elif key in (pygame.K_a, pygame.K_LEFT):
                move_tiles('a')
            elif key in (pygame.K_s, pygame.K_DOWN):
                move_tiles('s')
            elif key in (pygame.K_d, pygame.K_RIGHT):
                move_tiles('d')
            add_new_tile(grid)
            draw_game()
            if is_game_over():
                game_over()
