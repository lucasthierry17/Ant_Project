"""Imports"""
import math
import random
import pygame
import numpy as np
from start_screen import StartMenu


WIDTH, HEIGHT = 1200, 800
NUM_ANTS = 300 # number of ants
PRATIO = 5 # ratio between screen and phero_grid
NEST = (WIDTH // 3.5, HEIGHT // 2) 
VSYNC = True
SPEED = 2
HOME_PHEROMONE = 50
FOOD_PHEROMONE = 70
DECAY_RATE = 0.6
NEST_SIZE = 30
FOOD_SOURCES = [] 

class Ants(pygame.sprite.Sprite):
    """ANT Class, changes the ant orientation"""
    def __init__(self, nest, pheromones, speed):
        super().__init__()
        self.x_pos, self.y_pos = nest  # starting coordinates
        self.phero = pheromones
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (120, 45, 45), (6, 5), 3)  # draw_ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.start_ang = random.randint(
            0, 360
        )  # Initial angle between 0 and 360 degrees
        self.angle_range = (-10, 10)  # Range for random angle change
        self.desire_dir = pygame.Vector2(
            np.cos(np.radians(self.start_ang)), np.sin(np.radians(self.start_ang))
        )  # direction
        self.has_food = False
        self.my_food_source = []
        self.speed = speed

    def scaled_pos(self, pos_x, pos_y):
        """scales the position down to our ratio"""
        scaled_pos=(int(pos_x / PRATIO), int(pos_y / PRATIO))
        return scaled_pos

    def update(self):
        min_distance = 1000
        scaled_pos = self.scaled_pos(self.x_pos, self.y_pos)
        # Move the ant

        if self.has_food:  # ant has food
            distance = self.calculate_distance(
                scaled_pos, ((NEST[0] / PRATIO), (NEST[1] / PRATIO))
            )
            if distance < 5:  # ant has reached the nest
                self.has_food = False
                self.turn_around()

            elif distance > 30 or self.phero.img_array[scaled_pos][2] < 75:
                self.desire_dir = pygame.Vector2(
                    NEST[0] - self.x_pos, NEST[1] - self.y_pos
                ).normalize()  # go towards the nest

                random_angle = random.uniform(-50, 50)
                self.desire_dir.rotate_ip(random_angle)
                # Blend the straight direction with the random direction

            else:
                self.desire_dir = pygame.Vector2(
                    NEST[0] - self.x_pos, NEST[1] - self.y_pos
                ).normalize()  # go towards the nest

            self.phero.img_array[scaled_pos] += (0, FOOD_PHEROMONE, 0)  # update pheromones

        else:  # ant has no food
            if FOOD_SOURCES:
                for food in FOOD_SOURCES:
                    distance = self.calculate_distance(scaled_pos, food)
                    if distance < min_distance:
                        min_distance = distance
                        closest_food = food
                    if distance < 5:  # reaches the food source
                        self.has_food = True
                        self.my_food_source = food
                        if self.my_food_source not in FOOD_SOURCES:
                            self.my_food_source = None
                        break
                    
                # Move towards the food source if it's not too far or if pheromone value is high enough
                if min_distance < 15 or self.phero.img_array[scaled_pos][1] > 75:
                    if self.my_food_source:
                        self.desire_dir = pygame.Vector2(self.my_food_source[0] - scaled_pos[0], self.my_food_source[1] - scaled_pos[1])
                    else:
                        self.desire_dir = pygame.Vector2(closest_food[0] - scaled_pos[0], closest_food[1] - scaled_pos[1])
            else:
                closest_food = None
            if scaled_pos == self.my_food_source and self.my_food_source not in FOOD_SOURCES:
                self.my_food_source = None

            # Move randomly if no food source is found
            self.random_walk()

            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, HOME_PHEROMONE)

        self.x_pos += self.desire_dir[0] * self.speed
        self.y_pos += self.desire_dir[1] * self.speed

        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x_pos, self.y_pos):
            # Bounce back if the ant goes out of the screen 
            self.turn_around()

        self.rect.center = (self.x_pos, self.y_pos)

    def calculate_distance(self, start, target): 
        """calculates distance between two points"""
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)
    
    def turn_around(self):
        """turns the direction of the ant"""
        self.desire_dir *= -1
        self.x_pos += self.desire_dir[0] * self.speed
        self.y_pos += self.desire_dir[1] * self.speed

    def random_walk(self):
        angle_change = random.uniform(*self.angle_range)
        self.desire_dir = self.desire_dir.rotate(angle_change)
        if self.desire_dir.length() > 0:
            self.desire_dir = self.desire_dir.normalize()
        else:
            # If the length of the vector is zero, generate a new random direction
            random_angle = random.uniform(0, 360)
            self.desire_dir = pygame.Vector2(1, 0).rotate(random_angle)
    

class Pheromones:
    """This class handles generating and updating the Pheromone arrays"""
    def __init__(self, big_screen_size):
        self.surf_screen_size = (int(big_screen_size[0] / PRATIO), int(big_screen_size[1] / PRATIO))
        self.image = pygame.Surface(self.surf_screen_size).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        """The Pheromone Array"""
        self.img_array -= DECAY_RATE  # update pheromone values
        self.img_array = self.img_array.clip(0, 255) # clip to color range
        pygame.surfarray.blit_array(self.image, self.img_array) 
        return self.image
    
    def reset(self):
        """Resets the the array"""
        self.img_array.fill(0)

def main():
    """Game Loop"""
    pygame.init()
    start_menu = StartMenu()

    start_screen_size = (
        pygame.display.get_surface().get_size()
    )  # Store the original screen size

    pheromones = Pheromones((WIDTH, HEIGHT))  # creating phero grid
    ants = pygame.sprite.Group()

    ready_to_go = True
    while ready_to_go:
        if start_menu.game_state == "start_menu":
            pygame.display.set_caption("Start Menu")
            start_menu.handle_events()
            start_menu.draw()

            # Clear everything when returning to the start menu
            ants.empty()
            pheromones.reset()
            FOOD_SOURCES.clear()

        elif start_menu.game_state == "Simulation":
            pygame.display.set_caption("Simulation")
            for _ in range(
                int(start_menu.num_ants)
            ):  # adding the number of ants the user types in
                ants.add(Ants(NEST, pheromones, speed=float(start_menu.speed)))

            screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=VSYNC)

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        ready_to_go = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            pygame.display.set_mode(
                                start_screen_size
                            )  # Set the screen size back to the original
                            start_menu.game_state = "start_menu"

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mousepos = pygame.mouse.get_pos()

                        if event.button == 1:
                            FOOD_SOURCES.append(
                                (mousepos[0] // PRATIO, mousepos[1] // PRATIO)
                            )
                        elif event.button == 3:
                            for source in FOOD_SOURCES:
                                if (
                                    math.dist(
                                        mousepos,
                                        (source[0] * PRATIO, source[1] * PRATIO),
                                    )
                                    < 15
                                ):
                                    FOOD_SOURCES.remove(source)

                phero_grid = pheromones.update()
                ants.update()

                # Draw everything onto the screen
                screen.fill(0)  # Fill black for the next step
                scaled_screen = pygame.transform.scale(
                    phero_grid, (WIDTH, HEIGHT)
                )  # scale phero_grid back to normal screen size
                screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
                pygame.draw.circle(screen, [70, 50, 40], NEST, NEST_SIZE)  # Draw nest


                # Draw food sources
                for source in FOOD_SOURCES:
                    pygame.draw.circle(
                        screen,
                        (0, 200, 0),
                        (source[0] * PRATIO, source[1] * PRATIO),
                        15,
                    )  # draw food

                ants.draw(screen)  # Draw ants directly onto the screen

                pygame.display.update()

if __name__ == "__main__":
    main()