import numpy as np
import matplotlib.pyplot as plt

def perception(ant_positions, target_positions, perception_radius):
    """
    Simple perception function for ants to detect nearby targets.
    """
    detected_targets = []
    for ant_pos in ant_positions:
        # Calculate distance from the ant to each target
        distances = np.linalg.norm(target_positions - ant_pos, axis=1)
        
        # Check if any target is within the perception radius
        detected = any(distance <= perception_radius for distance in distances)
        # append the targets that are in the perception radius
        detected_targets.append(detected)
    
    return detected_targets

def approach_food(ant_positions, food_positions, detected_food, approach_speed):
    """
    Approach detected food sources.
    Calculates the nearest food position that is in the perception radius. Then instructs the ants to approach that food spot.
    """
    for ant, detected in enumerate(detected_food):
        # if food spot was detected by the perception function
        if detected:
            # Move ant towards the nearest food
            nearest_food_index = np.argmin(np.linalg.norm(food_positions - ant_positions[ant], axis=1))
            direction_to_food = food_positions[nearest_food_index] - ant_positions[ant]
            direction_to_food /= np.linalg.norm(direction_to_food)  # Normalize to unit vector
            # updates the position of the ant
            ant_positions[ant] += direction_to_food * approach_speed

    return ant_positions

def movement(num_steps, num_ants, perception_radius, approach_speed):
    """this function is a first simple implementation for the movements of the ants. It takes the number of steps and the number of ants. The ants start at the position (0, 0) and each get a starting direction.
    Then they walk randomly inside their side of view, which is (-40, 40) degrees."""
    plt.ion() # Turn on interactive mode for continuous visualization
    fig, ax = plt.subplots()

    ant_positions = np.zeros((num_ants, 2))  # Starting positions for each ant at (0, 0)
    ant_directions = np.random.uniform(0, 360, size=num_ants)

    food_positions = np.random.uniform(-15, 15, size=(5, 2))  # 5 random food positions

    for step in range(num_steps):
        for ant in range(num_ants):
            # Update ant position based on the current direction
            x, y = ant_positions[ant]
            x += np.cos(np.radians(ant_directions[ant]))
            y += np.sin(np.radians(ant_directions[ant]))

            # set a limit for the x and y axis, so that the ants cannot go outside the baord
            x = max(-20, min(x, 20))
            y = max(-20, min(y, 20))

            ant_positions[ant] = (x, y)

            # Update ant direction for the next step
            if step > 0:
                ant_directions[ant] += np.random.uniform(-40, 40)

        # Perception of nearby food spots
        detected_food = perception(ant_positions, food_positions, perception_radius)

        # Approach nearest food spot
        ant_positions = approach_food(ant_positions, food_positions, detected_food, approach_speed)

        # Visualization
        plt.scatter(ant_positions[:, 0], ant_positions[:, 1], marker='x', color='b')
        plt.scatter(food_positions[:, 0], food_positions[:, 1], marker='o', color='g')

        # marks the ants that detect a food spot red
        for ant, detected in enumerate(detected_food):
            if detected:
                plt.plot(ant_positions[ant, 0], ant_positions[ant, 1], 'rx')  # Mark ants detecting food

        plt.title(f'Step {step + 1}/{num_steps}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)
        plt.grid(True)
        plt.pause(0.4)
        plt.clf()

    plt.ioff()
    plt.show()

# Set the number of steps, ants, perception radius, and approach speed
num_steps = 60
num_ants = 30
perception_radius = 3
approach_speed = 0.7

movement(num_steps, num_ants, perception_radius, approach_speed)
