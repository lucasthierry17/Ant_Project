import numpy as np
import pytest
import pygame
from source.main import Pheromones
from source.main import Ants
pygame.init()
pygame.display.set_mode((1350, 800), ) 


def test_calculate_distance():
    """Testing calculate directions in Ants"""
    self_replacement = None
    expected_result=[4.123105625617661, 300.66592756745814, 61.18823416311342, 839.00238378684, 433.04041381838715, 67.02984409947557]
    start=[0,0]
    target=[[4,1],[300,20],[60,12],[839,2],[432,30],[2,67]]
    for run, entry in enumerate(target):
        result=Ants.calculate_distance(self_replacement,start, entry)
        assert result == expected_result[run] # Calculates the Distance between two spots


def test_scaled_position(): ## Muss eingefügt werden
    expected_result=[(40, 24), (46, 64), (24, 4), (11, 2), (56, 18)]
    x=[200,230,123,55,282]
    y=[120,321,21,10,90]
    for run, entry in enumerate(x):
        result = Ants.scaled_pos(None, entry, y[run])
        assert result == expected_result[run] # Positions get scaled by PRATIO

def test_update():
    phero=Pheromones((1350,800))
    ant=Ants((1350//3.5,800//2), phero,1)    
    start_value_desireDir=ant.desire_dir
    start_value_x=ant.x_pos
    start_value_y=ant.y_pos
    ant.update()
    result_value_desireDir=ant.desire_dir
    result_value_x=ant.x_pos
    result_value_y=ant.y_pos
    assert result_value_desireDir != start_value_desireDir # Succesfuly updated desireDir
    assert result_value_x != start_value_x# Succesfuly updated x
    assert result_value_y != start_value_y # Succesfuly updated y 

def test_random_walk():
    phero=Pheromones((1350,800))
    ant=Ants((1350//3.5,800//2), phero,1)    
    start_value_desireDir=ant.desire_dir
    ant.random_walk()
    result_value_desireDir=ant.desire_dir
    assert result_value_desireDir != start_value_desireDir # Succesfuly updated desireDir







if __name__ == '__main__':
    test_update()
    test_calculate_distance()
    test_scaled_position()
    test_random_walk()
