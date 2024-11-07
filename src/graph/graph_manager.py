import networkx as nx
from src.data.json_loader import load_graph_from_json


# Function to create a graph from a dictionary or list of edges
def create_graph_from_data(data):
    """
    Create a graph from a dictionary or list of edges. The data format should be a list of tuples or a dictionary of
    edges.
    :param data: List or dict representing the graph.
    :return: networkx.Graph object.
    """
    g = nx.Graph()

    if isinstance(data, list):  # A list of edges (tuples)
        g.add_edges_from(data)
    elif isinstance(data, dict):  # A dictionary with nodes as keys and edges as values
        for node, edges in data.items():
            for neighbor, weight in edges:
                for edge in edges:
                    g.add_edge(node, edge["node"], weight=edge["weight"])

    return g


# Function to load a graph from a JSON file
def load_graph_from_json_file(file_path):
    """
    Load a graph from a JSON file.
    :param file_path: Path to the JSON file.
    :return: networkx.Graph object.
    """
    graph_data = load_graph_from_json(file_path)
    return create_graph_from_data(graph_data)
