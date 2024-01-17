import time
import numpy as np
import matplotlib.pyplot as plt

class Ants():
    """This class contains the functions movement, perception and approach_food. """
    def __init__(self, num_ants):
        self.positions = np.zeros((num_ants, 2),dtype=float)
        self.directions = np.random.uniform(0, 360, size=num_ants)
        self.carrying_food = np.zeros(num_ants, dtype=bool)

    def calculate_direction(self, start, target):
        direction_vector = target - start
        direction = direction_vector / np.linalg.norm(direction_vector)
        return direction
    
    def movement(self, edge_turn_region=50):
        """this function is for the steps of the ants. First, the ants receive a random direction (self.directions). After the first step, they have a angle of view (right now -40 to 40 degrees). They walk randomly in this site of view. For each step they get a direction (-40 to 40 degrees) and take a step in that direction. If they enter the edge_region, they turn around and take the next step in the opposite direction
        Input: perception_radius, approach_speed, edge_turn_region
        """

        cos_directions = np.cos(np.radians(self.directions)) # chooses the direction on the x axis
        sin_directions = np.sin(np.radians(self.directions)) # same on the y axis

        for ant in range(len(self.positions)):      
            x, y = self.positions[ant]
            next_x = x + cos_directions[ant] # computes the next x coordinates
            next_y = y + sin_directions[ant] # computes the next y coordinates

           
            # Check if the next position is within the board boundaries
            if -20 <= next_x <= 20 and -20 <= next_y <= 20:
                x = next_x
                y = next_y
            else:
                # Ant is approaching the edge
                if abs(next_x) > board_x - edge_turn_region or abs(next_y) > board_y - edge_turn_region:
                    # Turn around 180 degrees
                    self.directions[ant] += 180
                else:
                    # Turn slightly around
                    self.directions[ant] += np.random.uniform(-20, 20)

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
            distances = np.linalg.norm(food.positions - ant_pos, axis=1) # calculate the distance for each ant to the food positions
            detected = any(distance <= perception_radius for distance in distances) # mark as detected if the distance to any food position is in the perception radius
            detected_targets.append(detected) # save detected targets in a list and return it
        return detected_targets
        

    def approach_food(self, food, detected_food, approach_speed):
        """this function determines how the ants approch the food. The function takes in the location of the food, the detected_food from every ant and the approch_speed. 
        The approch_speed determines how fast the ants move towards the food, if they have detected anything. This function is only in use, if an ant has detected a food_item. 
        If an ant detects several food_items inside of their radius, then the distance is calculated and the ants move to the closest one.
        In the end, the position of the ant is updated towards the food_item
        
        Input: Food Object, detected_food, approach_speed
        
        Output: returns the new positions of the ants (self.positions)"""
        
        # iterates over the elements of detected_food and their indices. Detected is a boolean for each ant 
        for ant, detected in enumerate(detected_food):
            # only approach food when they detected it and aren't already carrying food
            if detected and not self.carrying_food[ant]:
                nearest_food_index = np.argmin(np.linalg.norm(food.positions - self.positions[ant], axis=1)) # calculate the nearest food position
                direction_to_food = self.calculate_direction(self.positions[ant],food.positions[nearest_food_index]) # get the direction of the nearest food position
                self.positions[ant] += direction_to_food * approach_speed # adjust the position so they take a step towards the food position

                # when they arrived at the food position the status that they're carrying food turns true
                if np.linalg.norm(self.positions[ant] - food.positions[nearest_food_index]) < 0.5:
                    self.carrying_food[ant] = True
        return self.positions
    
    def return_home(self, ant):
        """This is a function to direct the ants back to the nest. It only activates if the status that they're carrying food is true.
        It calculates the direction back to the nest and adjusts the position towards that direction.
        When they reached the nest the status that they're carrying food turns false again
        
        Input: Ant Object
        
        Output: new positions of the ants"""

        # calculate the direction to the nest and take a step towards that direction
        direction_to_home = self.calculate_direction(self.positions[ant], board.nest_pos)
        self.positions[ant] += direction_to_home * (approach_speed)

        # Check if the ant has reached home
        if np.linalg.norm(self.positions[ant] - board.nest_pos) < 0.5:
            # Ant has reached home, reset the status to false
            self.carrying_food[ant] = False
        return self.positions 

class Food:
    "this class determines the location of the food_items and deploys them"
    def __init__(self, num_food):
        self.num_food = num_food
        self.positions = np.random.uniform(-15, 15, size=(num_food, 2))

        # self.radius = radius
        # self.center = None

        # # Generate random angles for polar coordinates
        # angles = np.linspace(0, 2 * np.pi, self.num_food)

        # radii = np.sqrt(np.random.uniform(0, 1, self.num_food)) * self.radius

        # # Convert polar coordinates to Cartesian coordinates
        # x = radii * np.cos(angles)
        # y = radii * np.sin(angles)

        # # Randomly choose the center of the filled circle
        # self.center = np.random.uniform(-18, 18, size=(1, 2))
        # # Store the positions
        # self.positions = np.column_stack((x, y)) + self.center


    def deploy_food(self):
        return self.positions

class Board:
    """the board class is for the visualisation of the board and for the simulation. """
    def __init__(self, num_ants, num_food):
        self.ants = Ants(num_ants)
        self.food = Food(num_food)
        self.nest_pos = np.array([0,0])

    def visualize(self, detected_food, step):
        plt.scatter(self.ants.positions[:, 0], self.ants.positions[:, 1], marker='x', color='b') # creates Ants as blue "x"
        plt.scatter(self.food.positions[:, 0], self.food.positions[:, 1], marker='o', color='g') # creates food sources as green "o"
        plt.scatter(self.nest_pos[0], self.nest_pos[1], marker='x', color='red')

        for ant, detected in enumerate(detected_food):
            if detected:
                plt.plot(self.ants.positions[ant, 0], self.ants.positions[ant, 1], 'rx') # marks ants that detect food red
            if self.ants.carrying_food[ant]:
                plt.plot(self.ants.positions[ant, 0], self.ants.positions[ant, 1], 'yx') # marks ants that are carrying food yellow

        plt.title(f'Step {step + 1}/{num_steps}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim(-board_x, board_x)
        plt.ylim(-board_y, board_y)
        plt.grid(True)

    def simulate(self, num_steps, perception_radius, approach_speed):
        plt.ion()
        fig, ax = plt.subplots()

        for step in range(num_steps):
            detected_food = self.ants.perception(self.food, perception_radius)
            for ant in range(len(self.ants.positions)):  
                print(ant)
                if self.ants.carrying_food[ant]:
                    print("Food")
                    self.ants.return_home(ant)

                else:
                    print("Movement")
                    
                    self.ants.approach_food(self.food, detected_food, approach_speed)
                    self.ants.movement()
            self.visualize(detected_food, step)

            plt.pause(0.4)
            plt.clf()

        plt.ioff()
        plt.show()
        plt.close()

# Set the number of steps, ants, perception radius, and approach speed
num_steps = 100
num_ants = 2
num_food = 30
radius = 3
perception_radius = 2
approach_speed = 0.8

board_x = 20
board_y = 20
start_time = time.time()
board = Board(num_ants, num_food)
board.simulate(num_steps, perception_radius, approach_speed) # runs the code 
end_time = time.time()
duration = end_time - start_time
print(duration)

# bewegen sich immer nur zurück zum Nest wenn beide Essen haben und zurück gehen!