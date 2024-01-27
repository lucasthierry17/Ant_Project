import time
import pygame
import numpy as np
# Initialize Pygame
pygame.init()
clock=pygame.time.Clock()

FPS=60
#Scale of pixel: Bord width //PXL
PXL=5
width =1000
height = 900

#Ant and Pheromone size in px
num_ants = 10
pheromone_width = 3
# Define constants
ant_size=5
pheromone_decay_rate = 0.99
max_pheromone_value = 255

def movement(positions, directions):
    """this function is for the movement of the ants. First, the ants receive a random direction (self.directions). After the first step, they have a angle of view (set to -40 to 40 degrees). They walk randomly in this site of view. For each step they get a direction (-40 to 40 degrees) and take a step in that direction. If they enter the edge_region, they turn around and take the next step in the opposite direction
    Input: edge_turn_region
    """
    cos_directions = np.cos(np.radians(directions))  # chooses the direction on the x axis
    sin_directions = np.sin(np.radians(directions))  # same on the y axis

    for ant in range(len(positions)):
        x, y = positions[ant]
        x = x + cos_directions[ant]  # computes the next x coordinates
        y = y + sin_directions[ant]  # computes the next y coordinates
        # Clip ant positions to be within the board boundaries
        x = np.clip(x, 0, width//PXL - 1)
        y = np.clip(y, 0, height//PXL - 1)

        positions[ant] = (x, y)
        directions[ant] += np.random.uniform(-20, 20)

    return positions

# Create a numpy array to represent the pheromone grid
pheromone_home = np.zeros((width//PXL, height//PXL), dtype=float)

# Create initial positions and directions for ants
# Set all ants to start in the middle of the window
ant_positions = np.full((num_ants, 2), (width/PXL // 2, height/PXL // 2), dtype=float)
ant_directions = np.random.uniform(0, 360, size=num_ants)

# Create a Pygame screen
screen = pygame.display.set_mode((width//PXL, height//PXL),pygame.SCALED,pygame.RESIZABLE)
pygame.display.set_caption("Pheromone Grid Visualization")

# Run the simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Place pheromones where ants have been
    ant_positions = movement(ant_positions, ant_directions)
    for ant_pos in ant_positions:
        x, y = ant_pos.astype(int)  # Convert positions to integers
        pheromone_home[x, y] += 1  # Increase pheromone value
    
    # Update pheromones
    pheromone_home *=  pheromone_decay_rate
    #pheromone_food *= pheromone_decay_rate
    # Clip pheromone values to the maximum allowed value
    np.clip(pheromone_home, 0, max_pheromone_value, out=pheromone_home)


    #green_color=(0,255,0)
    #surface_home = pygame.surfarray.make_surface(np.stack([np.zeros_like(pheromone_home), pheromone_home, np.zeros_like(pheromone_home)], axis=-1))
    surface_home = pygame.surfarray.make_surface(pheromone_home)


    
    # Spread pheromones in a square region around the ant position
    for ant_pos in ant_positions:
        x,y = ant_pos.astype(int)

        x_start, x_end = max(0, x - pheromone_width // 2), min(width, x + pheromone_width // 2)
        y_start, y_end = max(0, y - pheromone_width // 2), min(height, y + pheromone_width // 2)

        # Increase pheromone values within the specified region
        pheromone_home[x_start:x_end, y_start:y_end] += 1

        screen.blit(surface_home, (0, 0))

         

    for ant_pos in ant_positions:
        pygame.draw.circle(screen, (255, 0, 0), ant_pos.astype(int), ant_size)
    #check_border()
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()




