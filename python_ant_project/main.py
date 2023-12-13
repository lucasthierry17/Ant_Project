import numpy as np
import random


class World():
    """
    board infos :
        Position,
        Position Colony,
        etc
    """
    MAP_SIZE = 128
    NEST_NUMBER = 9

    def __init__(self):
        pass

    def create_world():
        world = World.create_map()
        nest_position = World.create_nest()
        world[nest_position[0]][nest_position[1]] = World.NEST_NUMBER
        return world

    def create_map():
        return np.zeros((World.MAP_SIZE, World.MAP_SIZE))

    def create_nest():
        first_position = 0  # Rename Variable
        nest_position_x = random.randint(first_position, World.MAP_SIZE)
        nest_position_y = random.randint(first_position, World.MAP_SIZE)
        return (nest_position_x, nest_position_y)


class Ants():
    """
    Ant stuff :
        Next move,
        Pheromone,
        Ant Antributes
    """


class Food():
    """
    Food atributes :
        smell distance,
        can_be_smelled(),
        Spawn food with decay,
        Static and Decaying food,
    """


class View():
    """
    GUI
    """


def Main():

    pass
