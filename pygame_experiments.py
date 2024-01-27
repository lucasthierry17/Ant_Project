import pygame
from pygame.locals import *
import numpy as np

# Define constants
width, height = 800, 600
array_size = (60, 45)
pixel_size = 12

# Create a NumPy array filled with random values between 0 and 1
array = np.random.rand(*array_size)

def map_value_to_color(value):
    blue_component = int(value * 255)
    return (0, 0, blue_component)



# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))

# Create a Pygame surface from the NumPy array
surface = pygame.surfarray.pixels_blue(colored_array)
scaled_surface = pygame.transform.scale(surface, (width, height))

# Draw the surface onto the screen
screen.blit(scaled_surface, (0, 0))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.display.flip()
pygame.quit()
