# Function to get all neighbors of a node
def get_neighbors(g, node):
    """
    Get the neighbors of a node in the graph.
    :param g: The graph (networkx.Graph).
    :param node: The node whose neighbors are to be returned.
    :return: List of neighbors of the node.
    """
    if node in g:
        return list(g.neighbors(node))
    return []


# Function to get all edges in the graph
def get_all_edges(g):
    """
    Get all edges of the graph with their weights.
    :param g: The graph (networkx.Graph).
    :return: List of tuples (node1, node2, weight).
    """
    return [(u, v, data['weight']) for u, v, data in g.edges(data=True)]


# Function to check if a node exists in the graph
def node_exists(g, node):
    """
    Check if a node exists in the graph.
    :param g: The graph (networkx.Graph).
    :param node: The node to check for existence.
    :return: True if the node exists, False otherwise.
    """
    return node in g


# Function to convert the graph to a dictionary format suitable for JSON export
def graph_to_dict(g):
    """
    Convert a networkx graph to a dictionary suitable for JSON storage.
    :param g: The graph (networkx.Graph).
    :return: A dictionary representation of the graph.
    """
    graph_dict = {}
    for node in g.nodes:
        neighbors = [(neighbor, g[node][neighbor]['weight']) for neighbor in g.neighbors(node)]
        graph_dict[node] = neighbors
    return graph_dict
