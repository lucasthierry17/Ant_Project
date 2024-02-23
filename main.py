"""
Ant Search Simulation Main Module

This module defines the main simulation for the ant search. It utilizes the StartMenu class
from the 'start_screen' module to manage the start menu. Ants, pheromones, and food sources
are simulated on the screen.

Classes:
- Ants: Sprite class representing ants in the simulation.
- Pheromones: Class managing the pheromone grid in the simulation.

Functions:
- main(): Main function to run the simulation.
"""

import pygame
import numpy as np
import math
import random
from start_screen import StartMenu

WIDTH, HEIGHT = 1200, 800
num_ants = 100
PRATIO = 5 # ratio between screen and phero_grid
nest = (WIDTH // 3.5, HEIGHT // 2)
VSYNC = True
SHOWFPS = True
food_sources = []

class Ants(pygame.sprite.Sprite):

    def __init__(self, nest, pheromones, speed):
        super().__init__()
        self.x, self.y = nest # starting coordinates
        self.phero = pheromones 
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (120, 45, 45), (6, 5), 3) # draw_ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.start_ang = random.randint(0, 360)  # Initial angle between 0 and 360 degrees
        self.angle_range = (-10, 10)  # Range for random angle change
        self.desireDir = pygame.Vector2(np.cos(np.radians(self.start_ang)), np.sin(np.radians(self.start_ang))) # direction 
        self.has_food = False
        self.speed = speed


    def update(self):
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))
        # Move the ant
        

        if self.has_food: # ant has food
            distance = self.calculate_distance(scaled_pos, ((nest[0] / PRATIO), (nest[1] / PRATIO)))
            if distance < 5: # ant has reached the nest
                self.has_food = False 
            
            elif distance > 30 or self.phero.img_array[scaled_pos][2] < 75:
                self.desireDir = pygame.Vector2(nest[0] - self.x, nest[1] - self.y).normalize() # go towards the nest
                
                random_angle = random.uniform(-50, 50)
                self.desireDir.rotate_ip(random_angle)
                # Blend the straight direction with the random direction
            
            else:
                self.desireDir = pygame.Vector2(nest[0] - self.x, nest[1] - self.y).normalize() # go towards the nest

            self.phero.img_array[scaled_pos] += (0, 200, 0) # update pheromones

        else: # ant has no food
            if food_sources:
                for food in food_sources:
                    distance = self.calculate_distance(scaled_pos, food)
                    if distance < 5: # reaches the food source
                        self.has_food = True
                        break
                    elif distance < 30 or self.phero.img_array[scaled_pos][1] > 75: # smells and goes to the food
                        self.desireDir = pygame.Vector2(food[0] - scaled_pos[0], food[1] - scaled_pos[1])
                    
            # Move randomly if no food source is found
            angle_change = random.uniform(*self.angle_range)
            self.desireDir = self.desireDir.rotate(angle_change).normalize()

            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, 50)
        
        self.x += self.desireDir[0] * self.speed
        self.y += self.desireDir[1] * self.speed
        
        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            # Bounce back if the ant goes out of the screen 
            self.desireDir *= -1
            self.x += self.desireDir[0] * self.speed
            self.y += self.desireDir[1] * self.speed

        self.rect.center = (self.x, self.y)

    def calculate_distance(self, start, target): #  calculates distance between two points
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)
    

class Pheromones:
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        self.img_array -= 1  # Evaporation rate
        self.img_array = self.img_array.clip(0, 255) # clip to color range
        pygame.surfarray.blit_array(self.image, self.img_array) 
        return self.image

    def reset(self):
        self.img_array.fill(0)


def main():
    pygame.init()
    start_menu = StartMenu()
    
    start_screen_size = pygame.display.get_surface().get_size()  # Store the original screen size

    pheromones = Pheromones((WIDTH, HEIGHT)) # creating phero grid
    ants = pygame.sprite.Group()
    

    go = True   
    while go:
        if start_menu.game_state == "start_menu":
            pygame.display.set_caption("Start Menu")
            start_menu.handle_events()
            start_menu.draw()

            # Clear everything when returning to the start menu
            ants.empty()
            pheromones.reset()
            food_sources.clear() 

        elif start_menu.game_state == "Simulation":
            pygame.display.set_caption("Simulation")
            for _ in range(int(start_menu.num_ants)): # adding the number of ants the user types in 
                    ants.add(Ants(nest,pheromones,speed=float(start_menu.speed)))

            screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=VSYNC) 
            
            running = True
            while running:
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        go = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            pygame.display.set_mode(start_screen_size)  # Set the screen size back to the original
                            start_menu.game_state = "start_menu"

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mousepos = pygame.mouse.get_pos()

                        if event.button == 1:
                            food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
                        elif event.button == 3:
                            for source in food_sources:
                                if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < 15:
                                    food_sources.remove(source)

                phero_grid = pheromones.update()
                ants.update()

                # Draw everything onto the screen
                screen.fill(0)  # Fill black for the next step
                scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT)) # scale phero_grid back to normal screen size
                screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
                pygame.draw.circle(screen, [70, 50, 40], nest, 16, 5)  # Draw nest

                # Draw food sources
                for source in food_sources:
                    pygame.draw.circle(screen, (0, 200, 0), (source[0] * PRATIO, source[1] * PRATIO), 15) # draw food

                ants.draw(screen)  # Draw ants directly onto the screen

                pygame.display.update()

if __name__ == "__main__":
    main()