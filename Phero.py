import pygame
import numpy as np
import math
import random

WIDTH, HEIGHT = 1200, 800
max_distance = 0
num_ants = 200
PRATIO = 5 # ratio between screen and phero_grid
nest = (WIDTH // 3.5, HEIGHT // 2)
VSYNC = True
SHOWFPS = True
food_sources = []
ALPHA = 5
BETA = 0.5
PHERO_THRESH = 70
EVAPURATION_RATE = 0.8
STEPSIZE = 2
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
        self.coming_from_food_source = None
        self.backend_pheromones_home = np.full((num_ants+1), 1)
        self.backend_pheromones_home[-1] = 100
        self.backend_pheromones_food = np.full((num_ants+len(food_sources)),0)
        self.backend_pheromones_food[len(food_sources):] = 200
        
   

    def get_pheromone_positions(self, color='green'):

        # Getting all the positions that are greater than the Pheromone Threshold
        if color == 'green':
            high_phero_positions = np.argwhere(self.phero.img_array[:, :, 1] > PHERO_THRESH)
        elif color == 'blue':
            high_phero_positions = np.argwhere(self.phero.img_array[:, :, 2] > PHERO_THRESH)

        # Getting the actual values on those positions 
        phero_values = self.phero.img_array[high_phero_positions[:, 0], high_phero_positions[:, 1], 1]
        
        return high_phero_positions, phero_values
    
    
    def get_nearest_food_source(self):
        nearest_food_source = None
        min_distance_food = float('inf')  # Setze min_distance_food auf unendlich zu Beginn

        # If the ant has no food origin it should follow the nearest food source
    
        for food_source in food_sources:
            food_source = np.array(food_source) * PRATIO
            
            distance_food = np.linalg.norm(food_source - self.rect.center)

            if distance_food < min_distance_food:
                min_distance_food = distance_food
                nearest_food_source = food_source
    
        return nearest_food_source



    def colony_optimization(self, positions, pheromones, alpha=ALPHA, beta=BETA, divident=3):

        # Getting Differences between the positions and the ant itself
        differences = positions - self.rect.center
        #print(f"Positions:\n{positions}")
        #print(f"Nest:\n{nest}")
        #print(f"differences:\n{differences}")
        # Calculation of eta, which contains the actual distance to those positions
        eta = np.linalg.norm(differences, axis=1)
        #print(f"eta:\n{eta}")
        #print(f"pheromones:\n{pheromones}")
        # Total forr the nominator
        total = sum((pheromones ** alpha) * (eta ** beta))

        # Calculating the probabilities
        probabilities = ((pheromones ** alpha) * (eta ** beta)) / total
        #print(f"probabilities:\n{probabilities}")
        cumulative_probs = np.cumsum(probabilities)
        random_value = np.random.rand()
        selected_position_index = np.searchsorted(cumulative_probs, random_value)
        direction_vector = differences[selected_position_index] / (eta[selected_position_index] / divident)
        #print(f"Probs:\n{probabilities}")
        #print(f"selected_direction_vector: {differences[selected_position_index]}\nThe Position which was given:{positions[selected_position_index]}")
        return direction_vector

    
    def update(self):
        global max_distance
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))

        # Move the ant
        if self.has_food: # ant has food
            distance = self.calculate_distance(scaled_pos, ((nest[0] / PRATIO), (nest[1] / PRATIO)))
            if distance > max_distance:
                max_distance = distance

            if distance < 5: # ant has reached the nest
                self.has_food = False 
             
            elif self.phero.img_array[scaled_pos[0] % self.phero.img_array.shape[0], scaled_pos[1] % self.phero.img_array.shape[1]][2] > 10 or self.has_food:
                
                pheromone_position, pheromone_values = self.get_pheromone_positions(color='blue')
                pheromone_position = pheromone_position * PRATIO

                # Sobald die Distanz zum Pheromon groß genug ist wird self.searcg_for_food auf False gesetztt:
                min_distance_phero = 0
                distances_phero = pheromone_position - self.rect.center
                distances_phero = np.linalg.norm(distances_phero, axis=0)

                indices =  np.where(distances_phero < 10)
                pheromone_position = pheromone_position[indices]
                pheromone_values = pheromone_values[indices]
                #print(f"Pheromon Werte bevorr nest:\n{pheromone_values}")

                pheromone_position = np.append(pheromone_position, [np.array(nest)], axis=0)
                pheromone_values = np.append(pheromone_values, 1000)
                direction_vector = self.colony_optimization(pheromone_position, pheromone_values)
                
                self.x += direction_vector[0]
                self.y += direction_vector[1]
                
                #self.phero.img_array[scaled_pos] += (0, 100, 0) # update pheromones
            pheromone_value = 255 * (distance / max_distance)
            if pheromone_value > 255:
                pheromone_value = 255  
            self.phero.img_array[scaled_pos] += (0, pheromone_value, 0)


        else: # ant has no food
            
            if food_sources:
                for i,food in enumerate(food_sources):
                    distance = self.calculate_distance(scaled_pos, food)
                    
                    if distance < 7: # reaches the food source
                        self.has_food = True
                        self.coming_from_food_source = self.get_nearest_food_source()
                        food = self.coming_from_food_source / PRATIO
                        
                        self.search_for_food = False
                        break
            

                    elif self.phero.img_array[scaled_pos[0] % self.phero.img_array.shape[0], scaled_pos[1] % self.phero.img_array.shape[1]][1] > 10 or self.search_for_food: # smells and goes to the food
 
                        #self.desireDir = pygame.Vector2(food[0] - scaled_pos[0], food[1] - scaled_pos[1])
                        food_index = i + amnt_food
                        self.search_for_food = True

                        pheromone_position, pheromone_values = self.get_pheromone_positions()
                        pheromone_position = pheromone_position * PRATIO

                        # Sobald die Distanz zum Pheromon groß genug ist wird self.searcg_for_food auf False gesetztt:
                        min_distance_phero = 0
                        distances_phero = pheromone_position - self.rect.center
                        distances_phero = np.linalg.norm(distances_phero, axis=1)

                        indices =  np.where(distances_phero < 100)
                        pheromone_position = pheromone_position[indices]
                        pheromone_values = pheromone_values[indices]
                        #print(f"Distances_phero: {distances_phero}")

                        min_distance_phero = np.min(distances_phero)
                        if min_distance_phero > 10:
                            self.search_for_food = False
                            self.coming_from_food_source = None

                        # Looking for the nearest food_source:
                        
                        #print(f"self.coming_from_food_source: {self.coming_from_food_source}")
                        nearest_food_source = None                
                        # If the ant has no food origin it should follow the nearest food source
                        if not np.any(self.coming_from_food_source):
                            nearest_food_source = self.get_nearest_food_source()
                            pheromone_position = np.append(pheromone_position, [np.array(nearest_food_source)], axis=0)
                            #print(f"Pheromone_position:\n{pheromone_position}\n food_position: {nearest_food_source}")
                            pheromone_values = np.append(pheromone_values, 10000)
                            #print(f"Pheromone_value:\n{pheromone_values}"
                            direction_vector = self.colony_optimization(positions=pheromone_position, pheromones=pheromone_values, divident=1)

                        elif np.any(self.coming_from_food_source):
                            pheromone_position = np.append(pheromone_position, [np.array(self.coming_from_food_source)], axis=0)
                            #print(f"Pheromone_position:\n{pheromone_position}\n food_position: {nearest_food_source}")
                            pheromone_values = np.append(pheromone_values, 10000)
                            #print(f"Pheromone_value:\n{pheromone_values}"
                            direction_vector = self.colony_optimization(positions=pheromone_position, pheromones=pheromone_values, divident=1)

                        else:
                            pheromone_position = np.append(pheromone_position, [np.array(nearest_food_source)], axis=0)
                            #print(f"Pheromone_position:\n{pheromone_position}\n food_position: {nearest_food_source}")
                            pheromone_values = np.append(pheromone_values, 10000)
                            #print(f"Pheromone_value:\n{pheromone_values}"
                            direction_vector = self.colony_optimization(positions=pheromone_position, pheromones=pheromone_values, divident=1)
                        
                        
                        self.x += direction_vector[0]
                        self.y += direction_vector[1]
                    else:
                        angle_change = random.uniform(*self.angle_range)
                        self.desireDir = self.desireDir.rotate(angle_change).normalize()
                        #print(f"food_array: {food_array}\nhome_array: {home_array}")
                        # Update pheromones

            # Move randomly if no food source is found
            
            angle_change = random.uniform(*self.angle_range)
            self.desireDir = self.desireDir.rotate(angle_change).normalize()
            #print(f"food_array: {food_array}\nhome_array: {home_array}")
            # Update pheromones
            self.phero.img_array[scaled_pos] += (0, 0, 50)
        
        self.x += self.desireDir[0] * STEPSIZE
        self.y += self.desireDir[1] * STEPSIZE
        if not food_sources:
            self.search_for_food = False
        # Check for collisions with screen boundaries
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            # Bounce back if the ant goes out of the screen 
            self.desireDir *= -1
            self.x += self.desireDir[0] * STEPSIZE
            self.y += self.desireDir[1] * STEPSIZE

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
        self.img_array -= EVAPURATION_RATE 
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
