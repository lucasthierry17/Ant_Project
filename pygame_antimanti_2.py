import pygame
import numpy as np
from pygame.locals import *


logical_width, logical_height = 150, 100  # size for the arrays
pixel_size = 6  # scales the screen up for visualization
width, height = logical_width * pixel_size, logical_height * pixel_size
num_ants = 50 # number of ants
size_ant = 5 # size of the ant for drawing
FPS = 250 # frames per second
pheri = 15  # this represents their sight of view
repulsion_distance = 5  # how far the ants will go towards the center
nest_position = np.array([width // 2, height // 2])  # set nest to the middle
home_pheromone = 255 # value of intensity added to the position
step_size = 4 # step_size of the ants
decay_rate = 2 # value is subtracted from the intensity in position x, y

class Ants:
    def __init__(self):
        self.food = Food(1, 2)
        self.found_food = False

    def calculate_direction(self, start, target):
        """Calculates the direction from the start to the target."""
        direction_vector = target - start
        return direction_vector / np.linalg.norm(direction_vector)
    
    
    def find_min_pheromone(self, ant_position, pheromones, radius):
        x, y = ant_position
        x, y = int(x), int(y)  # Convert to integers
        min_pheromone = float('inf')
        min_pheromone_position = None

        for i in range(max(0, x - radius), min(logical_width, x + radius + 1)):
            for j in range(max(0, y - radius), min(logical_height, y + radius + 1)):
                if pheromones[i, j] < min_pheromone:
                    min_pheromone = pheromones[i, j]
                    min_pheromone_position = np.array([i, j])

        return min_pheromone_position

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
            
            direction_to_center = self.calculate_direction(np.array([x, y]), nest_position)
            directions[ant] = np.degrees(np.arctan2(direction_to_center[1], direction_to_center[0]))
            repulsion_vector = direction_to_center * repulsion_distance
            x += repulsion_vector[0]
            y += repulsion_vector[1]

            positions[ant] = (x, y)
            if not self.found_food:
                # Wenn die Ameise noch kein Essen gefunden hat
                min_pheromone_position = self.find_min_pheromone(positions[ant], main.pheromones, radius=5)

                # Update direction based on the position of minimum pheromone
                if min_pheromone_position is not None:
                    direction_to_min_pheromone = self.calculate_direction(np.array([x, y]), min_pheromone_position)
                    directions[ant] = np.degrees(np.arctan2(direction_to_min_pheromone[1], direction_to_min_pheromone[0]))

                # Wenn Essen gefunden, aktualisiere den Status und setze ein neues Pheromon
                """
                if np.array_equal(min_pheromone_position, self.food.center):
                    logical_x, logical_y = min_pheromone_position.astype(int)
                    self.found_food = True
                    main.pheromones[logical_x, logical_y] = 255  # Pheromonwert für "Essen gefunden"
                """
            else:
                # Die Ameise hat Essen gefunden, folge dem schwächsten Pheromon in der Umgebung
                min_pheromone_position = self.find_min_pheromone(positions[ant], main.pheromones, radius=5)

                if min_pheromone_position is not None:
                    direction_to_min_pheromone = self.calculate_direction(np.array([x, y]), min_pheromone_position)
                    directions[ant] = np.degrees(np.arctan2(direction_to_min_pheromone[1], direction_to_min_pheromone[0]))

        return positions





class Food: # not implemented yet
    def __init__(self, num_food, radius, min_distance = 400):
        self.num_food = num_food
        self.radius = radius
        self.min_distance = min_distance
        self.center = None
        self.generate_positions()

    def generate_positions(self):
        angles = np.linspace(0, 2 * np.pi, self.num_food)
        radii = np.sqrt(np.random.uniform(0, 1, self.num_food)) * self.radius

        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        while True:
            self.center = np.random.uniform(-18, 18, size=2)
            if np.linalg.norm(self.center - np.array([width // 2, height // 2])) >= self.min_distance:
                break
        
        self.positions = np.column_stack((x, y)) + self.center



    

class Drawing:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def draw_pheromones(self, surface, pheromones):
        surface.fill((0, 0, 255, 0))
        for (x, y), intensity in np.ndenumerate(pheromones):
            pheromones[x, y] = max(intensity - decay_rate, 0)
            pygame.draw.rect(surface, (0, 0, 255, pheromones[x, y]), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

            # if essen gefunden dann draw an der position die Pheromonen mit der Farbe grün

    def draw_ants(self, screen, ant_positions, size):
        self.screen.fill((0, 0, 0))
        # this function takes in the screen, the position and size of the ant and draws them in
        self.draw_pheromones(self.surface, main.pheromones)
        self.screen.blit(self.surface, (0, 0))  # Clear the screen to draw the new positions

        for ant_pos in ant_positions:
            pygame.draw.circle(screen, (255, 0, 0), ant_pos.astype(int), size)  # draws the ants in red

        pygame.display.flip()  # updates the entire display
        self.clock.tick(FPS)  # regulates the frames per second


class Run:
    def __init__(self):
        self.ant_positions = np.full((num_ants, 2), nest_position, dtype=float)
        self.ant_directions = np.random.uniform(0, 360, size=num_ants)
        self.pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)  # Initialize pheromones to zero
        self.go = True

    def main(self):
        while self.go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.go = False

            ant_positions = ant.move_ants(self.ant_positions, self.ant_directions)

            for ant_pos in ant_positions:
                logical_x, logical_y = ant_pos.astype(int) // pixel_size
                
                self.pheromones[logical_x, logical_y] += home_pheromone

            vis.draw_ants(vis.screen, ant_positions, size_ant)


vis = Drawing()
ant = Ants()
main = Run()

if __name__ == "__main__":
    main.main()  # starts the code if this file is executed

