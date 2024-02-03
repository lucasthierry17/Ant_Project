import pygame
import numpy as np
from pygame.locals import *


logical_width, logical_height = 150, 100  # size for the arrays
pixel_size = 6  # scales the screen up for visualization
width, height = logical_width * pixel_size, logical_height * pixel_size
num_ants = 20 # number of ants
size_ant = 5 # size of the ant for drawing
FPS = 250 # frames per second
pheri = 15  # this represents their sight of view
repulsion_distance = 5  # how far the ants will go towards the center
nest_position = np.array([width // 2, height // 2])  # set nest to the middle
home_pheromone = 255 # value of intensity added to the position
food_pheromones = 255
step_size = 4 # step_size of the ants
decay_rate = 1 # value is subtracted from the intensity in position x, y
num_food = 200 # number of food items in the food source
radius = 7 # radius of the food source
size_food = 5 # size of each food item

class Ants:
    def __init__(self) -> None:
        self.has_food = np.zeros((num_ants), dtype=bool)
    def calculate_direction(self, start, target):
        """Calculates the direction from the start to the target."""
        direction_vector = target - start
        return direction_vector / np.linalg.norm(direction_vector)

    def move_ants(self, positions, directions):
        """Represents the movement of the ants."""
        cos_directions = step_size * np.cos(np.radians(directions))
        sin_directions = step_size * np.sin(np.radians(directions))

        for ant in range(len(positions)):
            x, y = positions[ant]
            next_x = x + cos_directions[ant]
            next_y = y + sin_directions[ant]

            if 0 <= next_x <= width and 0 <= next_y <= height:
                x, y = next_x, next_y
            else:
                direction_to_center = self.calculate_direction(np.array([x, y]), nest_position)
                directions[ant] = np.degrees(np.arctan2(direction_to_center[1], direction_to_center[0]))
                repulsion_vector = direction_to_center * repulsion_distance
                x += repulsion_vector[0]
                y += repulsion_vector[1]

            positions[ant] = (x, y)
            directions[ant] += np.random.uniform(-pheri, pheri)

        return positions



class Food:
    def __init__(self, num_food, radius, min_distance = 400):
        self.num_food = num_food
        self.radius = radius
        self.min_distance = min_distance
        self.center = None

    def generate_positions(self):
        # Generate random angles to distribute food positions uniformly in a circle
        angles = np.linspace(0, 2 * np.pi, self.num_food)
        radii = np.sqrt(np.random.uniform(0, 1, self.num_food)) * self.radius

        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        # randomly choose x and y coordinates for the center of the food source
        x_center = np.random.randint(50, width //2)
        y_center = np.random.randint(50, height)
        self.center = x_center, y_center

        # return the final and scaled positions of the food items 
        self.positions = np.column_stack((x, y)) * pixel_size + self.center
        return self.positions

    

class Drawing:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height))
        self.food_positions = Food(num_food, radius).generate_positions()



    def draw_pheromones(self, surface, home_pheromones, food_pheromones):
        for (x, y), intensity in np.ndenumerate(home_pheromones):
            food_pheromones[x ,y] = max(intensity - decay_rate, 0)
            home_pheromones[x, y] = max(intensity - decay_rate, 0)
            pygame.draw.rect(surface, (0, food_pheromones[x, y], home_pheromones[x, y]), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))


    def draw_food(self, size_food):
        # this function takes in the size of the food items and draws the food source on the screen
        for food_pos in self.food_positions:
            pygame.draw.circle(self.screen, (0, 255, 0), food_pos.astype(int) , size_food)


    def draw_ants(self, ant_positions, size):
        # this function takes in the screen, the position and size of the ant and draws them in
        self.screen.fill((0, 0, 0))
        self.draw_pheromones(self.surface, main.home_pheromones)
        self.screen.blit(self.surface, (0, 0))  # Clear the screen to draw the new positions
        self.draw_food(size_food)

        for ant_pos in ant_positions:
            pygame.draw.circle(self.screen, (255, 0, 0), ant_pos.astype(int), size)  # draws the ants in red

        pygame.display.flip()  # updates the entire display
        self.clock.tick(FPS)  # regulates the frames per second


class Run:
    def __init__(self):
        self.ant_positions = np.full((num_ants, 2), nest_position, dtype=float)
        self.ant_directions = np.random.uniform(0, 360, size=num_ants)
        self.home_pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)  # Initialize pheromones to zero
        self.food_pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)
        self.go = True


 
    def main(self):
        while self.go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.go = False

            ant_positions = ant.move_ants(self.ant_positions, self.ant_directions)

            for ant_pos in ant_positions:
                logical_x, logical_y = ant_pos.astype(int) // pixel_size

                if ant.has_food == False:
                    self.home_pheromones[logical_x, logical_y] += home_pheromone
                else: 
                    self.food_pheromomes[logical_x, logical_y] += food_pheromone
            vis.draw_ants(ant_positions, size_ant)


vis = Drawing()
ant = Ants()
main = Run()

if __name__ == "__main__":
    main.main()  # starts the code if this file is executed


