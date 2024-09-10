import numpy as np
from django.test import SimpleTestCase
from .GraphOps import calculate_jaccard_edges

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