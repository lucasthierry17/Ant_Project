import matplotlib.pyplot as plt
import numpy as np

def move_ants(num_ants, num_steps):
    for ant in range(num_ants):
        ant_position = [0, 0]
        ant_direction = np.random.randint(0, 360)

        x_values, y_values = [ant_position[0]], [ant_position[1]]

        for step in range(1, num_steps + 1):
            direction_x = np.random.uniform(-1, 1)
            ant_position[0] += direction_x
            direction_y = np.random.uniform(-1, 1)
            ant_position[1] += direction_y

            x_values.append(ant_position[0])
            y_values.append(ant_position[1])

        plt.plot(x_values, y_values, marker="x", label=f"Ant {ant + 1}")

    plt.title("Ant Movement")
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()

move_ants(2, 4)
