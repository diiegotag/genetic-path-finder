import unittest
import networkx as nx
from src.visualization.visualization import visualize_graph, visualize_path
from unittest.mock import patch


class TestVisualization(unittest.TestCase):

    def setUp(self):
        """Set up a simple graph for testing."""
        self.g = nx.Graph()
        self.g.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])

    @patch("matplotlib.pyplot.show")
    def test_visualize_graph(self, mock_show):
        """Test the visualize_graph function."""
        # Call the visualization function
        visualize_graph(self.g)

        # Assert that show was called (indicating the graph was rendered)
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.show")
    def test_visualize_path(self, mock_show):
        """Test the visualize_path function."""
        path = [1, 2, 3, 4]
        visualize_path(self.g, path)

        # Assert that show was called (indicating the path was rendered)
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
