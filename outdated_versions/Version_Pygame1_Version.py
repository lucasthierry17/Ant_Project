import pygame
import numpy as np

class Ants:
    def __init__(self, num_ants, start_position):
        self.positions = np.full((num_ants, 2), start_position, dtype=float)
        self.directions = np.random.uniform(0, 360, size=num_ants)

    def movement(self):
        cos_directions = np.cos(np.radians(self.directions))
        sin_directions = np.sin(np.radians(self.directions))

        for ant in range(len(self.positions)):
            x, y = self.positions[ant]
            x += cos_directions[ant]
            y += sin_directions[ant]

            # Clip ant positions to be within the board boundaries
            x = np.clip(x, 0, width - 1)
            y = np.clip(y, 0, height - 1)

            self.positions[ant] = (x, y)
            self.directions[ant] += np.random.uniform(-20, 20)

class Food:
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

class Simulation:
    def __init__(self, width, height, num_ants, num_food):
        self.width = width
        self.height = height
        self.num_ants = num_ants
        self.num_food = num_food

        self.pheromone_home = np.zeros((width, height), dtype=float)
        self.pheromone_decay_rate = 0.94
        self.max_pheromone_value = 255

        self.ants = Ants(num_ants, start_position=(width // 2, height // 2))
        self.food = Food(num_food, radius=3.5)

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pheromone Grid Visualization")


    def update_pheromones(self):
        self.pheromone_home *= self.pheromone_decay_rate

        self.ants.movement()
        for ant_pos in self.ants.positions:
            x, y = ant_pos.astype(int)
            self.pheromone_home[x, y] += 10

        np.clip(self.pheromone_home, 0, self.max_pheromone_value, out=self.pheromone_home)

    def display_simulation(self):
        surface_home = pygame.surfarray.make_surface(self.pheromone_home)
        self.screen.blit(surface_home, (0, 0))

        for ant_pos in self.ants.positions:
            pygame.draw.circle(self.screen, (255, 0, 0), ant_pos.astype(int), 5)

        for food_pos in self.food.positions:
            pygame.draw.circle(self.screen, (0, 255, 0), (int(food_pos[0] * 10) + 400, int(food_pos[1] * 10) + 300), 5)

        pygame.display.flip()

    def run_simulation(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update_pheromones()
            self.display_simulation()

        pygame.quit()

width, height = 1000, 800
num_ants = 100
num_food = 100

# Instantiate the Simulation class and run the simulation
ant_simulation = Simulation(width, height, num_ants, num_food)
ant_simulation.run_simulation()
