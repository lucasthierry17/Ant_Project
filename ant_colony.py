import numpy as np

class Antcolony:
    def __init__(self, pheromones, ant_positions, alpha=1, beta=1):
        self.pheromones = pheromones
        self.cost_matrix = None
        self.pheromone_matrix = None
        self.ant_positions = ant_positions
        self.num_nodes = len(ant_positions)
        self.alpha = alpha
        self.beta = beta
    
    def create_paths(self, iterations=15):
        cost_matrix = np.zeros((self.num_nodes, self.num_nodes))
        pheromone_matrix = np.zeros((self.num_nodes, self.num_nodes))

        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                distance = np.linalg.norm(self.ant_positions[i] - self.ant_positions[j])
                pheromone = (self.pheromones[j % len(self.pheromones)] - self.pheromones[i % len(self.pheromones)]) / 255
                cost_matrix[i, j] = distance
                cost_matrix[j, i] = distance
                pheromone_matrix[i, j] = pheromone
                pheromone_matrix[j, i] = pheromone

        self.cost_matrix = cost_matrix
        self.pheromone_matrix = pheromone_matrix

        best_path = None
        best_path_cost = float('inf')

        for _ in range(iterations):
            paths = []
            path_costs = []

            for ant_position in self.ant_positions:
                path, path_cost = self.build_path(ant_position, self.alpha, self.beta)
                paths.append(path)
                path_costs.append(path_cost)

                if path_cost < best_path_cost:
                    best_path_cost = path_cost
                    best_path = path

        return best_path

    def build_path(self, start_position, alpha, beta):
        current_node_idx = np.where((self.ant_positions == start_position).all(axis=1))[0][0]
        current_node = current_node_idx
        path = [current_node]
        path_cost = 0

        while len(path) < self.num_nodes:
            allowed_nodes = [node for node in range(self.num_nodes) if node not in path]
            allowed_indices = [node_idx for node_idx in allowed_nodes]
            probabilities = self.calculate_probabilities(current_node, allowed_indices, alpha, beta)

            # Roulette wheel selection
            selected_index = np.where(np.cumsum(probabilities) >= np.random.rand())[0][0]
            next_node_idx = allowed_indices[selected_index]
            next_node = next_node_idx

            path_cost += self.cost_matrix[current_node, next_node]

            path.append(next_node)
            current_node = next_node

        return path, path_cost

    def calculate_probabilities(self, current_node, allowed_indices, alpha=1, beta=1):
        pheromones = self.pheromone_matrix[current_node, allowed_indices]
        costs = self.cost_matrix[current_node, allowed_indices]

        visibility = 1 / costs
        total = np.sum((pheromones ** alpha) * (visibility ** beta))

        if total <= 0:
            probabilities = np.ones(len(allowed_indices)) / len(allowed_indices)
        else:
            probabilities = ((pheromones ** alpha) * (visibility ** beta)) / total
            probabilities[probabilities < 0] = 0
        #print(probabilities)
        return probabilities

if __name__ == '__main__':
    ant_positions = np.array([
        [279.43858888, 452.84353191],
        [269.91116778, 144.05058484],
        [604.84087488, 380.88308894],
        [274.29275079, 60.33058914],
        [299.37637418, 349.34068779],
        [605.0443384, 522.95035372],
        [481.939603, 71.71030511],
        [232.28976853, 207.38550046],
        [455.50462301, 206.4518115],
        [81.7378216, 194.86856145],
        [320.88502957, 206.80374892],
        [769.56476442, 106.80589675],
        [332.53759734, 502.78882809],
        [631.14786648, 436.31073266],
        [704.15601956, 328.81956771],
        [450.0, 300.0]
    ])

    pheromones = np.array([120, 120, 120, 120, 120, 240, 0, 0, 0, 120, 0, 0, 0, 0, 255])
    aoc = Antcolony(pheromones=pheromones, ant_positions=ant_positions)
    trail = aoc.create_paths()
    print(trail)
