"""Tests for the function inside the time_1.py file
"""
import pytest
from Version1 import Ants
from Version1 import Food
from Version1 import Board
import numpy as np


def test_movement():
    num_ants = 10  # sets up the number of ants for this test function
    ants = Ants(num_ants)  # creates an instance of the Ant class
    perception_radius = 3
    approach_speed = 0.5
    ants.movement(
        perception_radius, approach_speed
    )  # calls the movement function with the parameters perception_radius and approach_speed

    assert ants.positions.shape == (num_ants, 2)


def test_perception():
    # creates an instance of the class Ant
    num_ants = 10
    ants = Ants(num_ants)
    num_food = 5
    food = Food(num_food)

    # set up some values in order to check the function
    ants.positions = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]])
    food.positions = np.array([[0.5, 0.4], [1.3, 2.5], [3.3, 1.3], [5, 5.3], [8, 7]])

    # Set a known perception radius
    perception_radius = 1.0

    # Calls the
    perception_function = ants.perception(food, perception_radius)

    # set up the results
    expected_results = [True, True, True, False, False, True, False, True, True, False]
    assert (
        perception_function == expected_results
    )  # checking if the results from the function are equal to the expected results


def test_approach_food():
    # Create an instance of Ants and Food
    num_ants = 5
    ants = Ants(num_ants)
    num_food = 3
    food = Food(num_food)

    # Set positions of ants and food to known values
    ants.positions = np.array([[0.5, 0.5], [1, 1], [2.2, 2.5], [3, 3], [4.1, 4.7]])
    food.positions = np.array([[0, 0], [2, 2], [4, 4]])

    # only the first, third and fifth ant are detecting food
    detected_food = [True, False, True, False, True]

    # Set a known approach speed
    approach_speed = 0.5

    # Call the approach_food method
    updated_positions = ants.approach_food(food, detected_food, approach_speed)

    # Verify the results
    assert food.positions - updated_positions < food.positions - ants.positions
