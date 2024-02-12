import pygame
import numpy as np
from pygame.locals import *
from math import pi, sin, cos, atan2, radians, degrees
from random import randint

logical_width, logical_height = 150, 100# size for the pheromone array
pixel_size = 6                          # scales the screen up for visualization
width, height = logical_width * pixel_size, logical_height * pixel_size # actual size of the screen
num_ants = 50                           # number of ants
size_ant = 5                            # size of the ant for drawing
FPS = 10                                # frames per second
pheri = 15                              # this represents their sight of view
nest_position = np.array([width // 2, height // 2])  # set nest to the middle
home_pheromone = 255                    # value of intensity added to the position
food_pheromone = 255                    # value of intensity added to the position
step_size = 6                           # step_size of the ants
decay_rate = 5                          # value is subtracted from the intensity in position x, y
num_food = 200                          # number of food items in the food source
radius = 7                              # radius of the food source
size_food = 5                           # size of each food item
VSYNC = True
SHOWFPS = True

class Ants:
    """This class is for the ants. It contains the movement of the ants."""
    def __init__(self):
        self.has_food = np.zeros((num_ants), dtype=bool)

    def calculate_direction(self, start, target):
        """Calculates the direction from the start to the target.
        Parameters: start, target as coordinates.
        Returns: vector"""
        direction_vector = target - start
        return direction_vector / np.linalg.norm(direction_vector)

    def move_ants(self, positions, directions):
        """
        Update the positions and directions of the ants. Iterates through every ant.
        Parameters: positions (np.array): array for the positions
                    directions (np.aray): array for the directions
        Returns: positions of every ant
        """

        cos_directions = step_size * np.cos(np.radians(directions))
        sin_directions = step_size * np.sin(np.radians(directions))

        for ant in range(len(positions)): # iterate through each ant
            x, y = positions[ant]
            next_x = x + cos_directions[ant] # update the x_coordinate
            next_y = y + sin_directions[ant] # same for the y coordinate

            if self.has_food[ant] or not (0 <= next_x <= width and 0 <= next_y <= height): # if the ant has food or next step is outside the board

                direction_to_nest = self.calculate_direction(np.array([x, y]), nest_position) # calculate direction to nest
                directions[ant] = np.degrees(np.arctan2(direction_to_nest[1], direction_to_nest[0]))  # Move in the direction of the nest
                x += cos_directions[ant] 
                y += sin_directions[ant]
                distance_to_nest = np.linalg.norm(np.array([x, y]) - nest_position) # calculates the distance to the nest
                if distance_to_nest < vis.nest_size: # if ant reaches the nest...
                    self.has_food[ant] = False # set status to no food
                    directions[ant] += 180 # turn around
            
            else: # ant does not have food and next step is within board boundaries
                x, y = next_x, next_y

            positions[ant] = (x, y)
            directions[ant] += np.random.uniform(-pheri, pheri) # ant receives a random direction for the next step

        return positions
    



class Food:
    """
    Food_sources are being created with small green circles at random position (inside the board and not on top of the nest).
    """
    def __init__(self, num_food, radius, min_distance=400):
        self.num_food = num_food
        self.radius = radius
        self.min_distance = min_distance
        self.center = None

    def generate_positions(self):
        """ 
        Generates the positions for the food.
        Parameters: -
        Returns: positions"""
        # Generate random angles to distribute food positions uniformly in a circle
        angles = np.linspace(0, 2 * np.pi, self.num_food)
        radii = np.sqrt(np.random.uniform(0, 1, self.num_food)) * self.radius
        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        # randomly choose x and y coordinates for the center of the food source, also makes sure the food does not appear outside of the screen or on the nest. 
        x_center = np.random.randint(50, width // 3)
        y_center = np.random.randint(50, height - 50)
        self.center = x_center, y_center # center of the food source

        # return the final and scaled positions of the food items
        self.positions = np.column_stack((x, y)) * pixel_size + self.center

        return self.positions


class Drawing:
    """This class is for the drawing on the screen. We have a screen and a surface, which is being drawn onto the screen. Everything is drawn directly onto the screen, except of the pheromones, they are being drawn on our surface"""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height))
        self.food_positions = Food(num_food, radius).generate_positions()
        self.font = pygame.font.Font(None, 30)


    def draw_pheromones(self, surface, home_pheromones, food_pheromones):
        """This function draws the pheromones. 
        Parameters: surface (pygame.Surface), home and food_pheromones (np.arrays)
        Returns: Draws small rectangles on the screen, the values for the color are being stored inside two numpy arrays (food_pheromones and home_pheromones). The pheromones disappear through the substraction of the decay rate each step
        """
        for (x, y), intensity in np.ndenumerate(home_pheromones): # iterate through the array
            home_pheromones[x, y] = max(intensity - decay_rate, 0) # clip values to 0-255 and substract the decay_rate every step

        for (x, y), intensity in np.ndenumerate(food_pheromones): # same for the food_pheromones
            food_pheromones[x ,y] = max(intensity - decay_rate, 0)
            pygame.draw.rect(surface, (0, food_pheromones[x, y], home_pheromones[x, y]), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            # draws the value from the home_pheromones as b value and the value from the food_pheromones as the g value, with pixel_size as size


    def draw_food(self, size_food):
        """
        This function draws the food_sources at the generated location. 
        Parameters: size_food (radius of the food)
        Returns: draws the food on to the screen
        """
        for food_pos in self.food_positions:
            pygame.draw.circle(self.screen, (0, 255, 0), food_pos.astype(int), size_food)


    def draw_ants(self, ant_positions, size):
        """
        The ants are drawn on to the screen.
        Parameters: ant_positions (np.array), size (size of the ants)
        Returns: Draws the ants on to the screen
        """
        
        for ant_pos in ant_positions:
            
            pygame.draw.circle(self.screen, (255, 0, 0), ant_pos.astype(int), size)  # draws the ants without food in red

    def draw_nest(self):
        """
        This function draws the nest onto the screen at the given position
        Parameters: nest_size 
        Returns: Draws the nest on to the screen
        """

        self.nest_size = 30
        pygame.draw.circle(self.screen, (121, 61, 0), nest_position, self.nest_size)

    def draw_on_screen(self):
        """
        The different functions are being called in the order we want to appear the things on thte screen.
        """
        self.screen.fill((0, 0, 0))
        self.draw_pheromones(self.surface, main.home_pheromones, main.food_pheromones)
        self.screen.blit(self.surface, (0, 0))
        self.draw_food(size_food)
        self.draw_ants(main.ant_positions, size_ant)
        self.draw_nest()
        if SHOWFPS : self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, [0,200,0]), (8, 8))
        pygame.display.flip()
        self.clock.tick(FPS)


class Run:
    """
    This class runs the loop
    """

    def __init__(self):
        self.ants = Ants()
        self.ant_positions = np.full((num_ants, 2), nest_position, dtype=float)
        self.ant_directions = np.random.uniform(0, 360, size=num_ants)
        self.home_pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)
        self.home_pheromones = pg.
        self.food_pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)
        self.go = True

    def main(self):
        """
        Handles the exit and goes through every ant. 
        """
        # if we want to close the program
        while self.go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.go = False

            self.ant_positions = self.ants.move_ants(self.ant_positions, self.ant_directions) # ants take a step with the move_ants function

            for ant_pos, has_food in zip(self.ant_positions, self.ants.has_food): # iterates through the positions and the food_status
                logical_x = np.clip(ant_pos[0].astype(int) // pixel_size, 0, logical_width - 1)  # scales down the size of the screen to a smaller array for the width
                logical_y = np.clip(ant_pos[1].astype(int) // pixel_size, 0, logical_height - 1) # same for the height

                if not has_food: # if the ant does not have food --> spread home_pheromones
                    for food_pos in vis.food_positions: # Check if an ant is inside a food position
                        distance_to_food = np.linalg.norm(ant_pos - food_pos)
                        if distance_to_food < size_food: # is the distance is smaller then the radius of the food, update has_food to true
                            self.ants.has_food[np.where((self.ant_positions == ant_pos).all(axis=1))] = True
                    self.home_pheromones[logical_x, logical_y] += home_pheromone # updates the pheromone value

                else: # ant has food
                    self.food_pheromones[logical_x, logical_y] += food_pheromone # updates the food_pheromone value

                    
            vis.draw_on_screen() # updates the screen each step


vis = Drawing()
main = Run()

if __name__ == "__main__":
    main.main() 