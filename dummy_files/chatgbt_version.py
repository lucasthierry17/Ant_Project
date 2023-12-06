import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from enum import Enum
from matplotlib.colors import ListedColormap


class Smell(Enum):
    NEST = 1
    FOOD = 2
    OBSTACLE = 3

class Ant:
    def __init__(self, position, has_food_smell=False):
        self.position = position
        self.has_food_smell = has_food_smell

def create_board(size):
    return np.zeros((size, size))

def add_nest(board, nest_position):
    board[nest_position] = Smell.NEST.value

def add_food(board, food_position):
    board[food_position] = Smell.FOOD.value

def add_obstacle(board, obstacle_position):
    board[obstacle_position] = Smell.OBSTACLE.value

def update_ant_smell(board, ant):
    ant_row, ant_col = ant.position
    ant.has_food_smell = board[ant_row, ant_col] == Smell.FOOD.value

def move_ant(board, ant):
    # Simple random movement for demonstration purposes
    ant_row, ant_col = ant.position
    direction = np.random.choice(['up', 'down', 'left', 'right'])
    
    if direction == 'up' and ant_row > 0 and board[ant_row - 1, ant_col] != Smell.OBSTACLE.value:
        ant_row -= 1
    elif direction == 'down' and ant_row < board.shape[0] - 1 and board[ant_row + 1, ant_col] != Smell.OBSTACLE.value:
        ant_row += 1
    elif direction == 'left' and ant_col > 0 and board[ant_row, ant_col - 1] != Smell.OBSTACLE.value:
        ant_col -= 1
    elif direction == 'right' and ant_col < board.shape[1] - 1 and board[ant_row, ant_col + 1] != Smell.OBSTACLE.value:
        ant_col += 1
    
    ant.position = (ant_row, ant_col)

def update_board(board, ants, food_position, obstacle_positions):
    board.fill(0)
    for ant in ants:
        if ant.has_food_smell:
            board[ant.position] = Smell.FOOD.value
        else:
            board[ant.position] = Smell.NEST.value

    for obstacle_position in obstacle_positions:
        board[obstacle_position] = Smell.OBSTACLE.value

    # Add the apple (food item) to the board
    add_food(board, food_position)

def simulate_ants(num_ants, nest_position, food_position, obstacle_positions, board_size, max_steps):
    board = create_board(board_size)
    add_nest(board, nest_position)

    ants = [Ant(nest_position) for _ in range(num_ants)]

    for step in range(max_steps):
        for ant in ants:
            update_ant_smell(board, ant)
            move_ant(board, ant)

            if ant.position == food_position and ant.has_food_smell:
                # Ant found the apple, simulate carrying a tiny part of it back to the nest
                ant.has_food_smell = False

        update_board(board, ants, food_position, obstacle_positions)

        yield board

def visualize_simulation(board_size, nest_position, food_position, obstacle_positions, max_steps):
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        ax.imshow(frame, cmap=get_custom_cmap(), vmin=0, vmax=3, origin='upper')

    ani = animation.FuncAnimation(fig, update, frames=simulate_ants(20, nest_position, food_position, obstacle_positions, board_size, max_steps), repeat=False)
    plt.show()

def get_custom_cmap():
    colors = ['#8B4513', 'white', 'red', 'gray']
    return ListedColormap(colors)

# Example usage
board_size = 40
nest_position = (board_size // 2, board_size // 2)
food_position = (1, 8)
obstacle_positions = [(5, 5), (7, 12), (12, 8), (15, 15)]
max_steps = 100

visualize_simulation(board_size, nest_position, food_position, obstacle_positions, max_steps)


