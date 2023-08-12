import pygame
import math

# Initialize Pygame
pygame.init()

# Window dimensions
width = 800
height = 600

# Create the display surface
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotating Donut")

                            # Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Donut properties
radius = 100
thickness = 20
rotating_speed = 0.03
color_change_speed = 0.01

# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Calculate donut position
    angle = pygame.time.get_ticks() * rotating_speed
    x = int(width / 2 + math.cos(angle) * radius)
    y = int(height / 2 + math.sin(angle) * radius)

    # Change color
    color = (int(math.sin(angle * color_change_speed) * 127) + 128,
             int(math.sin(angle * color_change_speed + 2 * math.pi / 3) * 127) + 128,
             int(math.sin(angle * color_change_speed + 4 * math.pi / 3) * 127) + 128)

    # Draw the donut
    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, BLACK, (x, y), radius - thickness)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
