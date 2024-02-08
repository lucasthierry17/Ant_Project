import pygame
import numpy as np
from pygame.locals import *

logical_width, logical_height = 150, 100  # size for the arrays
pixel_size = 6  # scales the screen up for visualization
width, height = logical_width * pixel_size, logical_height * pixel_size

num_ants = 20  # number of ants
size_ant = 5  # size of the ant for drawing
FPS = 350  # frame per second

pheri = 15  # this represents their sight of view
repulsion_distance = 5  # how far the ants will go towards the center
nest_position = np.array([width // 2, height // 2])  # set nest to the middle
home_pheromone = 120  # value of intensity added to the position
food_pheromone = 120  # value of intensity added to the position

step_size = 7  # step_size of the ants
decay_rate = 2  # value is subtracted from the intensity in position x, y

num_food = 200  # number of food items in the food source
radius = 7  # radius of the food source
size_food = 5  # size of each food item

class Ants:
    def __init__(self) -> None:
        self.has_food = np.zeros((num_ants), dtype=bool)

    def calculate_direction(self, start, target):
        """Calculates the direction from the start to the target. It takes in the position of the target and the position of the nest."""
        direction_vector = target - start
        norm = np.linalg.norm(direction_vector)

        if np.isnan(norm) or norm < 1e-6:  # Check for small norm to handle division by very small values
            print("Warning: Norm is NaN or very small. Start:", start, "Target:", target)
            # Wenn die Norm NaN oder sehr klein ist, gebe einen Standardvektor zurück (z.B., nach rechts)
            return np.array([1.0, 0.0])

        return direction_vector / norm
    
    def find_min_pheromone(self, ant_position, pheromones, radius):
        x, y = map(int, ant_position)  # Convert to integers
        min_pheromone = float('inf')
        min_pheromone_position = None

        for i in range(max(0, x - radius), min(logical_width, x + radius + 1)):
            for j in range(max(0, y - radius), min(logical_height, y + radius + 1)):
                distance_to_nest = np.linalg.norm(np.array([i, j]) - nest_position)
                if pheromones[i, j] > 0 and distance_to_nest < min_pheromone:
                    min_pheromone = pheromones[i, j]
                    min_pheromone_position = np.array([i, j])

        return min_pheromone_position


    def move_ants(self, positions, directions, home_pheromones, food_pheromones):
        for ant in range(len(positions)):
            x, y = positions[ant]
            logical_x, logical_y = int(x) // pixel_size, int(y) // pixel_size

            # Check if the ant has food
            if self.has_food[ant]:
                # If the ant has food, follow blue pheromones
                min_pheromone_position = self.find_min_pheromone((logical_x, logical_y), home_pheromones, pheri)
            else:
                # If the ant does not have food, search for green pheromones
                min_pheromone_position = self.find_min_pheromone((logical_x, logical_y), food_pheromones, pheri)

            if min_pheromone_position is not None:
                if not self.has_food[ant]:
                    # Ameisen ohne Futter suchen den kürzesten Weg zur Futterquelle
                    tsp_path = self.find_tsp_path((logical_x, logical_y), min_pheromone_position, food_pheromones)
                    for tsp_point in tsp_path[1:-1]:
                        # Debugging-Ausgaben hinzufügen
                        #print("Before calculate_direction:", tsp_point)
                        # Berechnung der Richtung für jeden Punkt auf dem TSP-Pfad
                        direction_vector = self.calculate_direction(np.array([logical_x, logical_y]), tsp_point)

                        print("Before calculate_direction:", tsp_point)
                        # Berechnung der Richtung für jeden Punkt auf dem TSP-Pfad
                        direction_vector = self.calculate_direction(np.array([logical_x, logical_y]), tsp_point)

                        # Überprüfen, ob die berechnete Richtung gültig ist
                        if not np.isnan(direction_vector).any():
                            directions[ant] = np.degrees(np.arctan2(direction_vector[1], direction_vector[0]))

                            # Ameise bewegt sich in Richtung des Punktes auf dem TSP-Pfad
                            next_x, next_y = x + direction_vector[0] * step_size, y + direction_vector[1] * step_size

                            # Debugging-Ausgaben hinzufügen
                            print("After calculate_direction:", next_x, next_y)

                            # Überprüfen, ob die Ameise außerhalb der Grenzen ist und den Fall behandeln
                            if 0 <= logical_x < logical_width and 0 <= logical_y < logical_height:
                                # Überprüfen, ob next_x oder next_y NaN ist und behandeln
                                if not np.isnan(next_x) and not np.isnan(next_y):
                                    positions[ant] = (next_x, next_y)
                                    # Überprüfen, ob eine Ameise innerhalb einer Futterposition ist
                                    for food_pos in vis.food_positions:
                                        distance_to_food = np.linalg.norm(np.array([next_x, next_y]) - food_pos)
                                        if distance_to_food < size_food:
                                            self.has_food[ant] = True
                                            home_pheromones[logical_x, logical_y] += home_pheromone
                                            break  # Um mehrfache Kollisionen mit Futterquellen zu vermeiden
                                    else:
                                        # Fall behandeln, wenn die Ameise außerhalb der Grenzen ist
                                        self.has_food[ant] = False  # has_food auf False setzen, um weitere Probleme zu verhindern
                                else:
                                    # Fall behandeln, wenn next_x oder next_y NaN ist
                                    self.has_food[ant] = False  # has_food auf False setzen, um weitere Probleme zu verhindern
                            else:
                                # Fall behandeln, wenn die Ameise außerhalb der Grenzen ist
                                self.has_food[ant] = False # has_food auf False setzen, um weitere Probleme zu verhindern
                else:
                    # Ameisen mit Futter folgen den blauen Pheromonen
                    direction_vector = self.calculate_direction(np.array([logical_x, logical_y]), min_pheromone_position)

                    # Überprüfen, ob die berechnete Richtung gültig ist
                    if not np.isnan(direction_vector).any():
                        directions[ant] = np.degrees(np.arctan2(direction_vector[1], direction_vector[0]))

                        # Ameise bewegt sich in Richtung des Minimum-Pheromon-Positions
                        next_x, next_y = x + direction_vector[0] * step_size, y + direction_vector[1] * step_size

                        # Aktualisierung von logischen_x und logischen_y basierend auf der neuen Ameisenposition
                        logical_x, logical_y = int(next_x) // pixel_size, int(next_y) // pixel_size

                        # Überprüfen, ob die Ameise außerhalb der Grenzen ist und den Fall behandeln
                        if 0 <= logical_x < logical_width and 0 <= logical_y < logical_height:
                            # Überprüfen, ob next_x oder next_y NaN ist und behandeln
                            if not np.isnan(next_x) and not np.isnan(next_y):
                                positions[ant] = (next_x, next_y)
                                distance_to_home = np.linalg.norm(np.array([next_x, next_y]) - nest_position)
                                if distance_to_home < 30:
                                    self.has_food[ant] = False
                            else:
                                # Fall behandeln, wenn die Ameise außerhalb der Grenzen ist
                                self.has_food[ant] = False  # has_food auf False setzen, um weitere Probleme zu verhindern

            else:
                # If no pheromone is found, move randomly
                cos_directions = step_size * np.cos(np.radians(directions))
                sin_directions = step_size * np.sin(np.radians(directions))

                next_x = x + cos_directions[ant]
                next_y = y + sin_directions[ant]

                # Überprüfen, ob die berechnete Position innerhalb der Grenzen liegt
                if 0 <= next_x <= width and 0 <= next_y <= height:
                    # Überprüfen, ob next_x oder next_y NaN ist und behandeln
                    if not np.isnan(next_x) and not np.isnan(next_y):
                        x, y = next_x, next_y
                else:
                    # Wenn die berechnete Position außerhalb der Grenzen liegt, führe eine Repulsion zum Nest durch
                    direction_to_center = self.calculate_direction(np.array([x, y]), nest_position)
                    directions[ant] = np.degrees(np.arctan2(direction_to_center[1], direction_to_center[0]))
                    repulsion_vector = direction_to_center * repulsion_distance
                    x += repulsion_vector[0]
                    y += repulsion_vector[1]

                positions[ant] = (x, y)
                directions[ant] += np.random.uniform(-pheri, pheri)

        return positions



    def find_tsp_path(self, start, target, pheromones):
        # Use a basic TSP algorithm to find a path from start to target based on pheromone intensity
        path = [start]
        visited = set([start])

        while len(visited) < logical_width * logical_height:
            current_position = path[-1]
            neighbors = self.get_neighbors(current_position, pheromones)

            next_position = None
            max_pheromone = 0

            for neighbor in neighbors:
                if neighbor not in visited and pheromones[neighbor[0], neighbor[1]] > max_pheromone:
                    next_position = neighbor
                    max_pheromone = pheromones[neighbor[0], neighbor[1]]

            if next_position:
                path.append(next_position)
                visited.add(next_position)
            else:
                # If no unvisited neighbor with pheromone is found, break the loop
                break

        # Adjust the path to be more direct between start and target
        path.append(target)

        return path

    def get_neighbors(self, position, pheromones):
        x, y = position
        neighbors = []

        for i in range(max(0, x - 1), min(logical_width, x + 2)):
            for j in range(max(0, y - 1), min(logical_height, y + 2)):
                if i != x or j != y:
                    neighbors.append((i, j))

        return neighbors

class Food:
    """In this class, the food_sources are being created. They are shown as x of smaller green circles inside of a bigger circle. They are being placed randomly inside a certain area (away from the nest)"""
    def __init__(self, num_food, radius, min_distance=400):
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
        x_center = np.random.randint(50, width // 3)

        y_center = np.random.randint(50, height - 50)

      
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
        """This function draws the pheromones. It draws small rectangles on the screen, the values for the color are being stored inside two numpy arrays (food_pheromones and home_pheromones). The pheromones disappear through the substraction of the decay rate each step"""
        for (x, y), intensity in np.ndenumerate(home_pheromones):
            home_pheromones[x, y] = max(intensity - decay_rate, 0)
        for (x, y), intensity in np.ndenumerate(food_pheromones):
            food_pheromones[x ,y] = max(intensity - decay_rate, 0) 
            pygame.draw.rect(surface, (0, food_pheromones[x, y], home_pheromones[x, y]), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
        
            
        

    def draw_food(self, size_food):
        """This function draws the food_sources at the generated location"""
        # this function takes in the size of the food items and draws the food source on the screen
        for food_pos in self.food_positions:
            pygame.draw.circle(self.screen, (0, 255, 0), food_pos.astype(int), size_food)

    def draw_ants(self, ant_positions, size):
        """The ants are drawn in red with the size specified in the size_ant variable. Also, we are calling the other drawing functions, so that the elements are drawn on to the screen as well"""
        # this function takes in the screen, the position and size of the ant and draws them in
        self.screen.fill((0, 0, 0))
        self.draw_pheromones(self.surface, main.home_pheromones, main.food_pheromones)
        self.screen.blit(self.surface, (0, 0))  # Clear the screen to draw the new positions
        self.draw_food(size_food)


        for ant_pos in ant_positions:
            
            pygame.draw.circle(self.screen, (255, 0, 0), ant_pos.astype(int), size)  # draws the ants without food in red

        self.draw_nest()

       

        pygame.display.flip()  # updates the entire display
        self.clock.tick(FPS)  # regulates the frames per second


    def draw_nest(self):
        pygame.draw.circle(self.screen, (121, 61, 0), (width // 2, height // 2), 30)





class Run:
    def __init__(self):
        self.ants = Ants()
        self.ant_positions = np.full((num_ants, 2), nest_position, dtype=float)
        self.ant_directions = np.random.uniform(0, 360, size=num_ants)
        self.home_pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)  # Initialize home pheromones to zero
        self.food_pheromones = np.full((logical_width, logical_height), 0, dtype=np.uint8)  # Initialize food pheromones to zero
        self.go = True

    def main(self):
        while self.go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.go = False

            self.ant_positions = self.ants.move_ants(self.ant_positions, self.ant_directions, self.home_pheromones, self.food_pheromones)

            for ant_pos, has_food in zip(self.ant_positions, self.ants.has_food):
                logical_x, logical_y = ant_pos.astype(int) // pixel_size


                if not has_food:
                     # Check if an ant is inside a food position
                    for food_pos in vis.food_positions:
                        distance_to_food = np.linalg.norm(ant_pos - food_pos)
                        if distance_to_food < size_food:
                            self.ants.has_food[np.where((self.ant_positions == ant_pos).all(axis=1))] = True
                    self.home_pheromones[logical_x, logical_y] += home_pheromone
                else:
                    self.food_pheromones[logical_x, logical_y] += food_pheromone
                    distance_to_home = np.linalg.norm(ant_pos - nest_position)
                    if distance_to_home < 30:
                        self.ants.has_food[np.where((self.ant_positions == ant_pos).all(axis=1))] = False


            vis.draw_ants(self.ant_positions, size_ant)

vis = Drawing()
main = Run()

if __name__ == "__main__":
    main.main()  # starts the code if this file is executed
