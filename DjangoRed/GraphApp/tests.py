import networkx as nx
from django.test import SimpleTestCase
from .GraphOps import calculate_jaccard_edges, get_centrality, get_communities

# Create your tests here.
class Jaccard_test(SimpleTestCase):

    def test_jaccard_calculation(self):

        # Test the range of all subreddits (no more than 50000000 users) in geospace
        for i in range(1, 23):
            power = 2**i
            set_1 = set([0])
            set_2 = set([x for x in range(power)])

            edge_list, edge_labels_dict, max_jaccard = calculate_jaccard_edges(((0, set_1), (1, set_2)))

            print(f"{i}: true {0.5**i} returned {max_jaccard}")
            self.assertAlmostEqual(max_jaccard, 1 / (power), 5)

        # Test edge cases
        set_1 = set([0])
        set_2 = set([0])
        edge_list, edge_labels_dict, max_jaccard = calculate_jaccard_edges(((0, set_1), (1, set_2)))
        self.assertAlmostEqual(max_jaccard, 1.0)
        
        set_1 = set([0])
        set_2 = set([1])
        edge_list, edge_labels_dict, max_jaccard = calculate_jaccard_edges(((0, set_1), (1, set_2)))
        self.assertAlmostEqual(max_jaccard, 0.0)

class Centrality_test(SimpleTestCase):

    def test_centrality(self):    

        # Star (hub) graph
        g = nx.Graph()
        g.add_edge(0, 1, weight=0.1)
        g.add_edge(0, 2, weight=0.2)
        g.add_edge(0, 3, weight=0.3)
        g.add_edge(0, 4, weight=0.4)
        g.add_edge(0, 5, weight=0.5)

        vertex_order = [0, 5, 4, 3, 2, 1]

        # Assert order
        sorted_verticies = get_centrality(g)
        for true, returned in zip(vertex_order, sorted_verticies):
            self.assertEqual(true, returned[0]) # returned[0] has the vertex number, returned[1] is centrality value

        # Assortative graph with equal weights
        g = nx.Graph()
        g.add_edge(0, 1, weight=1)
        g.add_edge(0, 2, weight=1)
        g.add_edge(0, 3, weight=1)
        g.add_edge(3, 2, weight=1)
        g.add_edge(2, 1, weight=1)
        g.add_edge(2, 4, weight=1)

        vertex_order = [2, 0, 1, 3, 4]

        # Assert order
        sorted_verticies = get_centrality(g)
        for true, returned in zip(vertex_order, sorted_verticies):
            self.assertEqual(true, returned[0])

        # Assortative graph with biased weights
        g = nx.Graph()
        g.add_edge(0, 1, weight=0.5)
        g.add_edge(0, 2, weight=0.3)
        g.add_edge(0, 3, weight=0.6)
        g.add_edge(3, 2, weight=0.2)
        g.add_edge(2, 1, weight=0.4)
        g.add_edge(2, 4, weight=0.1)

        vertex_order = [0, 1, 2, 3, 4]

        # Assert order
        sorted_verticies = get_centrality(g)
        for true, returned in zip(vertex_order, sorted_verticies):
            self.assertEqual(true, returned[0])