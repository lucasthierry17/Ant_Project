import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 1200, 800
NUM_ANTS = 1
PRATIO = 5  # Ratio between screen and phero_grid
NEST = (WIDTH // 5, HEIGHT // 4)
VSYNC = True
SHOWFPS = True
FOOD_RADIUS = 20
SPEED= 2
NEST_SIZE = 15
HOME_PHEROMONE = 200
FOOD_PHEROMONE = 100
SIZE_ANT = 5
max_distance = 0
food_sources = []


class Ants(pygame.sprite.Sprite):
    def __init__(self, nest, pheromones):
        super().__init__()
        self.x, self.y = nest  # Starting coordinates
        self.phero = pheromones
        self.angle = random.randint(0, 360)
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (6, 5), SIZE_ANT)  # Draw ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.pos = pygame.Vector2(self.rect.center)
        self.angle_range = (-8, 8)  # Range for random angle change
        self.desireDir = pygame.Vector2(np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle)))  # Direction 
        self.has_food = False # True if food, else False
        self.path_to_food = []  # List to store the path to the food source
        self.last_sdp = (NEST[0] / PRATIO, NEST[1] / PRATIO)

    def update(self):
        global max_distance, SPEED
        angle = random.randint(0, 360)
        randDir = pygame.Vector2(np.cos(np.radians(angle)), np.sin(np.radians(angle)))
        random_scale = 0.11
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))
        food_color = (0, 100, 0)
        nest_color = (0, 0, 100)

        if self.has_food:
            self.update_with_food(randDir, random_scale, scaled_pos)
        else:
            self.update_without_food(randDir, scaled_pos)
        self.move()
        self.check_boundaries()
        self.last_sdp = scaled_pos

    def update_with_food(self, randDir, random_scale, scaled_pos):
        global max_distance
        distance = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))
        if distance > max_distance:
            max_distance = distance
        if distance < (NEST_SIZE / PRATIO):
            self.has_food = False 
        elif distance > max_distance - 15:
            self.desireDir = pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize()
        else:
            self.desireDir += pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize() * .08
            self.desireDir = pygame.Vector2(self.desireDir + randDir * random_scale).normalize()
            self.path_to_food.append(scaled_pos)  # Store current position in the path_to_food list
        pheromone_value = 200 * (distance / max_distance)
        if pheromone_value > 255:
            pheromone_value = 255  
        if scaled_pos != self.last_sdp:
            self.phero.img_array[scaled_pos] += (0, pheromone_value, 0)

    def update_without_food(self, randDir, scaled_pos):
        random_angle = random.uniform(-8, 8)
        self.desireDir = self.desireDir.rotate(random_angle)
        if food_sources:
            self.update_with_food_sources(randDir, scaled_pos)
        else:
            #self.random_walk() 
            #self.adjust_direction(scaled_pos, 1)
            self.move_towards_food(scaled_pos)
        if self.last_sdp != scaled_pos:
            self.phero.img_array[scaled_pos] += (0, 0, HOME_PHEROMONE)
    
    def return_home(self):
        # Follow the reverse of the path_to_food list to return home
        while self.path_to_food:
            next_pos = self.path_to_food.pop()  # Get the next position from the path_to_food list
            self.desireDir = pygame.Vector2(next_pos[0] - self.x, next_pos[1] - self.y).normalize()  # Set direction towards next_pos
            self.move()

    def random_walk(self):
        self.desireDir = self.desireDir.rotate(random.uniform(*self.angle_range))


    def update_with_food_sources(self, randDir, scaled_pos):
        min_distance = float("inf")
        nearest_food = None
        for food in food_sources:
            distance = self.calculate_distance(scaled_pos, food)
            if distance < min_distance:
                min_distance = distance
                nearest_food = food
                if min_distance < (FOOD_RADIUS / PRATIO):
                    self.has_food = True
                elif min_distance < (FOOD_RADIUS / 2):
                    self.desireDir = pygame.Vector2(nearest_food[0] - scaled_pos[0], nearest_food[1] - scaled_pos[1]).normalize()
                else:
                    #self.adjust_direction(scaled_pos, 1)
                    self.move_towards_food(scaled_pos)
    def move(self):
        self.x += self.desireDir[0] * SPEED 
        self.y += self.desireDir[1] * SPEED
        self.rect.center = (self.x, self.y)

    def check_boundaries(self):
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            self.turn_around()

    
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
        behind = self.phero.img_array[scaled_pos[0], max(scaled_pos[1] - 1, 0)]  
    
        max_concentration = max(front[channel], left[channel], right[channel])
        possible_directions = []
        if front[channel] == left[channel] == right[channel]: # go random if all values are equal
            random_angle = random.uniform(-10, 10)
            self.desireDir = self.desireDir.rotate(random_angle)

        else:
            #if max_concentration == left[channel]:
            #    possible_directions.append(pygame.Vector2(-1, 0))  # Turn left
            #if max_concentration == front[channel]:
            #    possible_directions.append(pygame.Vector2(0, -1))  # Move forward
            #if max_concentration == behind[channel]:
            #    possible_directions.append(pygame.Vector2(0, 1))  # Move behind
            if max_concentration == right[channel]:
                self.desireDir = pygame.Vector2(right[0] - scaled_pos[0], right[1] - scaled_pos[1]).normalize() # turn right
            if max_concentration == left[channel]:
                self.desireDir = pygame.Vector2(left[0] - scaled_pos[0], left[1] - scaled_pos[1]).normalize() # turn left
            if max_concentration == front[channel]:
                self.desireDir = pygame.Vector2(front[0] - scaled_pos[0], front[1] - scaled_pos[1]).normalize() # go to the front
    
            else: 
                random_angle = random.uniform(-10, 10)
                self.desireDir = self.desireDir.rotate(random_angle)

    def move_towards_food(self, scaled_pos):
        # Define vectors for different directions
        directions = [pygame.Vector2(0, -1), pygame.Vector2(-1, 0), pygame.Vector2(1, 0), pygame.Vector2(0, 1)]

        # Calculate the positions of adjacent cells
        adjacent_positions = [(scaled_pos[0], scaled_pos[1] - 1),  # Up
                            (scaled_pos[0] - 1, scaled_pos[1]),  # Left
                            (scaled_pos[0] + 1, scaled_pos[1]),  # Right
                            (scaled_pos[0], scaled_pos[1] + 1)]  # Down

        max_concentration = -1
        max_direction = None

        # Find the direction with the maximum pheromone concentration that doesn't lead towards the nest
        for direction, adjacent_pos in zip(directions, adjacent_positions):
            x, y = adjacent_pos
            # Ensure that the adjacent position is within the grid bounds
            if 0 <= x < self.phero.img_array.shape[0] and 0 <= y < self.phero.img_array.shape[1]:
                concentration = self.phero.img_array[x, y, 1]  # Assuming green channel contains pheromone concentration
                if concentration > max_concentration:
                    max_concentration = concentration
                    max_direction = direction

        # If there's a direction with a positive pheromone concentration, move towards it
        if max_concentration > 0:
            self.desireDir = max_direction
            print("Tried if")
        else:
            # If no positive concentration is found, move randomly
            random_angle = random.uniform(-10, 10)
            self.desireDir = self.desireDir.rotate(random_angle)
            print("Tried else")
        self.desireDir = self.desireDir.normalize()


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

        
def handle_mouse_input(event):
    global food_sources
    mousepos = pygame.mouse.get_pos()
    if event.button == 1:
        food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
    elif event.button == 3:
        for source in food_sources:
            if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < FOOD_RADIUS:
                food_sources.remove(source)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=VSYNC) 
    pheromones = Pheromones((WIDTH, HEIGHT))  # Creating phero grid
    ants = pygame.sprite.Group()
    global food_sources # Define food_sources locally

    for _ in range(NUM_ANTS):  # Adding num_ants
        ants.add(Ants(NEST, pheromones))

    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_input(event)  # Pass event
        phero_grid = pheromones.update()
        ants.update()

        draw(screen, phero_grid, food_sources, ants)  # Pass ants as parameter
    pygame.quit()

def draw(screen, phero_grid, food_sources, ants):
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
