import unittest
import json
import os
from src.data.json_loader import load_graph_from_json, save_graph_to_json


class TestJsonLoader(unittest.TestCase):

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
        save_graph_to_json(self.sample_graph, self.test_file)

    def test_load_graph_from_json(self):
        """
        Test that the `load_graph_from_json` function correctly loads graph data from a JSON file.
        """
        graph_data = load_graph_from_json(self.test_file)

        # Assert that the loaded graph matches the sample graph
        self.assertEqual(graph_data, self.sample_graph)

        # Ensure the graph data structure is a dictionary
        self.assertIsInstance(graph_data, dict)

        # Ensure specific content is loaded correctly (e.g., check for Tijuana node)
        self.assertIn("Tijuana", graph_data)
        self.assertIn("Rosarito", graph_data)

    def test_save_graph_to_json(self):
        """
        Test that the `save_graph_to_json` function correctly saves graph data to a JSON file.
        """
        new_graph = {
            "Mexicali": [
                {"node": "Tijuana", "weight": 135},
                {"node": "San Felipe", "weight": 197}
            ]
        }

        save_graph_to_json(new_graph, 'new_test_graph.json')

        # Verify the new file is created and contains correct data
        with open('new_test_graph.json', 'r') as f:
            loaded_graph = json.load(f)

        self.assertEqual(loaded_graph, new_graph)

        # Cleanup the created file
        os.remove('new_test_graph.json')

    def tearDown(self):
        """
        Cleanup method to remove the test files after tests are done.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


if __name__ == '__main__':
    unittest.main()
