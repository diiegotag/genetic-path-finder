import sys

from src.data.json_loader import load_graph_from_json
from src.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from src.visualization.visualization import visualize_path


def main(graph_file: str, start_node: str, end_node: str, generations: int = 100, population_size: int = 50):
    """
    Run the genetic algorithm to find an optimal path between two nodes in a graph.

    Args:
        graph_file (str): Path to the JSON file containing the graph definition.
        start_node (str): Name of the starting node.
        end_node (str): Name of the destination node.
        generations (int, optional): Number of generations to run the algorithm. Default is 100.
        population_size (int, optional): Size of the population. Default is 50.
    """

    # Step 1: Load the graph from JSON file
    graph, positions = load_graph_from_json(graph_file)
    if not graph:
        print(f"Error: Could not load the graph from {graph_file}")
        return

    # Step 2: Initialize the genetic algorithm
    ga = GeneticAlgorithm(graph=graph, start_node=start_node, end_node=end_node,
                          generations=generations, population_size=population_size)

    # Step 3: Run the genetic algorithm to find the best path
    best_path, best_distance = ga.run()
    print(f"Best path found: {best_path} with distance {best_distance}")

    # Step 4: Visualize the graph and the optimal path
    visualize_path(graph, best_path, positions)


if __name__ == "__main__":
    # Usage: python run_algorithm.py graph_file.json start_node end_node
    if len(sys.argv) < 4:
        print("Usage: python run_algorithm.py <graph_file> <start_node> <end_node> [generations] [population_size]")
    else:
        graph_file = sys.argv[1]
        start_node = sys.argv[2]
        end_node = sys.argv[3]
        generations = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        population_size = int(sys.argv[5]) if len(sys.argv) > 5 else 50
        main(graph_file, start_node, end_node, generations, population_size)
