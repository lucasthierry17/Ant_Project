"""Tests for the function inside the time_1.py file
"""

import numpy as np
from Version1 import Ants, Food


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
    num_ants = 5
    ants = Ants(num_ants)
    num_food = 5
    food = Food(num_food)

    # set up some values in order to check the function
    ants.positions = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
    food.positions = np.array([[0.5, 0.4], [1.3, 2.5], [3.3, 1.3], [5, 5.3], [8, 7]])

    # Set a known perception radius
    perception_radius = 1.0

    # Calls the
    perception_function = ants.perception(food, perception_radius)

    # set up the results
    expected_results = [True, True, True, False, False]
    assert (
        perception_function == expected_results
    )  # checking if the results from the function are equal to the expected results


def test_deploy_food():
    num_food = 3  # set the number of food sources
    food = Food(num_food)
    food_positions = food.deploy_food()  # runs the function

    # Check if the number of positions matches the expected number of food items
    assert len(food_positions) == num_food  # checking for the right number of food sources
    assert np.all(
        np.logical_and(food_positions >= -15, food_positions <= 15)
    )  # checking if positions are within our expected range
    # Check if the shape of the positions array is correct
    assert food_positions.shape == (num_food, 2)  # checking for shape
