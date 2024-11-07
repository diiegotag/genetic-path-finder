import json


def load_graph_from_json(file_path):
    """
    Load graph data and positions from a JSON file.
    :param file_path: Path to the JSON file.
    :return: A tuple containing two elements:
             1. A dictionary representing the graph structure.
             2. A dictionary representing the positions of the nodes.
    """
    with open(file_path, 'r') as f:
        graph_data = json.load(f)

    graph = {node: [{"node": neighbor["node"], "weight": neighbor["weight"]} for neighbor in neighbors]
             for node, neighbors in graph_data.items() if node != "positions"}

    positions = graph_data.get("positions", {})

    return graph, positions


def save_graph_to_json(graph_data, positions, file_path):
    """
    Save graph data and positions to a JSON file.
    :param graph_data: Dictionary representing the graph structure.
    :param positions: Dictionary representing the positions of the nodes.
    :param file_path: Path where the JSON file will be saved.
    """

    data_to_save = graph_data.copy()
    data_to_save["positions"] = positions

    with open(file_path, 'w') as f:
        json.dump(data_to_save, f, indent=4)
