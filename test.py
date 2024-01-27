import pygame
from pygame.locals import *
import numpy as np

logical_width, logical_height = 100, 75 # size for the arrays
pixel_size = 10 # scales the screen up for visualisation
pheromone_decay_rate = 0.94 # between 0.9 and 0.99
max_pheromone_value = 255
width, height = logical_width * pixel_size, logical_height * pixel_size 
num_ants = 20
size_ant = 5 
FPS = 70 
pheri = 15 # this represents their sight of view
repulsion_distance = 5 # how far the ants will go towards the center
nest_position = np.array([width // 2, height // 2]) # set nest to the middle
VSYNC = True 

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

def update_pheromones(pheromones):
    """this function updates the pheromones. It takes in the array of the pheromones and returns an updated version. The values in the grid get smaller because of the decay rate"""
    pheromones *= pheromone_decay_rate
    return np.clip(pheromones, 0, max_pheromone_value) # ensures values stay within range 

def draw_ants(screen, ant_positions, size):
    # this function takes in the screen, the position and size of the ant and draws them in
    for ant_pos in ant_positions:
        pygame.draw.circle(screen, (255, 0, 0), ant_pos.astype(int), size) # draws the ants in red

def draw_pheromones(screen, pheromones, color, scale):
    # this function draws both of the pheromones grids
    surface = pygame.surfarray.make_surface(pheromones) 
    surface_array = pygame.surfarray.array3d(surface)
    surface_array[pheromones > 0] = color
    scaled_surface = pygame.transform.scale(surface, scale)
    screen.blit(scaled_surface, (0, 0))

def main(): 
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), vsync=VSYNC) # creates the screen

    pheromone_home = np.zeros((logical_width, logical_height), dtype=float) # sets up the pheromone grid for the home pheromones
    pheromone_food = np.zeros((logical_width, logical_height), dtype=float) # same for the food pheromones

    ant_positions = np.full((num_ants, 2), nest_position, dtype=float) # each ant starts at the position of the nest
    ant_directions = np.random.uniform(0, 360, size=num_ants) # for the first step, each ant gets a random direction

    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False

        pheromone_home = update_pheromones(pheromone_home)
        pheromone_food = update_pheromones(pheromone_food)

        ant_positions = move_ants(ant_positions, ant_directions)

        for ant_pos in ant_positions: # go through every ant and update their 
            logical_x, logical_y = ant_pos.astype(int) // pixel_size # scales the position down to the array in order to update the values of the grids
            logical_x = np.clip(logical_x, 0, logical_width - 1) # makes sure the values dont exceed the width of the board
            logical_y = np.clip(logical_y, 0, logical_height - 1) # same for the height
           
            x, y = logical_x * pixel_size, logical_y * pixel_size # scales the position back up for visualisation on the actual screen
            x, y = np.clip(x, 0, width - 1), np.clip(y, 0, height - 1) # makes sure the ants dont walk outside the board

            pheromone_home[logical_x, logical_y] += 30 # updates the value in the part of the home_pheromone grid
            pheromone_food[logical_x, logical_y] += 30 # same happens for the food grid

        pheromone_home = np.clip(pheromone_home, 0, max_pheromone_value) # makes sure the values stay in range of the max_pheromone value
        pheromone_food = np.clip(pheromone_food, 0, max_pheromone_value) # same here for the food

        draw_pheromones(screen, pheromone_home, [244,0 ,0], (width, height)) # blue fr the home pheromones
        draw_pheromones(screen, pheromone_food, [0, 255, 0], (width, height)) # green for the food pheromones

        draw_ants(screen, ant_positions, size_ant) 

        pygame.display.flip() # updates the entire display
        clock.tick(FPS) # regulates the frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
