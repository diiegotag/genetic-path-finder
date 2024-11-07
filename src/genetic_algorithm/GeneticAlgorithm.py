import random
from src.graph.graph_manager import create_graph_from_data


def selection(population, fitnesses, tournament_size=3):
    """Tournament selection to choose parents for the next generation."""
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])[0]  # Select the individual with the highest fitness
        selected.append(winner)
    return selected


def crossover(parent1, parent2, graph, end_node):
    """Perform crossover between two parents and correct invalid paths."""
    # Find a common node if exists to perform crossover; otherwise, keep the first parent
    common_nodes = set(parent1).intersection(parent2)
    if common_nodes:
        crossover_point = random.choice(list(common_nodes))
        idx1, idx2 = parent1.index(crossover_point), parent2.index(crossover_point)

        # Generate the child and ensure it is a valid path by removing duplicates
        child = parent1[:idx1] + parent2[idx2:]
        child = list(dict.fromkeys(child))  # Remove duplicates while preserving order

        # Correct path to reach end_node if not included
        if child[-1] != end_node:
            child = correct_path_to_end(child, graph, end_node)
        return child
    return parent1


def correct_path_to_end(child, graph, end_node):
    """Ensure the child path connects to the end_node by adding valid nodes."""
    last_node = child[-1]
    while last_node != end_node:
        neighbors = [node for node in graph[last_node] if node not in child]
        if not neighbors:
            return None  # Return None if no valid path to end_node can be found
        next_node = random.choice(neighbors)
        child.append(next_node)
        last_node = next_node
    return child


def calculate_path_distance(graph, path):
    """Calculate the total distance of a path on the graph."""
    total_distance = 0
    for i in range(len(path) - 1):
        current_node, next_node = path[i], path[i + 1]
        if next_node not in graph[current_node]:
            return float('inf')  # Invalid path if no connection exists
        total_distance += graph[current_node][next_node]['weight']
    return total_distance


class GeneticAlgorithm:

    def __init__(self, graph, start_node, end_node, generations, population_size):
        self.graph = create_graph_from_data(graph)  # Create graph from provided data
        self.start_node = start_node
        self.end_node = end_node
        self.generations = generations
        self.population_size = population_size
        self.visited_nodes = set()

    def fitness(self, individual):
        """Calculate fitness based on path distance and node exploration."""
        if not self.is_valid_path(individual):
            return -float('inf')  # Penalize invalid paths directly

        total_distance = calculate_path_distance(self.graph, individual)
        if total_distance == float('inf'):
            return -float('inf')  # Penalize invalid paths

        # Adjust distance weight for stronger penalization of long paths
        distance_weight = 0.85  # Increased emphasis on short distance
        path_fitness = (1 / (1 + total_distance)) ** distance_weight

        # Reward correct end node
        if individual[-1] == self.end_node:
            fitness = path_fitness + 3.0  # Higher reward for reaching end_node
        else:
            fitness = path_fitness - total_distance  # Heavy penalty for non-terminal paths

        # Add a small reward for exploring new nodes
        unexplored_nodes = set(individual) - self.visited_nodes
        fitness += len(unexplored_nodes) * 0.1
        self.visited_nodes.update(unexplored_nodes)

        return fitness

    def is_valid_path(self, path):
        """Check if a given path is valid in the graph."""
        for i in range(len(path) - 1):
            if path[i + 1] not in self.graph[path[i]]:
                return False
        return True

    def create_initial_population(self):
        """Create the initial population with random paths."""
        population = []
        for _ in range(self.population_size):
            individual = [self.start_node]
            current_node = self.start_node
            while current_node != self.end_node:
                next_node = self.get_random_adjacent_node(current_node, individual)
                if next_node is None:
                    break  # If no valid next node, stop the path
                individual.append(next_node)
                current_node = next_node
            if self.is_valid_path(individual):  # Ensure only valid paths are added
                population.append(individual)
        return population

    def get_random_adjacent_node(self, node, current_path):
        """Get a random adjacent node that has not been visited in the current path."""
        adjacent_nodes = [neighbor for neighbor in self.graph[node] if neighbor not in current_path]
        if not adjacent_nodes:
            return None  # No unvisited adjacent nodes
        return random.choice(adjacent_nodes)

    def mutate(self, individual, mutation_rate=0.2):
        """Apply mutation to a path to introduce diversity."""
        for i in range(1, len(individual) - 1):  # Exclude start and end nodes
            if random.random() < mutation_rate:
                current_node = individual[i]
                neighbors = list(self.graph.neighbors(current_node))
                if neighbors:
                    # Replace with a random neighbor if possible
                    individual[i] = random.choice(neighbors)

        # Remove any duplicates that could create loops in the path
        individual = list(dict.fromkeys(individual))

        # Ensure path reaches the end node
        if individual[-1] != self.end_node:
            individual = correct_path_to_end(individual, self.graph, self.end_node)

        return individual if individual and self.is_valid_path(individual) else None  # Return None if invalid

    def visualize_population(self, population, fitnesses):
        """Visualize the population and their fitness scores."""
        print("Current Population and Fitnesses:")
        for i, (individual, fitness) in enumerate(zip(population, fitnesses)):
            print(f"Individual {i + 1}: Path = {individual} | Fitness = {fitness:.4f}")

    def run(self):
        """Run the genetic algorithm to find the best path from start to end node."""
        population = self.create_initial_population()
        for generation in range(self.generations):
            print(f"\nGeneration {generation + 1}:")
            fitnesses = [self.fitness(individual) for individual in population]

            # Visualize the population and their fitnesses
            self.visualize_population(population, fitnesses)

            # Selection: tournament selection
            selected_population = selection(population, fitnesses)

            # Crossover and mutation to create the next generation
            next_generation = []
            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(selected_population, 2)
                child = crossover(parent1, parent2, self.graph, self.end_node)
                child = self.mutate(child) if child else None  # Ensure mutation on valid paths
                if child and self.is_valid_path(child):
                    next_generation.append(child)

            population = next_generation

        # Return the best solution after all generations
        best_individual = max(population, key=self.fitness)
        best_distance = calculate_path_distance(self.graph, best_individual)
        return best_individual, best_distance
