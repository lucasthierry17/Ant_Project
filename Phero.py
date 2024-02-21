import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 1200, 800
num_ants = 10
PRATIO = 4 # ratio between screen and phero_grid
nest = (WIDTH // 3.5, HEIGHT // 2)
VSYNC = True
SHOWFPS = True
food_sources = []
ALPHA = 7
BETA = 1
PHERO_THRESH = 5
ant_positions_home = np.zeros((num_ants + 1, 2), dtype=int)
ant_positions_home[-1] = nest
amnt_food = len(food_sources)
ant_positions_food = np.zeros((num_ants + amnt_food, 2))


class Ants(pygame.sprite.Sprite):
    def __init__(self, nest, pheromones):
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
        self.search_for_food = False
        self.alpha = ALPHA
        self.beta = BETA
        self.backend_pheromones_home = np.full((num_ants+1), 1)
        self.backend_pheromones_home[-1] = 100
        self.backend_pheromones_food = np.full((num_ants+len(food_sources)),0)
        self.backend_pheromones_food[len(food_sources):] = 200
        
   

    def get_pheromone_positions(self):
        '''
        Getting the positions on the board where the Pheromon Value is greater than the Threshold.
        Also getting the actual pheromone value at those Positions
        '''
        # Assuming PHERO_THRESH is defined somewhere in your code
        high_phero = np.argwhere(self.phero.img_array[:, :, 1] > PHERO_THRESH)

        print(f"High Phero:\n{high_phero}")
        phero_positions = np.array(list(zip(high_phero[:, 0], high_phero[:, 1])))
        print(f"Phero Positions:\n{phero_positions}")

        high_phero_differences = phero_positions - self.rect.center
        high_phero_distances = np.linalg.norm(high_phero_differences, axis=1)
        print(f"Phero Distances:\n{high_phero_distances}")

        # Assuming food_sources is defined somewhere in your code
        # You might need to adjust the length based on your actual requirements
        phero_values = high_phero_distances / 10
        #print(f"Unrounded Distances:\n{1000 / high_phero_distances}")

        # Print or use phero_values as needed
        print(f"Pheromone Values:\n {phero_values}")

        return phero_positions, phero_values


    def update(self):
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))
        # Move the ant
        

        if self.has_food: # ant has food
            distance = self.calculate_distance(scaled_pos, ((nest[0] / PRATIO), (nest[1] / PRATIO)))
            if distance < 5: # ant has reached the nest
                self.has_food = False 
                """
                elif distance > 30 or self.phero.img_array[scaled_pos][2] < 75:
                    self.desireDir = pygame.Vector2(nest[0] - self.x, nest[1] - self.y).normalize() # go towards the nest
                    
                    random_angle = random.uniform(-50, 50)
                    self.desireDir.rotate_ip(random_angle)
                    # Blend the straight direction with the random direction
                
                else:
                    self.desireDir = pygame.Vector2(nest[0] - self.x, nest[1] - self.y).normalize() # go towards the nest
                """
            else:
                
                # Calculation of all differences from the ants current position to the others
                differences = ant_positions_home - self.rect.center
                #print(f"Alle Richtungsvektoren:\n{differences}")
                
                # Calculation of the actual distanc
                eta = np.linalg.norm(differences, axis=1)

                # Total for the nominator:
                total = sum((self.backend_pheromones_home ** self.alpha) * (eta ** self.beta))

                # Calculating the Probabilities:
                probs = ((self.backend_pheromones_home ** ALPHA) * (eta ** BETA)) / total
                #print(f"Wahrscheinlichkeiten: {probs}")
                # Choosing the next direction according to the calculated probs
                cumulative_probs = np.cumsum(probs)
                random_value = np.random.rand() # Random Value between 0 and 1
                selected_position_index = np.searchsorted(cumulative_probs, random_value)
                #print(f"Ausgesuchte Position: {selected_position_index}")
                # Richtungsvektor wird ausgesucht und durch den eigenen halbierten Betrag des Richtungsvektors dividiert
                direction_vector = differences[selected_position_index] / (eta[selected_position_index] / 3)
                
                # Checking for negative Values:

                #print(f"Direction Vector: {direction_vector}")
                #print(f"Der Punkt zuvor: ({self.x}, {self.y})")
                self.x += direction_vector[0]
                self.y += direction_vector[1]
                #print(f"Der neue Punkt: ({self.x}, {self.y})")
                self.phero.img_array[scaled_pos] += (0, 100, 0) # update pheromones


        else: # ant has no food
            if food_sources:
                for i,food in enumerate(food_sources):
                    distance = self.calculate_distance(scaled_pos, food)
                    
                    if distance < 9: # reaches the food source
                        self.has_food = True
                        break
            
                    
                    elif self.phero.img_array[scaled_pos][1] > 20: # smells and goes to the food
                        #self.desireDir = pygame.Vector2(food[0] - scaled_pos[0], food[1] - scaled_pos[1])
                        food_index = i + amnt_food
                        
                        pheromone_position, pheromone_values = self.get_pheromone_positions()
                        pheromone_position[food_index] = np.array(food) * PRATIO
                        distance_ant_food = np.linalg.norm(self.rect.center - (np.array(food)) * PRATIO)
                        print(f"Distance_ant_food:\n{distance_ant_food}")

                        if distance_ant_food < 50:
                            pheromone_values[food_index] = 0
                        else:
                            pheromone_values[food_index] = 100000000 / distance_ant_food
                        differences = pheromone_position - self.rect.center
                        # Calculation of the actual distanc
                        eta = np.linalg.norm(differences, axis=1)
                        print(f"eta: {eta}\n{eta.shape}")
                        #print(f"Eta:\n{eta}\n{eta.shape}")
                        #print(f"Eta:\n{eta}")
                        print(f"Pheromone_values:{pheromone_values}\n{pheromone_values.shape}")

                        # Total for the nominator:
                        total = sum((pheromone_values ** self.alpha) * (eta ** self.beta))

                        # Calculating the Probabilities:
                        probs = ((pheromone_values ** ALPHA) * (eta ** BETA)) / total
                        #print(f"Wahrscheinlichkeiten: {probs}")
                        #print(f"Wahrscheinlichkeiten: {probs}")
                        # Choosing the next direction according to the calculated probs
                        cumulative_probs = np.cumsum(probs)
                        random_value = np.random.rand() # Random Value between 0 and 1
                        selected_position_index = np.searchsorted(cumulative_probs, random_value)
                        #print(f"Ausgesuchte Position: {selected_position_index}")
                        # Richtungsvektor wird ausgesucht und durch den eigenen halbierten Betrag des Richtungsvektors dividiert
                        direction_vector = differences[selected_position_index] / (eta[selected_position_index] / 2)
                        
                        # Checking for negative Values:

                        
                        self.x += direction_vector[0]
                        self.y += direction_vector[1]


            # Move randomly if no food source is found
            
            angle_change = random.uniform(*self.angle_range)
            self.desireDir = self.desireDir.rotate(angle_change).normalize()
            #print(f"food_array: {food_array}\nhome_array: {home_array}")
            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, 50)
        
        self.x += self.desireDir[0] * 2
        self.y += self.desireDir[1] * 2
        
        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            # Bounce back if the ant goes out of the screen 
            self.desireDir *= -1
            self.x += self.desireDir[0] * 2
            self.y += self.desireDir[1] * 2

        self.rect.center = (self.x, self.y)


        #print(f"Ant position: {ant_positions}")

    def calculate_distance(self, start, target): #  calculates distance between two points
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)
    

class Pheromones:
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)
        

    def update(self):
        self.img_array -= 0.5  # Evaporation rate
        self.img_array = self.img_array.clip(0, 255) # clip to color range
        pygame.surfarray.blit_array(self.image, self.img_array) 
        return self.image

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=VSYNC) 
    pheromones = Pheromones((WIDTH, HEIGHT)) # creating phero grid
    ants = pygame.sprite.Group()

    for _ in range(num_ants): # adding num_ants
        ants.add(Ants(nest, pheromones))

    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()

                if event.button == 1:
                    food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
                    mousepos_ratio = (mousepos[0] // PRATIO, mousepos[1] // PRATIO)
                    
                elif event.button == 3:
                    for source in food_sources:
                        if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < 15:
                            food_sources.remove(source)

        phero_grid = pheromones.update()
        ants.update()
        for i, ant in enumerate(ants):
            ant_positions_home[i] = ant.rect.center
            ant_positions_food[i] = ant.rect.center

        #print(f"Ant position: {ant_positions}")

        # Draw everything onto the screen
        screen.fill(0)  # Fill black for the next step
        scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT)) # scale phero_grid back to normal screen size
        screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
        pygame.draw.circle(screen, [70, 50, 40], nest, 16, 5)  # Draw nest

        # Draw food sources
        for source in food_sources:
            pygame.draw.circle(screen, (0, 200, 0), (source[0] * PRATIO, source[1] * PRATIO), 30) # draw food

        ants.draw(screen)  # Draw ants directly onto the screen

        pygame.display.update()

if __name__ == "__main__":
    main()
