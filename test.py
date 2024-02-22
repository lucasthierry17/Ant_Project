import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 900, 600
NUM_ANTS = 1
PRATIO = 3  # Ratio between screen and phero_grid
NEST = (WIDTH // 5, HEIGHT // 4)
VSYNC = True
SHOWFPS = True
FOOD_RADIUS = 10
SPEED= 1
NEST_SIZE = 10
HOME_PHEROMONE = 200
FOOD_PHEROMONE = 100
SIZE_ANT = 3
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
        self.last_sdp = (nest[0]/10/2,nest[1]/10/2)

        

    def update(self):
        global max_distance, SPEED
        angle = random.randint(0, 360)
        randDir = pygame.Vector2(np.cos(np.radians(angle)), np.sin(np.radians(angle)))
        random_scale = 0.11
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))

        if self.has_food:
            self.update_with_food(randDir, random_scale, scaled_pos)
        else:
            self.update_without_food(randDir, scaled_pos)
        self.move()
        self.check_boundaries()

    def update_with_food(self, randDir, random_scale, scaled_pos):
        global max_distance
        distance = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))
        if distance > max_distance:
            max_distance = distance
        if distance < (NEST_SIZE / PRATIO):
            self.has_food = False 
            self.turn_around()
        elif distance > max_distance - 15:
            self.desireDir = pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize()
        else:
            self.desireDir += pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize() * .08
            self.desireDir = pygame.Vector2(self.desireDir + randDir * random_scale).normalize()
            
        pheromone_value = 255 * (distance / max_distance)
        if pheromone_value > 255:
            pheromone_value = 255  
        if scaled_pos != self.last_sdp:
            self.phero.img_array[scaled_pos] += (0, FOOD_PHEROMONE, 0)

    def update_without_food(self, randDir, scaled_pos):
        random_angle = random.uniform(-8, 8)
        self.desireDir = self.desireDir.rotate(random_angle)
        if food_sources:
            self.update_with_food_sources(randDir, scaled_pos)
        else:
            #self.move_towards_food(scaled_pos, 1)
            self.last_try(scaled_pos)
        if self.last_sdp != scaled_pos:
            self.phero.img_array[scaled_pos] += (0, 0, HOME_PHEROMONE)

    def random_walk(self):
        self.desireDir = self.desireDir.rotate(random.uniform(*self.angle_range))


    def update_with_food_sources(self, randDir, scaled_pos):
        min_distance = float("inf")
        nearest_food = None
        random_scale = 0.11
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
                    #self.move_towards_food(scaled_pos, 1)
                    self.last_try(scaled_pos)
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
    

    """def move_towards_food(self, scaled_pos, channel):
        directions = [pygame.Vector2(0, -1), pygame.Vector2(-1, 0), pygame.Vector2(1, 0), pygame.Vector2(0, 1)]
        up = self.phero.img_array[scaled_pos[0], scaled_pos[1] - 1, channel]
        right = self.phero.img_array[scaled_pos[0] + 1, scaled_pos[1], channel]
        left = self.phero.img_array[scaled_pos[0] -1, scaled_pos[1], channel]
        down = self.phero.img_array[scaled_pos[0], scaled_pos[1] +1, channel]
        print(up, right, left, down)
        if left == right == up == down == 0:
            self.random_walk()
        else:
            if up < min(right, left, down):
                self.desireDir = directions[0]
                print("up: ", up)
        
            elif right < min(left, down):
                self.desireDir = directions[2]
                print("right: ", right)
            elif left < down:
                self.desireDir = directions[1]
                print("left: ", left)
            else:
                self.desireDir = directions[3]
                print("down: ", down)"""
    
    def last_try(self, scaled_pos):
        right_sensor_dir = self.desireDir.rotate(-10)
        left_sensor_dir = self.desireDir.rotate(10)
        straight_sensor_dir = self.desireDir

        right_sensor_index = (int(scaled_pos[0] + right_sensor_dir[0]), int(scaled_pos[1] + right_sensor_dir[1]))
        left_sensor_index = (int(scaled_pos[0] + left_sensor_dir.x), int(scaled_pos[1] + left_sensor_dir[1]))
        straight_sensor_index = (int(scaled_pos[0] + straight_sensor_dir.x), int(scaled_pos[1] + straight_sensor_dir[1]))

        right = self.phero.img_array[right_sensor_index[0], right_sensor_index[1]][1]
        left = self.phero.img_array[left_sensor_index[0], left_sensor_index[1]][1]
        straight = self.phero.img_array[straight_sensor_index[0], straight_sensor_index[1]][1]

        if right > max(left, straight):
            self.desireDir = right_sensor_dir
            print("right")
        elif left > straight:
            self.desireDir = left_sensor_dir
            print("left")
        else:
            self.desireDir = straight_sensor_dir
            print("straight")

class Pheromones:
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        self.img_array -= 0.4  # Evaporation rate
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
