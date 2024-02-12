import time
import matplotlib.pyplot as plt
import numpy as np


class Ants:
    """This class contains the functions movement, perception and approach_food."""

    def __init__(self, num_ants):
        self.positions = np.zeros((num_ants, 2)) # ants start at the nest location
        self.directions = np.random.uniform(0, 360, size=num_ants) # degree between 0 and 360
        self.carrying_food = np.zeros(num_ants, dtype=bool)

    def calculate_direction(self, start, target):
        direction_vector = target - start
        direction = direction_vector / np.linalg.norm(direction_vector)
        return direction


    def movement(self, edge_turn_region=1, repulsion_distance=3):
        """this function is for the movement of the ants. First, the ants receive a random direction (self.directions). After the first step, they have a angle of view (set to -40 to 40 degrees). They walk randomly in this site of view. For each step they get a direction (-40 to 40 degrees) and take a step in that direction. If they enter the edge_region, they turn around and take the next step in the opposite direction
        Input: edge_turn_region
        """

        cos_directions = np.cos(np.radians(self.directions))  # chooses the direction on the x axis
        sin_directions = np.sin(np.radians(self.directions))  # same on the y axis

         
        for ant in range(len(self.positions)):
            x, y = self.positions[ant]
            next_x = x + cos_directions[ant]  # computes the next x coordinates
            next_y = y + sin_directions[ant]  # computes the next y coordinates

            # Check if the next position is within the board boundaries
            if -board_x <= next_x <= board_x and -board_y <= next_y <= board_y:
                x = next_x
                y = next_y
            else:
                # if the next step of the ant is outside of our board, the ant turns around 180 degrees
                if abs(next_x) > board_x - edge_turn_region or abs(next_y) > board_y - edge_turn_region:
                    # Turn around 180 degrees
                    self.directions[ant] += 180

                    direction_to_center = self.calculate_direction(np.array([next_x, next_y]), np.array([0, 0]))
                        # Move away from the border by repulsion_distance
                    repulsion_vector = direction_to_center * repulsion_distance
                    x += repulsion_vector[0]
                    y += repulsion_vector[1]
                   
            self.positions[ant] = (x, y)

            self.directions[ant] += np.random.uniform(-40, 40)    
        

    def perception(self, food, perception_radius):
        """this function contains the way, how the ants can find some food or the nest. It takes in the location of the food and the perception_radius.
        Every ant starts with none detected_targets. Every ant has a perception radius, in which they can "smell" food items.
        Every step and for each ant, the code checks, if there are any food_items in their radius.
        
        Input: Food Object, perception_radius
        
        Output: list of detected targets in the perception radius (detected_targets)"""

        detected_targets = []
        for ant_pos in self.positions:
            distances = np.linalg.norm(food.positions - ant_pos, axis=1)
            detected = any(distance <= perception_radius for distance in distances)
            detected_targets.append(detected)

        return detected_targets
        

    def approach_food(self, food, detected_food, approach_speed):
        """this function determines how to ants approch the food. The function takes in the location of the food, the detected_food from every ant and the approch_speed. The approch_speed determines how fast the ants move towards the food, if they have detected anything. This function is only in use, if an ant has detected a food_item. If an ant detects several food_items inside of their radius, then the distance is calculated and the ants move to the closest one. In the end, the position of the ant is updated towards the food_item"""
        for ant, detected in enumerate(detected_food):
            if detected and not self.carrying_food[ant]:
                nearest_food_index = np.argmin(np.linalg.norm(food.positions - self.positions[ant], axis=1))
                direction_to_food = food.positions[nearest_food_index] - self.positions[ant]
                norm_direction = np.linalg.norm(direction_to_food)
                if norm_direction > 0:  # Avoid division by zero
                    direction_to_food /= norm_direction

                    self.positions[ant] += direction_to_food * approach_speed

        return self.positions
    
    def return_home(self, ant):
        
         # if the ant is carrying food
        for ant in range(len(self.positions)):
                

            direction_to_home = self.calculate_direction(self.positions[ant], board.nest_pos)
            self.positions[ant] += direction_to_home * (approach_speed)

            # Check if the ant has reached home (you can modify this condition based on your needs)
            if np.linalg.norm(self.positions[ant] - board.nest_pos) < 0.5:
                # Ant has reached home, reset the flag to search for food again
                self.carrying_food[ant] = False
            
            
        return self.positions 


class Food:
    "this class determines the location of the food_items and deploys them"

    def __init__(self, num_food):
        self.positions = np.random.uniform(-board_x, board_x, size=(num_food, 2))
    def deploy_food(self):
        return self.positions


class Board:
    """the board class is for the visualisation of the board and for the simulation, which runs through every step and displays the current board."""

    def __init__(self, num_ants, num_food):
        self.ants = Ants(num_ants)
        self.food = Food(num_food)
        self.nest_pos = np.array([0,0])

    def visualize(self, detected_food, step):
        
            
        plt.scatter(
            self.ants.positions[:, 0], self.ants.positions[:, 1], marker="x", color="b"
        )  # creates Ants as blue "x"
        plt.scatter(
            self.food.positions[:, 0], self.food.positions[:, 1], marker="o", color="g"
        )  # creates food sources as green "o"

        for ant, detected in enumerate(detected_food):
            if detected:
                plt.plot(self.ants.positions[ant, 0], self.ants.positions[ant, 1], 'rx')

        plt.title(f'Step {step + 1}/{num_steps}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)
        plt.grid(True)

    def simulate(self, num_steps, perception_radius, approach_speed):
        plt.ion()
        

        for step in range(num_steps):
            self.ants.movement(perception_radius, approach_speed)
            detected_food = self.ants.perception(self.food, perception_radius)
            self.ants.positions = self.ants.approach_food(self.food, detected_food, approach_speed)

            self.visualize(detected_food, step)

            plt.pause(0.3)
            plt.clf()

        plt.ioff()
        plt.show()
        plt.close()


# Set the number of steps, ants, perception radius, and approach speed
num_steps = 30
num_ants = 1
num_food = 10
perception_radius = 2
approach_speed = 0.7

start_time = time.time()
board = Board(num_ants, num_food)
board.simulate(num_steps, perception_radius, approach_speed) # runs the code 
end_time = time.time()
duration = end_time - start_time
print(duration)

# bewegen sich immer nur zurück zum Nest wenn beide Essen haben und zurück gehen!