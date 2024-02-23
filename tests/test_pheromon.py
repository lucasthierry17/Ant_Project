import numpy as np
import pytest
import pygame
from source.main import Pheromones
from source.main import Ants
pygame.init()
pygame.display.set_mode((350, 100), vsync=True) 




def test_update():
    pher=Pheromones((350,100))
    start=pher.img_array
    pher.update()
    result=pher.img_array
    assert result is not start #image gets updated


def test_reset():
    pher=Pheromones((350,100))
    start=pher.img_array.fill(11)
    pher.reset()
    result=pher.img_array
    assert result is not start #image gets Cleared




if __name__ == '__main__':
    test_update()
