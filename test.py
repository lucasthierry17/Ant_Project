import math
import numpy as np
import random
import pygame

WIDTH, HEIGHT = 900, 600
NUM_ANTS = 10
PRATIO = 4  # Ratio between screen and phero_grid
NEST = (WIDTH // 5, HEIGHT // 4)
VSYNC = True
SHOWFPS = True
FOOD_RADIUS = 25
SPEED= 2
NEST_SIZE = 10
HOME_PHEROMONE = 200
FOOD_PHEROMONE = 100
SIZE_ANT = 3
MAX_DISTANCE = 0
food_sources = []


class Ants(pygame.sprite.Sprite):
    """Class representing ants in the simulation."""
    def __init__(self, nest, pheromones):
        """
        Initialize an Ant instance.

        Parameters:
        - nest (tuple): Tuple representing the starting coordinates (x, y) of the ant.
        - pheromones (Pheromones): Pheromones object representing the pheromone grid.

        Attributes:
        - x (float): The x-coordinate of the ant's current position.
        - y (float): The y-coordinate of the ant's current position.
        - phero (Pheromones): Pheromones object associated with the ant.
        - angle (int): Initial angle representing the orientation of the ant.
        - image (pygame.Surface): Surface representing the visual appearance of the ant.
        - orig_image (pygame.Surface): Rotated version of the original image for proper orientation.
        - rect (pygame.Rect): Rectangle representing the bounding box of the ant's image.
        - pos (pygame.Vector2): Vector representing the center of the ant's bounding box.
        - angle_range (tuple): Range for random angle adjustments during movement.
        - desire_dir (Vector2): Vector representing the desired direction of the ant's movement.
        - has_food (bool): True if the ant is carrying food, False otherwise.
        - last_sdp (tuple): Last scaled down position to track changes in the pheromone grid.
        """
        super().__init__()
        self.x, self.y = nest  # Starting coordinates
        self.phero = pheromones
        self.angle = random.randint(0, 360)
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (6, 5), SIZE_ANT) # Draw ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.pos = pygame.Vector2(self.rect.center)
        self.angle_range = (-8, 8) # Range for random angle change
        self.desire_dir = pygame.Vector2(np.cos(np.radians(self.angle)),
                                        np.sin(np.radians(self.angle))) # Direction
        self.has_food = False # True if food, else False
        self.last_sdp = (nest[0]/10/2,nest[1]/10/2)


    def update(self):
        """Update the ant's position."""
        # global MAX_DISTANCE, SPEED
        angle = random.randint(0, 360)
        rand_dir = pygame.Vector2(np.cos(np.radians(angle)), np.sin(np.radians(angle)))
        random_scale = 0.11
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))

        if self.has_food:
            self.update_with_food(rand_dir, random_scale, scaled_pos)
        else:
            self.update_without_food(scaled_pos)
        self.move()
        self.check_boundaries()

    def update_with_food(self, rand_dir, random_scale, scaled_pos):
        """Update the ant's position when it has food."""
        global MAX_DISTANCE
        distance = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))
        if distance > MAX_DISTANCE:
            MAX_DISTANCE = distance
        if distance < (NEST_SIZE / PRATIO):
            self.has_food = False
            self.turn_around()
        elif distance > MAX_DISTANCE - 15:
            self.desire_dir = pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize()
        else:
            # Gradual adjustment towards the direction of the nest
            self.desire_dir += pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize() * .08
            self.desire_dir = pygame.Vector2(self.desire_dir + rand_dir * random_scale).normalize()

        pheromone_value = 255 * (distance / MAX_DISTANCE)
        pheromone_value = min(pheromone_value, 255)

        if scaled_pos != self.last_sdp:
            # Deposit pheromones on the ground based on the distance to the nest
            self.phero.img_array[scaled_pos] += (0, pheromone_value, 0)

    def update_without_food(self, scaled_pos):
        """Update the ant's position when it doesn't have food."""
        random_angle = random.uniform(-8, 8)
        # Randomly adjust the ant's direction
        self.desire_dir = self.desire_dir.rotate(random_angle)
        if food_sources:
            self.update_with_food_sources(scaled_pos)
        else:
            #self.move_towards_food(scaled_pos, 1)
            # If there are no food sources, follow pheromones
            self.follow_pheromones(scaled_pos, 1)
        if self.last_sdp != scaled_pos:
            # Deposit home pheromones on the ground
            self.phero.img_array[scaled_pos] += (0, 0, HOME_PHEROMONE)

    def random_walk(self):
        """Make the ant walk around randomly by changing its direction randomly."""
        self.desire_dir = self.desire_dir.rotate(random.uniform(*self.angle_range))


    def update_with_food_sources(self, scaled_pos):
        """Update the ant's position when there are food sources nearby."""
        min_distance = float("inf")
        nearest_food = None
        for food in food_sources:
            distance = self.calculate_distance(scaled_pos, food)
            if distance < min_distance:
                min_distance = distance
                nearest_food = food

                if min_distance < (FOOD_RADIUS / PRATIO):
                    # If the ant is close to a food source, pick up the food
                    self.has_food = True

                elif min_distance < (FOOD_RADIUS / 2):
                    # Adjust the direction towards the nearest food source
                    self.desire_dir = pygame.Vector2(nearest_food[0] - scaled_pos[0],
                                                    nearest_food[1] - scaled_pos[1]).normalize()

                else:
                    # If not close to a food source, follow pheromones
                    self.follow_pheromones(scaled_pos, 2)
    def move(self):
        """Move the ant based on its current direction and speed."""
        self.x += self.desire_dir[0] * SPEED
        self.y += self.desire_dir[1] * SPEED
        self.rect.center = (self.x, self.y)

    def check_boundaries(self):
        """Check if the ant is within the screen boundaries and turn around if necessary."""
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            self.turn_around()

    def calculate_distance(self, start, target):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((target[0] - start[0]) ** 2 + (target[1] - start[1])**2)

    def turn_around(self):
        """Turn the ant around by reversing its direction."""
        self.desire_dir *= -1
        self.x += self.desire_dir[0] * SPEED
        self.y += self.desire_dir[1] * SPEED
        return self.x, self.y

    def follow_pheromones(self, scaled_pos, channel): # this function is not done, do not change anything
        """Follow pheromones to determine the ant's direction."""
        right_sensor_dir = self.desire_dir.rotate(-90).normalize() * 2
        left_sensor_dir = self.desire_dir.rotate(90).normalize() * 2
        straight_sensor_dir = self.desire_dir.normalize() * 2
        #print(right_sensor_dir, left_sensor_dir, straight_sensor_dir)

        # Obtain pheromone values from neighboring positions
        right_sensor_index = (int(scaled_pos[0] + right_sensor_dir[0]),
                              int(scaled_pos[1] + right_sensor_dir[1]))
        left_sensor_index = (int(scaled_pos[0] + left_sensor_dir[0]),
                             int(scaled_pos[1] + left_sensor_dir[1]))
        straight_sensor_index = (int(scaled_pos[0] + straight_sensor_dir[0]),
                                 int(scaled_pos[1] + straight_sensor_dir[1]))
        #print(right_sensor_index, left_sensor_index, straight_sensor_index)

        right = self.phero.img_array[right_sensor_index[0], right_sensor_index[1]][channel]
        left = self.phero.img_array[left_sensor_index[0], left_sensor_index[1]][channel]
        straight = self.phero.img_array[straight_sensor_index[0], straight_sensor_index[1]][channel]
        #print(left, right, straight)

        if right == left == straight:
            # If all pheromone values are equal, walk around randomly
            self.random_walk()
            #print("went random")
        else:
            # Determine the direction based on the highest pheromone value
            if right > max(left, straight):
                self.desire_dir = right_sensor_dir
            elif left > straight:
                self.desire_dir = left_sensor_dir
            else:
                self.desire_dir = straight_sensor_dir

class Pheromones:
    """Class representing the pheromone grid in the simulation."""
    def __init__(self, big_size):
        """
        Initialize a Pheromones instance.

        Parameters:
        - big_size (tuple): Tuple representing the size of the entire grid in the simulation.
        """
        self.surf_size = (int(big_size[0] / PRATIO), int(big_size[1] / PRATIO))
        self.image = pygame.Surface(self.surf_size).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        """Update the pheromone grid by applying evaporation and clipping values."""
        self.img_array -= 0.4  # Evaporation rate
        # Clip pheromone values to stay within the color range
        self.img_array = self.img_array.clip(0, 255)
        # Update the pygame surface with the modified pheromone grid
        pygame.surfarray.blit_array(self.image, self.img_array)
        return self.image

def handle_mouse_input(event):
    """
    Handle mouse input events to add or remove food sources.

    Parameters:
    - event (pygame.event.Event): Mouse input event.
    """
    # global food_sources
    mousepos = pygame.mouse.get_pos()
    if event.button == 1:
        # Add a new food source when left-clicked
        food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
    elif event.button == 3:
        # Remove a food source when right-clicked near one
        for source in food_sources:
            if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < FOOD_RADIUS:
                food_sources.remove(source)

def main():
    """Main function to run the simulation."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=VSYNC)
    pheromones = Pheromones((WIDTH, HEIGHT))  # Creating phero grid
    ants = pygame.sprite.Group()
    # global food_sources # Define food_sources locally

    for _ in range(NUM_ANTS):  # Adding num_ants
        ants.add(Ants(NEST, pheromones))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GO = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_input(event)  # Pass event
        phero_grid = pheromones.update()
        ants.update()

        draw(screen, phero_grid, food_sources, ants)  # Pass ants as parameter
    pygame.quit()

def draw(screen, phero_grid, food_sources, ants):
    """
    Draw the simulation elements on the screen.

    Parameters:
    - screen (pygame.Surface): The screen surface to draw on.
    - phero_grid (pygame.Surface): The pheromone grid surface.
    - food_sources (list): List of food source coordinates.
    - ants (pygame.sprite.Group): Group containing ant sprites.
    """
    screen.fill(0)  # Fill black for the next step
    # Scale phero_grid back to normal screen size
    scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT))
    screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
    pygame.draw.circle(screen, [70, 50, 40], NEST, NEST_SIZE)  # Draw nest

    # Draw food sources
    for source in food_sources:
        pygame.draw.circle(screen, (0, 200, 0),
                           (source[0] * PRATIO, source[1] * PRATIO),
                           FOOD_RADIUS)

    ants.draw(screen)  # Draw ants directly onto the screen

    pygame.display.update()

if __name__ == "__main__":
    main()
