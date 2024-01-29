import pygame
import numpy as np
from pygame.locals import *

# Dimensions of the array
logical_width, logical_height = 100, 75 # size for the arrays
pixel_size = 8 # scales the screen up for visualisation
width, height = logical_width * pixel_size, logical_height * pixel_size 
num_ants = 20
size_ant = 5 
FPS = 70 
pheri = 15 # this represents their sight of view
repulsion_distance = 5 # how far the ants will go towards the center
nest_position = np.array([width // 2, height // 2]) # set nest to the middle
home_pheromone = 200
ant_coordinates = []


def calculate_direction(start, target):
    """this function calculates the direction from the start to the target. It takes in the position from start and target as x and y coordinates and returns the direction as x and y coordinates"""

    direction_vector = target - start
    return direction_vector / np.linalg.norm(direction_vector)

def move_ants(positions, directions):
    """this function is represents the movement of the ants. Each ant has a pherisphere (pheri). It receives a degree in its pherisphere and walks a step in that direction. The direction is calculated by the sin and cos. """
    cos_directions = np.cos(np.radians(directions))
    sin_directions = np.sin(np.radians(directions))

    for ant in range(len(positions)):
        x, y = positions[ant]
        next_x = x + cos_directions[ant]
        next_y = y + sin_directions[ant]

        if 0 <= next_x <= width and 0 <= next_y <= height: # if the next step is within board boundaries
            x, y = next_x, next_y
        else: # next step would be outside the board
            direction_to_center = calculate_direction(np.array([x, y]), nest_position)
            directions[ant] = np.degrees(np.arctan2(direction_to_center[1], direction_to_center[0]))
            repulsion_vector = direction_to_center * repulsion_distance
            x += repulsion_vector[0] # updates the x-coordinate of the ant
            y += repulsion_vector[1] # same for the y coordinate

        positions[ant] = (x, y)
        directions[ant] += np.random.uniform(-pheri, pheri)

    return positions


def draw_pheromones(surface, pheromones, ant_coordinates):
    
    surface.fill((0, 0, 255, 0))
    for x, y in ant_coordinates:
            pheromones[x, y] = max(pheromones[x, y] - 1,  0)
            pygame.draw.rect(surface, (0, 0, 255, pheromones[x, y]), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))  



def draw_ants(screen, ant_positions, size):
    # this function takes in the screen, the position and size of the ant and draws them in
    for ant_pos in ant_positions:
        pygame.draw.circle(screen, (255, 0, 0), ant_pos.astype(int), size) # draws the ants in red

def main(): 
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
 # creates the screen

    ant_positions = np.full((num_ants, 2), nest_position, dtype=float) # each ant starts at the position of the nest
    ant_directions = np.random.uniform(0, 360, size=num_ants) # for the first step, each ant gets a random direction

    pheromones = np.full((logical_width, logical_height), 255, dtype=np.uint8)  # initial pheromone array


    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False

       
        ant_positions = move_ants(ant_positions, ant_directions)

        for ant_pos in ant_positions: # go through every ant and update their 
            logical_x, logical_y = ant_pos.astype(int) // pixel_size # scales the position down to the array in order to update the values of the grids
            logical_x = np.clip(logical_x, 0, logical_width - 1) # makes sure the values dont exceed the width of the board
            logical_y = np.clip(logical_y, 0, logical_height - 1) # same for the height

            pheromones[logical_x, logical_y] += home_pheromone
            ant_coordinates.append((logical_x, logical_y))

           
            x, y = logical_x * pixel_size, logical_y * pixel_size # scales the position back up for visualisation on the actual screen
            x, y = np.clip(x, 0, width - 1), np.clip(y, 0, height - 1) # makes sure the ants dont walk outside the board
            

        draw_pheromones(surface, pheromones, ant_coordinates)
        screen.fill((0, 0, 0))
        screen.blit(surface, (0, 0))  # Clear the screen to draw the new positions
        draw_ants(screen, ant_positions, size_ant) 


        pygame.display.flip() # updates the entire display
        clock.tick(FPS) # regulates the frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
