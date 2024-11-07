import unittest
import networkx as nx
from src.graph.graph_utils import get_neighbors, get_all_edges, node_exists, graph_to_dict


class TestGraphUtils(unittest.TestCase):

    def setUp(self):
        """
        Setup method to prepare the test environment.
        Creates a sample graph for testing.
        """
        # Create a simple sample graph
        self.graph = nx.Graph()
        self.graph.add_edge("Tijuana", "Rosarito", weight=20)
        self.graph.add_edge("Tijuana", "Tecate", weight=52)
        self.graph.add_edge("Rosarito", "Ensenada", weight=85)
        self.graph.add_edge("Tecate", "Mexicali", weight=135)

    def test_get_neighbors(self):
        """
        Test that `get_neighbors` correctly retrieves neighbors of a node.
        """
        neighbors = get_neighbors(self.graph, "Tijuana")

        # Check if neighbors of Tijuana are Rosarito and Tecate
        self.assertIn("Rosarito", neighbors)
        self.assertIn("Tecate", neighbors)

        # Test for a node with no neighbors
        neighbors = get_neighbors(self.graph, "Ensenada")
        self.assertEqual(neighbors, ["Rosarito"])

        # Test for a non-existing node (should return empty list)
        neighbors = get_neighbors(self.graph, "San Felipe")
        self.assertEqual(neighbors, [])

    def test_get_all_edges(self):
        """
        Test that `get_all_edges` returns all edges with weights.
        """
        edges = get_all_edges(self.graph)

        # Check the length of edges (should be 4 in this case)
        self.assertEqual(len(edges), 4)

        # Verify that each edge has the correct weight
        edge = ("Tijuana", "Rosarito", 20)
        self.assertIn(edge, edges)

        edge = ("Tecate", "Mexicali", 135)
        self.assertIn(edge, edges)

    def test_node_exists(self):
        """
        Test that `node_exists` correctly checks for node existence in the graph.
        """
        self.assertTrue(node_exists(self.graph, "Tijuana"))
        self.assertTrue(node_exists(self.graph, "Rosarito"))

        # Test for a node that does not exist
        self.assertFalse(node_exists(self.graph, "San Felipe"))

    def test_graph_to_dict(self):
        """
        Test that `graph_to_dict` converts the graph to the correct dictionary format.
        """
        graph_dict = graph_to_dict(self.graph)

        # Check that the graph dictionary has the correct structure
        self.assertIn("Tijuana", graph_dict)
        self.assertIn("Rosarito", graph_dict)

        # Ensure the edges and weights are correctly converted
        self.assertIn(("Rosarito", 20), graph_dict["Tijuana"])
        self.assertIn(("Tecate", 52), graph_dict["Tijuana"])

        # Test for a node with no neighbors
        self.assertEqual(graph_dict["Ensenada"], [("Rosarito", 85)])

    def tearDown(self):
        """
        Cleanup method to remove the test files after tests are done.
        """
        # No files to remove in this test case
        pass


if __name__ == '__main__':
    unittest.main()
