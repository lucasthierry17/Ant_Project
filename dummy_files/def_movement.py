import numpy as np
import matplotlib.pyplot as plt

def movement(num_steps, num_ants):
    """this function is a first simple implementation for the movements of the ants. It takes the number of steps and the number of ants. The ants start at the position (0, 0) and each get a starting direction.
    Then they walk randomly inside their side of view, which is (-40, 40) degrees."""
    plt.ion()  # Turn on interactive mode for continuous visualization
    fig, ax = plt.subplots()

    ant_positions = np.zeros((num_ants, 2))  # Starting positions for each ant at (0, 0)
    ant_directions = np.random.uniform(0, 360, size=num_ants)

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

        # Plots the position of the ants after every step 
        plt.scatter(ant_positions[:, 0], ant_positions[:, 1], marker='x', color='b')

        plt.title(f'Step {step + 1}/{num_steps}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)
        plt.grid(True)
        plt.pause(0.1)  # Adds a pause of one second between the plots

        # Clear the previous plot
        plt.clf()

    plt.ioff()  # Turn off interactive mode at the end
    plt.show()

# Set the number of steps and ants
num_steps = 30
num_ants = 100

movement(num_steps, num_ants)



