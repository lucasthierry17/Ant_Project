import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 1200, 800
num_ants = 75
PRATIO = 5
nest = (WIDTH // 3.5, HEIGHT // 2)
VSYNC = True
SHOWFPS = True
food_sources = []



class Ants(pygame.sprite.Sprite):
    def __init__(self, nest, pheromones):
        super().__init__()
        self.x = nest[0] # starting x coordinate
        self.y = nest[1] # starting y
        self.phero = pheromones
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        #self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (120, 45, 45), (6, 5), 5)
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.start_ang = random.randint(0, 360)  # Initial angle between 0 and 360 degrees
        self.angle_range = (-10, 10)  # Range for random angle change
        self.desireDir = pygame.Vector2(np.cos(np.radians(self.start_ang)), np.sin(np.radians(self.start_ang)))
        self.has_food = False
        self.resposible_food = None

    def update(self):
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))

        if self.has_food:  # ant has food
            distance = self.calculate_distance(scaled_pos, ((nest[0] / PRATIO), (nest[1] / PRATIO)))
            if distance < 5:  # ant has reached the nest
                self.has_food = False
            else:
                # Get pheromone direction
                pheromone_direction = pygame.Vector2(*self.phero.get_direction(scaled_pos))

                # If pheromone gradient is available, normalize and use it
                if pheromone_direction.length() > 0:
                    self.desireDir = pheromone_direction.normalize()
                else:
                    # If no pheromone gradient, move towards the nest
                    self.desireDir = pygame.Vector2(nest[0] - scaled_pos[0], nest[1] - scaled_pos[1]).normalize()

            self.phero.img_array[scaled_pos] += (0, 100, 0)  # update pheromones

        else:  # ant has no food
            # Get pheromone direction
            pheromone_direction = pygame.Vector2(*self.phero.get_direction(scaled_pos))

            # If pheromone gradient is available, normalize and use it
            if pheromone_direction.length() > 0:
                random_angle = random.uniform(0, 360)
                self.desireDir = pygame.Vector2(1, 0).rotate(random_angle)
                #self.desireDir = pheromone_direction.normalize()
            else:
                # If no pheromone gradient, move randomly
                random_angle = random.uniform(0, 360)
                self.desireDir = pygame.Vector2(1, 0).rotate(random_angle)

            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, 75)

        # Move the ant
        self.x += self.desireDir[0] * 2
        self.y += self.desireDir[1] * 2

        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            # Bounce back if the ant goes out of bounds
            self.desireDir *= -1
            self.x += self.desireDir[0] * speed
            self.y += self.desireDir[1] * speed

        self.rect.center = (self.x, self.y)


    def calculate_distance(self, start, target):
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)
    
    
class Pheromones:
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        self.img_array -= 0.8  # Evaporation rate
        self.img_array = self.img_array.clip(0, 255)
        pygame.surfarray.blit_array(self.image, self.img_array)
        return self.image

    def get_direction(self, pos):
        # Calculate the gradient of pheromone intensity in the neighborhood of the position
        x, y = pos
        gradient_x = (self.img_array[x + 1, y][2] - self.img_array[x - 1, y][2]) / 2
        gradient_y = (self.img_array[x, y + 1][2] - self.img_array[x, y - 1][2]) / 2
        return gradient_x, gradient_y
    



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=VSYNC)
    pheromones = Pheromones((WIDTH, HEIGHT))
    ants = pygame.sprite.Group()
    speed = 2
    speed_slide = pygame.Rect(20, 20, 100, 10)

    for _ in range(num_ants):
        ants.add(Ants(nest, pheromones))

    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if event.button == 1:
                    if speed_slide.collidepoint(event.pos):
                        # Calculate speed based on slider position
                        speed = (event.pos[0] - speed_slide.x) / speed_slide.width * 9 + 1  # Speed ranges from 1 to 10
                        # Update the speed for all ants
                        for ant in ants:
                            ant.speed = speed
                    else:
                        mousepos = pygame.mouse.get_pos()
                        food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))

                elif event.button == 3:
                    for source in food_sources:
                        if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < 15:
                            food_sources.remove(source)
                

        phero_grid = pheromones.update()
        ants.update()

        # Draw everything onto the screen
        screen.fill(0)  # Fill black for the next step
        scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT))
        screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
        pygame.draw.circle(screen, [70, 50, 40], nest, 16, 5)  # Draw nest

        # Draw food sources
        for source in food_sources:
            pygame.draw.circle(screen, (0, 200, 0), (source[0] * PRATIO, source[1] * PRATIO), 30)
        pygame.draw.rect(screen, (255, 255, 255), speed_slide)

        ants.draw(screen)  # Draw ants directly onto the screen
        
        pygame.display.update()

if __name__ == "__main__":
    main()
