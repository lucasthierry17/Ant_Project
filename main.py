"""Imports"""
import math
import random
import pygame
import numpy as np
from start_screen import StartMenu

# Defining Constants
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
    """ This class encapsulates the behavior and attributes of the ants. It serves as a blueprint
        for creating individual ant instances. The primary functionality of this class is to control
        the orientation and movement of the ants within the simulation. 
        
        The ants' orientation is determined by their initial angle and is subject to random changes within a specified range.
        Additionally, the class handles the ants' interaction with food sources, their navigation
        towards the nest, and the updating of pheromone trails left by the ants.
        
        The behavior is dependent on whether an ant is carrying food or not, and it includes methods for random
        walking and turning around upon reaching certain conditions."""
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
        self.has_food = False   # Status of the ant
        self.my_food_source = []    # food_source to which the ant is goint to
        self.speed = speed

    def scaled_pos(self, pos_x, pos_y):
        """scales the position down to our ratio"""
        scaled_pos=(int(pos_x / PRATIO), int(pos_y / PRATIO))
        return scaled_pos

    def update(self):
        """Updates the position depending on the status of the ant"""
        min_distance = 1000
        scaled_pos = self.scaled_pos(self.x_pos, self.y_pos)

        # Check the food status of the ant
        if self.has_food:  

            # Calculate distance to the nest
            distance = self.calculate_distance(
                scaled_pos, ((NEST[0] / PRATIO), (NEST[1] / PRATIO))
            )
            if distance < 5:  # ant has reached the nest
                self.has_food = False   # Change the status of the ant
                self.turn_around()

            # If the ant collides with a pheromone_value greater than 75, it should follow the direction vector to the nest
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
        
        # The food status of the ant is false
        else:  
            if FOOD_SOURCES:
                for food in FOOD_SOURCES:
                    distance = self.calculate_distance(scaled_pos, food)  # Calculates distances from its own position to all food sources
                    if distance < min_distance:
                        min_distance = distance  # Getting the closest food source by searching for the minimum distance
                        closest_food = food
                    if distance < 5:  # reaches the food source
                        self.has_food = True # Change the food status
                        self.my_food_source = food  # The found food_status is now marked 
                        if self.my_food_source not in FOOD_SOURCES:
                            self.my_food_source = None
                        break
                    
            # Move towards the food source if it's not too far or if pheromone value is high enough
                if min_distance < 15 or self.phero.img_array[scaled_pos][1] > 75:
                    if self.my_food_source: # If a marked food source is given, calculate the distance to its own position
                        self.desire_dir = pygame.Vector2(self.my_food_source[0] - scaled_pos[0], self.my_food_source[1] - scaled_pos[1])
                    else: 
                        # If no marked food source is given, calculate the distance to its own position
                        self.desire_dir = pygame.Vector2(closest_food[0] - scaled_pos[0], closest_food[1] - scaled_pos[1])
            else:
                closest_food = None
            if scaled_pos == self.my_food_source and self.my_food_source not in FOOD_SOURCES:
                self.my_food_source = None

            # Move randomly if no food source is found
            self.random_walk()

            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, HOME_PHEROMONE)

        # Update the position of the ant
        self.x_pos += self.desire_dir[0] * self.speed
        self.y_pos += self.desire_dir[1] * self.speed

        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x_pos, self.y_pos):
            # Bounce back if the ant goes out of the screen 
            self.turn_around()

        self.rect.center = (self.x_pos, self.y_pos) # Defining the new center of the ant

    def calculate_distance(self, start, target): 
        """calculates distance between two points"""
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)
    
    def turn_around(self):
        """turns the direction of the ant"""
        self.desire_dir *= -1
        self.x_pos += self.desire_dir[0] * self.speed
        self.y_pos += self.desire_dir[1] * self.speed

    def random_walk(self):
        """Introduces a random movement pattern for the ant."""
        # Generate a random angle within the specified range
        angle_change = random.uniform(*self.angle_range)

        # Rotate the current direction vector by the random angle
        self.desire_dir = self.desire_dir.rotate(angle_change)

        # Check if the resulting direction has a non-zero length
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
    """ 
    Game Loop

    This function represents the main game loop, orchestrating the flow of the simulation.
    It initializes Pygame, sets up the StartMenu, and prepares necessary components such
    as pheromones and ant groups.
    
    The Pygame display is updated within the nested loop, and the screen is filled with black
    in preparation for the next frame. The pheromone grid is scaled back to the original
    screen size and drawn onto the screen. The nest and food sources are drawn as circles,
    and ant instances are directly drawn onto the screen.

    Note: This function assumes the existence of the following global variables/constants:
    - WIDTH, HEIGHT, NUM_ANTS, PRATIO, NEST, VSYNC, SPEED, HOME_PHEROMONE, FOOD_PHEROMONE,
      DECAY_RATE, NEST_SIZE, FOOD_SOURCES.
    - Ants class, Pheromones class, and necessary imports.
    """
    # Initialize Pygame
    pygame.init()
    start_menu = StartMenu() # Create an instance of the StartMenu class

   # Store the original screen size for later use
    start_screen_size = (
        pygame.display.get_surface().get_size()
    )  # Store the original screen size

    pheromones = Pheromones((WIDTH, HEIGHT))  # # Create an instance of the Pheromones class to represent the pheromone grid
    ants = pygame.sprite.Group() # Create a Pygame sprite group to manage ant instances

    # Flag to control the main loop    
    ready_to_go = True

    # Main game loop
    while ready_to_go:
        # Check the current state of the game
        if start_menu.game_state == "start_menu":
            pygame.display.set_caption("Start Menu") # Set the Pygame window caption to "Start Menu"
            
            # Handle events, update, and draw the start menu
            start_menu.handle_events()
            start_menu.draw()

            # Clear everything when returning to the start menu
            ants.empty()    # Remove all ant instances
            pheromones.reset()  # Reset the pheromone grid
            FOOD_SOURCES.clear()     # Clear the list of food sources

        elif start_menu.game_state == "Simulation":
            # Set the Pygame window caption to "Simulation"
            pygame.display.set_caption("Simulation")

            # Create ant instances based on the user-specified number
            for _ in range(
                int(start_menu.num_ants)
            ):  # adding the number of ants the user types in
                ants.add(Ants(NEST, pheromones, speed=float(start_menu.speed)))

            # Create a Pygame window for the simulation
            screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=VSYNC)

            # Flag to control the simulation loop
            running = True
            while running:
                # Event handling
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

                        # Placing the food source with left-click
                        if event.button == 1:
                            FOOD_SOURCES.append(
                                (mousepos[0] // PRATIO, mousepos[1] // PRATIO)
                            )

                        # Removing the food source with right-click
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

                # Update pheromones and ants
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

                pygame.display.update() # Update the display

if __name__ == "__main__":
    main()