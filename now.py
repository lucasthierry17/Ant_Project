import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 1200, 800
NUM_ANTS = 10
PRATIO = 5  # Ratio between screen and phero_grid
NEST = (WIDTH // 3.5, HEIGHT // 2)
VSYNC = True
SHOWFPS = True
FOOD_RADIUS = 15
FOOD_PHEROMONE_UPDATE = (0, 200, 0)
SPEED = 2
food_sources = []

class Ants(pygame.sprite.Sprite):

    def __init__(self, nest, pheromones):
        super().__init__()
        self.x, self.y = nest  # Starting coordinates
        self.phero = pheromones
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (120, 45, 45), (6, 5), 3)  # Draw ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.start_ang = random.randint(0, 360)  # Initial angle between 0 and 360 degrees
        self.angle_range = (-10, 10)  # Range for random angle change
        self.desireDir = pygame.Vector2(np.cos(np.radians(self.start_ang)), np.sin(np.radians(self.start_ang)))  # Direction
        self.has_food = False
        self.trail_strength = 220  # Initial strength of the pheromone trail

    def update(self):
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))

        if self.has_food:  # Ant has food
            distance = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))
            if distance < 5:  # Ant has reached the nest
                self.has_food = False
                self.trail_strength = 50  # Set trail strength to 50 at the nest
            else:
                self.trail_strength -= 1  # Decrease trail strength as ant moves away from food source
                self.trail_strength = max(50, self.trail_strength)
                self.phero.img_array[scaled_pos] += (0, self.trail_strength, 0)
                self.move_towards(NEST)

        else:  # Ant has no food
            random_angle = random.uniform(-10, 10)
            self.desireDir = self.desireDir.rotate(random_angle)

            if food_sources:
                min_distance = 100000
                nearest_food = None
                for food in food_sources:
                    distance = self.calculate_distance(scaled_pos, food)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_food = food

                if min_distance < 5:  # Reaches the food source
                    self.has_food = True
                elif nearest_food:
                    self.move_towards(nearest_food)

            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, 50)

        # Move the ant
        self.x += self.desireDir[0] * SPEED
        self.y += self.desireDir[1] * SPEED

        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            # Bounce back if the ant goes out of the screen
            self.desireDir *= -1
            self.x += self.desireDir[0] * SPEED
            self.y += self.desireDir[1] * SPEED

        self.rect.center = (self.x, self.y)

    def calculate_distance(self, start, target):
        return math.sqrt((target[0] - start[0]) ** 2 + (target[1] - start[1]) ** 2)

    def move_towards(self, target):
        target_pos = (int(target[0] / PRATIO), int(target[1] / PRATIO))
        self.desireDir = pygame.Vector2(target[0] - self.x, target[1] - self.y).normalize()
        self.phero.img_array[target_pos] += (0, self.trail_strength, 0)  # Update pheromone at target position

class Pheromones:

    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        self.img_array -= 0.2  # Evaporation rate
        self.img_array = np.clip(self.img_array, 0, 255)  # Clip to color range
        pygame.surfarray.blit_array(self.image, self.img_array.astype(int))
        return self.image

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=VSYNC)
    pheromones = Pheromones((WIDTH, HEIGHT))  # Creating phero grid
    ants = pygame.sprite.Group()

    for _ in range(NUM_ANTS):  # Adding num_ants
        ants.add(Ants(NEST, pheromones))

    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()

                if event.button == 1:
                    food_sources.append((mousepos[0], mousepos[1]))
                elif event.button == 3:
                    for source in food_sources:
                        if math.dist(mousepos, source) < FOOD_RADIUS:
                            food_sources.remove(source)

        phero_grid = pheromones.update()
        ants.update()

        # Draw everything onto the screen
        screen.fill(0)  # Fill black for the next step
        scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT))  # Scale phero_grid back to normal screen size
        screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
        pygame.draw.circle(screen, [70, 50, 40], NEST, 16, 5)  # Draw nest

        # Draw food sources
        for source in food_sources:
            pygame.draw.circle(screen, (0, 200, 0), source, FOOD_RADIUS)  # Draw food

        ants.draw(screen)  # Draw ants directly onto the screen

        pygame.display.update()

if __name__ == "__main__":
    main()
