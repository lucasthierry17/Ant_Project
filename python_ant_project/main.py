""" libraries """
import numpy as np
import random
import matplotlib.pyplot as plt
import time
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Circle
"""           """

class Board:
    """
    board infos :
        Position,
        Position Colony,
        etc
    """
    MAP_SIZE = 128
    NEST_SIZE = 3

    NEST_NUMBER = 9
    FOOD_NUMBER = 5
    PHEROMONE_HOME_NUMBER=1
    PHEROMONE_FOOD_NUMBER=2
    def __init__(self):
        self.world = np.zeros((Board.MAP_SIZE, Board.MAP_SIZE//2))
        self.amount_of_static_food_source = 5
        self.has_food = False

    def create_world(self):
        Board.create_nest(self)
        Board.create_static_food(self)
        pass


    def create_nest(self):
        nest_location = Board.get_nest_location(self)
        self.world[nest_location[0],nest_location[1]] = Board.NEST_NUMBER
        pass

    def get_nest_location(self):
        """Random nest spawn
        first_position = 0  # Rename Variable
        nest_position_x = random.randint(first_position, Board.MAP_SIZE)
        nest_position_y = random.randint(first_position, Board.MAP_SIZE)
        """
        compensate_indexing = 1
        nest_location = 10
        nest_position_x = nest_location - compensate_indexing
        nest_position_y = nest_location - compensate_indexing
        return (nest_position_x, nest_position_y)

    """
        smell distance,
        can_be_smelled(),
        Spawn food with decay,
        Static and Decaying food,
    """
    def create_static_food(self):
        for number in range(self.amount_of_static_food_source):
            amount, location_x, location_y = Board.static_food_spawn(self)
            half_the_amount = int(amount//2)
            print(amount, location_x, location_y)
            for piece in range(amount):
                if piece <= half_the_amount:
                    self.world[location_x+piece,location_y] = Board.FOOD_NUMBER 
                elif piece >= half_the_amount:
                    self.world[location_x,location_y+piece] = Board.FOOD_NUMBER

        pass

    def static_food_spawn(self):
        compensate_indexing = 1
        
        amount_of_food = random.randint(4, 20)
        location_food_x = random.randint(20, Board.MAP_SIZE - 20)
        location_food_y = random.randint(20, Board.MAP_SIZE//2 - 20) 
        return amount_of_food, location_food_x - compensate_indexing , location_food_y - compensate_indexing

    def dynamic_food_spawn(self):
        decay_time_in_seconds = 5
        pass
    def place_pheromone(self, position):
        Food_PHEROMONE = 4
        Normal_PHEROMONE = 5
        if self.has_food is True:
           Board.world[position[0]-1][position[1]-1] == Food_PHEROMONE
        if self.has_food is False:
           Board.world[position[0]-1][position[1]-1] == Normal_PHEROMONE  
        pass


class Ants:
    """
    Ant stuff :
        Next move,
        Pheromone,
        Ant Antributes
    """
    def __init__(self, ant_speed, ant_has_food_bool):
        self.ant_travel_speed = 1
        self.ant_has_food = False

    """
    GUI Matplotlib
    """
def view(array, circle_radius,nest_position):
    my_array = array

    # Get the indices and values from the array
    indices = np.indices(my_array.shape)
    x_values = indices[0].flatten()
    y_values = indices[1].flatten()
    data_values = my_array.flatten()
    colors_custom = [(1, 1, 1), (1, 0, 0), (1, 1, 0), (0, 0, 0)]  # Example: black to red to yellow to white
    custom_cmap = LinearSegmentedColormap.from_list('custom_colormap', colors_custom, N=256)

    # Normalize your data to the range [0, 1]
    norm = Normalize(vmin=data_values.min(), vmax=data_values.max())
    normalized_data = norm(data_values)

    # Create a scatter plot using your custom colormap
    plt.scatter(x_values, y_values, c=normalized_data, cmap=custom_cmap)
    circle_radius = 5
    circle = Circle(nest_position, circle_radius, edgecolor='brown', facecolor='brown', linewidth=2)
    plt.gca().add_patch(circle)
    # Show the plot
    plt.show()




   

def main(amount_ants=5, amaount_static_food_source=3):
    simulation = Board()
    simulation.create_world()
    np.savetxt('output.txt', simulation.world, fmt='%d', delimiter='')
    view(simulation.world,simulation.NEST_SIZE, simulation.get_nest_location())
    """
        A Start Simulation function
    """
    """
    while True:
        for ant in range(amount_ants):
    """
if __name__ == '__main__':
    """START AREA"""
    main()



