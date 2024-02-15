import pygame
import numpy as np
from ant_colony import Antcolony

# Define constants

pygame.init()

# Define constants
width, height = 1000, 800
pheromone_decay_rate = 0.99
max_pheromone_value = 10
num_ants = 100
num_food = 200
radius = 10
size_food = 5
step_size = 7
repulsion_distance = 5  # how far the ants will go towards the center
pheri = 7  # this represents their sight of view
nest_position = np.array([width // 2, height // 2])  # set nest to the middle


class Ant:
    def __init__(self):
            # Create a numpy array to represent the pheromone grid
            self.pheromone_home = np.zeros((width, height), dtype=float)
            self.pheromone_food = np.zeros((width, height), dtype=float)
            self.ant_positions = np.full((num_ants, 2), (width // 2, height // 2), dtype=float)
            self.ant_directions = np.random.uniform(0, 360, size=num_ants)
            self.has_food = np.zeros((num_ants), dtype=bool)
            self.aco_food = Antcolony(self.pheromone_home, self.ant_positions)
            self.aco_home = Antcolony(self.pheromone_home, self.ant_positions)
            self.alpha = 1
            self.beta = 1
            self.backend_pheromones = np.full((num_ants+1), 2)
            self.backend_pheromones[-1] = 100

    def calculate_direction(self, start, target):
        """Calculates the direction from the start to the target. It takes in the position of the target and the position of the nest."""
        direction_vector = target - start
        return direction_vector / np.linalg.norm(direction_vector)
    
    def create_arrays(self):
        food_array = np.zeros((num_ants, 2))
        home_array = np.zeros((num_ants, 2))

        # Fill the arrays with the positions of the ants according to their food status
        for ant in range(len(self.ant_positions)):
            if self.has_food[ant]:
                food_array[ant] = self.ant_positions[ant]
                home_array[ant] = [0,0]
            
            elif not self.has_food[ant]:
                food_array[ant] = [0,0]
                home_array[ant] = self.ant_positions[ant]
        # Append nest_position to each row
        home_array = np.vstack([home_array, nest_position])
        food_array = np.vstack([food_array, nest_position])
        return food_array, home_array
        
    def movement(self, positions, directions):
        """this function is for the movement of the ants. First, the ants receive a random direction (self.directions). After the first step, they have a angle of view (set to -40 to 40 degrees). They walk randomly in this site of view. For each step they get a direction (-40 to 40 degrees) and take a step in that direction. If they enter the edge_region, they turn around and take the next step in the opposite direction
        Input: edge_turn_region
        """
        cos_directions = step_size * np.cos(np.radians(directions))
        sin_directions = step_size * np.sin(np.radians(directions))

        for ant in range(len(positions)):
            x, y = positions[ant]
            next_x = x + cos_directions[ant]
            next_y = y + sin_directions[ant]

            if 0 <= next_x <= width and 0 <= next_y <= height:
                x, y = next_x, next_y
            
            else:
                direction_to_center = self.calculate_direction(np.array([x, y]), nest_position)
                directions[ant] = np.degrees(np.arctan2(direction_to_center[1], direction_to_center[0]))
                repulsion_vector = direction_to_center * repulsion_distance
                x += repulsion_vector[0]
                y += repulsion_vector[1]


            if self.has_food[ant]:
                print(f"self.food wurde bei der {ant}. Ameise auf {self.has_food[ant]}")
                food_array, home_array = self.create_arrays()
                print(f"food_array und home_array wurden erstellt. Food Array:\n{food_array}\n Home Array:\n{home_array}")
                differences = home_array - food_array[ant]
                differences[ant] = [0, 0] # Distanz von der Ameise zu ihrer eigenen Position wird auf 0 gesetzt
                print(f"Distanz zu den Punkten wurde ausgerechnet:\n {differences}")
                eta = np.linalg.norm(differences, axis=1)
                print(f"eta: \n{eta}")
                total = sum((self.backend_pheromones ** self.alpha) * (eta ** self.beta))
                print(f"total:\n {total}")
                
            
                probabilities = ((self.backend_pheromones ** self.alpha) * (eta ** self.beta)) / total
                print(f"Wahrscheinlichkeiten wurden ausgerechnet: {probabilities}")
                cumulative_probabilities = np.cumsum(probabilities)
                random_value = np.random.rand()  # Zufälliger Wert zwischen 0 und 1
                selected_position_index = np.searchsorted(cumulative_probabilities, random_value)
                print(f"selection_position_index: {selected_position_index}")

                direction_vector = differences[selected_position_index] / (eta[selected_position_index] / 3)
                print(f"Die nächste Position: {direction_vector}")

                x = direction_vector[0] + positions[ant][0]
                y = direction_vector[1] + positions[ant][1]
                print(f"Richtungsvektor = ({x}, {y})")
    

            
            positions[ant] = (x, y)
            directions[ant] += np.random.uniform(-pheri, pheri)

        return positions

class Food:
    def __init__(self, num_food, radius, min_distance=400):
        self.num_food = num_food
        self.radius = radius
        self.min_distance = min_distance
        self.center = None


    def generate_positions(self):
        angles = np.linspace(0, 2 * np.pi, self.num_food)
        radii = np.sqrt(np.random.uniform(0, 1, self.num_food)) * self.radius

        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        x_center = np.random.randint(50, width // 3)
        y_center = np.random.randint(50, height - 50)

        self.center = x_center, y_center

        self.positions = np.column_stack((x, y)) + self.center
        return self.positions


class Run:
    def __init__(self):
        self.ants = Ant()
        self.screen = pygame.display.set_mode((width, height))
        self.food_positions = Food(num_food, radius).generate_positions()

    def main(self):
        pygame.display.set_caption("Pheromone Grid Visualization")

        # Run the simulation loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update pheromones
            self.ants.pheromone_home *= pheromone_decay_rate #Hier werden die phereomene verblassen nachdem sie später generiert werden an der gleichen position wie die der Ameise
            self.ants.pheromone_food *= pheromone_decay_rate

            # Place pheromones where ants have been
            self.ants.ant_positions = self.ants.movement(self.ants.ant_positions, self.ants.ant_directions)
            # ...

            for ant_pos, has_food in zip(self.ants.ant_positions, self.ants.has_food):
                x, y = ant_pos.astype(int)  # Move this line inside the loop
                #x = np.clip(x, 0, width - 1)  # Ensure x is within the valid range
                #y = np.clip(y, 0, height - 1)  # Ensure y is within the valid range

                if has_food:
                    self.ants.pheromone_food[x, y] += 10
                    distance_to_home = np.linalg.norm(ant_pos - nest_position)
                    if distance_to_home < 30:
                        self.ants.has_food[np.where((self.ants.ant_positions == ant_pos).all(axis=1))] = False
                        self.ants.pheromone_food[x, y] += 10 
                        print("Has_food had been changed to False")

                else:
                    for food_pos in self.food_positions:
                        distance_to_food = np.linalg.norm(ant_pos - food_pos)
                        if distance_to_food < size_food:
                            self.ants.has_food[np.where((self.ants.ant_positions == ant_pos).all(axis=1))] = True
                            print("Has_food had been changed to True")
                        self.ants.pheromone_food[x, y] += 10  # Increase pheromone value
                self.ants.pheromone_home[x, y] += 10  # Increase pheromone value
  # Increase pheromone value

                      # Increase pheromone value

# ...

                
            # Clip pheromone values to the maximum allowed value
            self.ants.pheromone_home[nest_position] = max_pheromone_value
            np.clip(self.ants.pheromone_home, 0, max_pheromone_value, out=self.ants.pheromone_home)
            np.clip(self.ants.pheromone_food, 0, max_pheromone_value, out=self.ants.pheromone_food)

            # Create Pygame surfaces from numpy arrays
            surface_home = pygame.surfarray.make_surface(self.ants.pheromone_home)
            surface_food = pygame.surfarray.make_surface(self.ants.pheromone_food)

            # Display the surfaces
            self.screen.blit(surface_home, (0,0))
            self.screen.blit(surface_food, (0,0))
            pygame.draw.circle(self.screen, (121, 61, 0), (width // 2, height // 2), 30)
            
            # Render ants as red dots
            for ant_pos in self.ants.ant_positions:
                pygame.draw.circle(self.screen, (255, 0, 115), ant_pos.astype(int), 4)
            
            pygame.draw.circle(self.screen, (121, 61, 0), (width // 2, height // 2), 30)
            for food_pos in self.food_positions:
                pygame.draw.circle(self.screen, (0, 255, 0), food_pos.astype(int), size_food)

            pygame.display.flip()

        pygame.quit()


main = Run()

if __name__ == "__main__":
    main.main()