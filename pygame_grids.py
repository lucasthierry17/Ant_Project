import pygame
from pygame.locals import *
import numpy as np

pygame.init()   
clock = pygame.time.Clock()

width, height = 800, 600 
pheromone_decay_rate = 0.94 # please set between 0.9 and 0.99
max_pheromone_value = 255
num_ants = 100
size_ant = 5 # sets the size of the ant
FPS = 250 # sets the frames per second (higher produces a faster visualisation)
pheri = 20 # set a degree for the pherisphere of the ant (direction in which the ants are walking)
repulsion_distance = 5 # distance for moving towards the center
nest_position = np.array([width//2, height//2]) 

def calculate_direction(start, target):
        direction_vector = target - start
        direction = direction_vector / np.linalg.norm(direction_vector)
        return direction

def movement(positions, directions):
    """this function is for the movement of the ants. First, the ants receive a random direction (self.directions). After the first step, they have a angle of view (set with pheri). They walk randomly in this site of view. For each step they get a direction and take a step in that direction. If they enter the edge_region, they turn around and take the next step in the opposite direction
    """
    cos_directions = np.cos(np.radians(directions))  # chooses the direction on the x axis
    sin_directions = np.sin(np.radians(directions))  # same on the y axis

    for ant in range(len(positions)):
        x, y = positions[ant]
        
        next_x = x + cos_directions[ant]  # computes the next x coordinates
        next_y = y + sin_directions[ant]  # computes the next y coordinates

        if 0 <= next_x <= width and 0 <= next_y <= height:
                x = next_x
                y = next_y
        else:  
             # If the next step of the ant is outside of our board, update direction towards the center
            direction_to_center = calculate_direction(np.array([x, y]), nest_position)
        
            # Update direction to move towards the center
            directions[ant] = np.degrees(np.arctan2(direction_to_center[1], direction_to_center[0]))

            # Move away from the border by repulsion_distance
            repulsion_vector = direction_to_center * repulsion_distance
            x += repulsion_vector[0]
            y += repulsion_vector[1]
        
        #x = np.clip(x, 0, width - 1) # ensures that x is withtin the width of the board
        #y = np.clip(y, 0, height - 1) # same for y and the height

        # check if the ants are going outside
        positions[ant] = (x, y)
        directions[ant] += np.random.uniform(-pheri, pheri)

    return positions

# pheromone grid for the food and home pheromones
pheromone_home = np.zeros((width, height), dtype=float)
pheromone_food = np.zeros((width, height), dtype=float)

ant_positions = np.full((num_ants, 2), (width // 2, height // 2), dtype=float) # sets the starting positions for the ants
ant_directions = np.random.uniform(0, 360, size=num_ants) # sets the starting direction


screen = pygame.display.set_mode((width, height)) # creates our screen with width and height

# Run the simulation loop
go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False

    # Update pheromones
    pheromone_home *= pheromone_decay_rate
    pheromone_food *= pheromone_decay_rate

    # Place pheromones where ants have been
    ant_positions = movement(ant_positions, ant_directions)
    for ant_pos in ant_positions:
        x, y = ant_pos.astype(int)  # Convert positions to integers
        pheromone_home[x, y] += 30  # Increase pheromone value
        pheromone_food[x, y] += 30  # Increase pheromone value

    # Clip pheromone values to the maximum allowed value
    np.clip(pheromone_home, 0, max_pheromone_value, out=pheromone_home)
    np.clip(pheromone_food, 0, max_pheromone_value, out=pheromone_food)

    # Create Pygame surfaces from numpy arrays
    surface_home = pygame.surfarray.make_surface(pheromone_home)
    surface_food = pygame.surfarray.make_surface(pheromone_food)

    # Display the surfaces
    screen.blit(surface_home, (0, 0)) # draws the home_pheromones on to the screen at position (0, 0)
    screen.blit(surface_food, (0, 0)) # same for the food pheromones
    

    for ant_pos in ant_positions:
        pygame.draw.circle(screen, (255, 0, 0), ant_pos.astype(int), size_ant) # draws red ants as x 

    pygame.display.flip() # updates the display
    clock.tick(FPS) # used to control the frames per second

pygame.quit()





