import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

matplotlib.use('Qt5Agg')


def visualize_graph(graph, positions=None):
    """
    Visualize the graph using matplotlib and networkx.
    :param positions:
    :param graph: The graph represented as a dictionary (dict).
    """
    # Convert the dictionary to a networkx graph
    g = nx.Graph()

    # Add nodes and edges
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            g.add_edge(node, neighbor['node'], weight=neighbor['weight'])

    # If no custom node positions are provided, use spring_layout
    if positions is None:
        positions = nx.spring_layout(g)  # Positioning of nodes

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(g, pos=positions, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold',
            edge_color='gray')
    plt.title("Graph visualization")
    plt.show()


def visualize_path(graph, path, positions=None):
    """
    Visualize a specific path within the graph.
    :param positions:
    :param graph: The graph represented as a dictionary (dict).
    :param path: List of nodes representing the path.
    """
    # Convert the dictionary to a networkx graph
    g = nx.Graph()

    # Add nodes and edges
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            g.add_edge(node, neighbor['node'], weight=neighbor['weight'])

    # If no custom node positions are provided, use spring_layout
    if positions is None:
        positions = nx.spring_layout(g)  # Positioning of nodes

    # Draw the full graph
    plt.figure(figsize=(8, 6))
    nx.draw(g, positions, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold',
            edge_color='gray')

    # Highlight the path
    edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(g, positions, edgelist=edges_in_path, edge_color='red', width=2)

    # Draw edge labels for the distances
    edge_labels = {}
    for (node1, node2) in g.edges():
        weight = g[node1][node2]['weight']
        edge_labels[(node1, node2)] = f'{weight} km'  # Format the weight as km

    nx.draw_networkx_edge_labels(g, positions, edge_labels=edge_labels, font_size=8)

    plt.title(f"Path Visualization: {path}")
    plt.show()
