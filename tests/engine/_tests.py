import unittest
from src import SearchEngine

class SearchEngineTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = SearchEngine('./tests/mocks/animal_corpus', 'cranfield')

    def test_vectorize_query(self):
        q = 'zorro nutria'
        ans = ['nutria', 'zorro']
        self.assertEqual(self.engine.vectorize_query(q), ans)

    def test_get_weights(self):
        q = 'zorro nutria'
        q = self.engine.vectorize_query(q)
        q = list(filter(lambda term: term in self.engine.index['vocabulary'], q))

        self.engine.indexer.N = 1
        self.engine.indexer.max_freq = [1]

        w, wq = self.engine.get_weights(q, 0.5)
        ans_w = [
            [0.09, 0.09, 0.09, 0.09, 0],
            [0, 0, 0.39, 0, 0.39],
            [0, 0.066, 0.2, 0.2, 0],
            ]
        self.assertEqual(w, ans_w)