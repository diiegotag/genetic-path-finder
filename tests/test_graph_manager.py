import unittest
import networkx as nx
from src.graph.graph_manager import create_graph_from_data, load_graph_from_json_file
import os
import json


class TestGraphManager(unittest.TestCase):

    def setUp(self):
        """
        Setup method to prepare the test environment.
        Creates a sample graph JSON file for testing.
        """
        # Sample graph data for testing
        self.sample_graph = {
            "Tijuana": [
                {"node": "Rosarito", "weight": 20},
                {"node": "Tecate", "weight": 52}
            ],
            "Rosarito": [
                {"node": "Tijuana", "weight": 20},
                {"node": "Ensenada", "weight": 85}
            ]
        }

        self.test_file = 'test_graph.json'
        # Save the sample graph data to a JSON file
        with open(self.test_file, 'w') as f:
            json.dump(self.sample_graph, f, indent=4)

    def test_create_graph_from_data_dict(self):
        """
        Test that `create_graph_from_data` creates the correct graph from a dictionary.
        """
        # Create graph from sample data
        graph = create_graph_from_data(self.sample_graph)

        # Assert that the graph is a NetworkX graph object
        self.assertIsInstance(graph, nx.Graph)

        # Check that the nodes are added correctly
        self.assertTrue(graph.has_node("Tijuana"))
        self.assertTrue(graph.has_node("Rosarito"))

        # Check that the edges are added correctly
        self.assertTrue(graph.has_edge("Tijuana", "Rosarito"))
        self.assertTrue(graph.has_edge("Rosarito", "Tijuana"))

        # Check the weight of the edge
        weight = graph["Tijuana"]["Rosarito"]['weight']
        self.assertEqual(weight, 20)

    def test_load_graph_from_json_file(self):
        """
        Test that `load_graph_from_json_file` loads a graph correctly from a JSON file.
        """
        # Load graph using the function
        graph = load_graph_from_json_file(self.test_file)

        # Assert that the loaded graph is a NetworkX graph object
        self.assertIsInstance(graph, nx.Graph)

        # Check the presence of nodes
        self.assertTrue(graph.has_node("Tijuana"))
        self.assertTrue(graph.has_node("Rosarito"))

        # Check the presence of edges
        self.assertTrue(graph.has_edge("Tijuana", "Rosarito"))

        # Check the weight of the edge
        weight = graph["Tijuana"]["Rosarito"]['weight']
        self.assertEqual(weight, 20)

    def tearDown(self):
        """
        Cleanup method to remove the test files after tests are done.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


if __name__ == '__main__':
    unittest.main()
