import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 1200, 800
NUM_ANTS = 100
PRATIO = 5  # Ratio between screen and phero_grid
NEST = (WIDTH // 3.5, HEIGHT // 2)
VSYNC = True
SHOWFPS = True
FOOD_RADIUS = 30
FOOD_PHEROMONE_UPDATE = (0, 200, 0)
SPEED= 2
food_sources = []
NEST_SIZE = 25
SIZE_ANT = 5
max_distance = 0

class Ants(pygame.sprite.Sprite):

    def __init__(self, nest, pheromones):
        super().__init__()
        self.x, self.y = nest  # Starting coordinates
        self.phero = pheromones 
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (6, 5), SIZE_ANT)  # Draw ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.pos = pygame.Vector2(self.rect.center)
        self.start_ang = random.randint(0, 360)  # Initial angle between 0 and 360 degrees
        self.angle_range = (-10, 10)  # Range for random angle change
        self.desireDir = pygame.Vector2(np.cos(np.radians(self.start_ang)), np.sin(np.radians(self.start_ang)))  # Direction 
        self.has_food = False
        

    def update(self):
        angle = random.randint(0, 360)
        randDir = pygame.Vector2(np.cos(np.radians(angle)),np.sin(np.radians(angle)))
        wandrStr = 0.1
        global max_distance
        global distance
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))
        if self.has_food:  # Ant has food
            distance = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))
            if distance > max_distance:
                max_distance = distance
            if distance < (NEST_SIZE / 4):  # Ant has reached the nest
                self.has_food = False 
            else:
                #self.adjust_direction(scaled_pos, 2)
                #self.desireDir = pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize()

                self.desireDir += pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize() * .08
                self.desireDir = pygame.Vector2(self.desireDir + randDir * wandrStr)

                # Add random deviation


                # Set the adjusted direction as the desireDir
                #pheromone_value = 200 * (distance / max_distance)
                #if pheromone_value > 255:
                #    pheromone_value = 255  
                self.phero.img_array[scaled_pos] += (0, 100, 0)

        else:  # Ant has no food
            random_angle = random.uniform(-10, 10)
            self.desireDir = self.desireDir.rotate(random_angle)
            distance_to_nest = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))

            if food_sources:
                min_distance = float("inf")
                nearest_food = None
                for food in food_sources:
                    distance = self.calculate_distance(scaled_pos, food)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_food = food
                        if min_distance < (FOOD_RADIUS / 5):  # Reaches the food source
                            self.has_food = True

                        elif min_distance < (FOOD_RADIUS):
                            self.desireDir = pygame.Vector2(nearest_food[0] - scaled_pos[0], nearest_food[1] - scaled_pos[1]).normalize()

                        else:
                        # Adjust direction based on pheromone concentrations
                            self.adjust_direction(scaled_pos, 1)
            else:
                self.adjust_direction(scaled_pos, 1)
        
            # Update pheromones
            pheromone_value = 100 - distance_to_nest
            if pheromone_value > 255:
                pheromone_value = 255
            self.phero.img_array[scaled_pos] += (0, 0, pheromone_value)

        # Move the ant
        self.x += self.desireDir[0] * SPEED 
        self.y += self.desireDir[1] * SPEED

        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            self.turn_around() 
            
            

        self.rect.center = (self.x, self.y)

    def calculate_distance(self, start, target):
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)

    def turn_around(self):
        self.desireDir *= -1
        self.x += self.desireDir[0] * SPEED
        self.y += self.desireDir[1] * SPEED
        return self.x, self.y

    def adjust_direction(self, scaled_pos, channel):
        # Check pheromone concentrations in the surrounding area and adjust direction accordingly
        front = self.phero.img_array[scaled_pos[0], scaled_pos[1]]
        left = self.phero.img_array[max(scaled_pos[0] - 1, 0), scaled_pos[1]]
        right = self.phero.img_array[min(scaled_pos[0] + 1, self.phero.img_array.shape[0] - 1), scaled_pos[1]]
        behind = self.phero.img_array[scaled_pos[0], max(scaled_pos[1] - 1, 0)]  # Corrected here
        

        max_concentration = max(front[channel], left[channel], right[channel])
        possible_directions = []
        if front[channel] == left[channel] == right[channel]: # go random if all values are equal
            random_angle = random.uniform(-10, 10)
            self.desireDir = self.desireDir.rotate(random_angle)
        else:
            if max_concentration == left[channel]:
                possible_directions.append(pygame.Vector2(-1, 0))  # Turn left
            if max_concentration == front[channel]:
                possible_directions.append(pygame.Vector2(0, -1))  # Move forward
            if max_concentration == behind[channel]:
                possible_directions.append(pygame.Vector2(0, 1))  # Move behind
            if max_concentration == right[channel]:
                possible_directions.append(pygame.Vector2(1, 0))  # Turn right
            
            if possible_directions:
                random_angle = random.uniform(-10, 10)
                self.desireDir = random.choice(possible_directions).rotate(random_angle)
            else: 
                random_angle = random.uniform(-10, 10)
                self.desireDir = self.desireDir.rotate(random_angle)

class Pheromones:
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        self.img_array -= 0.1  # Evaporation rate
        self.img_array = self.img_array.clip(0, 255)  # Clip to color range
        pygame.surfarray.blit_array(self.image, self.img_array) 
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
                    food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
                elif event.button == 3:
                    for source in food_sources:
                        if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < FOOD_RADIUS:
                            food_sources.remove(source)

        phero_grid = pheromones.update()
        ants.update()

        # Draw everything onto the screen
        screen.fill(0)  # Fill black for the next step
        scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT))  # Scale phero_grid back to normal screen size
        screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
        pygame.draw.circle(screen, [70, 50, 40], NEST, NEST_SIZE)  # Draw nest

        # Draw food sources
        for source in food_sources:
            pygame.draw.circle(screen, (0, 200, 0), (source[0] * PRATIO, source[1] * PRATIO), FOOD_RADIUS)  # Draw food

        ants.draw(screen)  # Draw ants directly onto the screen

        pygame.display.update()

if __name__ == "__main__":
    main()
