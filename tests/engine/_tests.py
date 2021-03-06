import unittest
from src import SearchEngine, Indexer

class SearchEngineTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = SearchEngine('./tests/mocks/animal_corpus', 'cranfield')

    def test_vectorize_query(self):
        q = 'zorro nutria'
        ans = ['nutria', 'zorro']
        self.assertEqual(self.engine.vectorize_query(q), ans)


    def test_get_weights(self):
        q = 'leon nutria zorro'
        q = self.engine.vectorize_query(q)
        q = list(filter(lambda term: term in self.engine.index['vocabulary'], q))

        self.engine.indexer.N = 1
        self.engine.indexer.max_freq = [1]

        w, wq = self.engine.get_weights(q, 0.5)
        ans_w = [
            [0.09691001300805642, 0.09691001300805642, 0.09691001300805642, 0.09691001300805642, 0],
            [0, 0, 0.3979400086720376, 0, 0.3979400086720376],
            [0, 0.07394958320545211, 0.22184874961635637, 0.22184874961635637, 0],
            ]
        self.assertEqual(w, ans_w)

    
    def test_search(self):
        q = 'nutria leon'
        ranking = self.engine.search(q, 0)
        print(ranking)

    def test__full_feedback(self):
        q = 'nutria leon zorro'
        ranking = self.engine.search(q, 0)
        print(ranking)
        feedback = [
            (ranking[0], True),
            (ranking[1], True),
            (ranking[2], False),
            (ranking[3], True),
            (ranking[4], False),
        ]
        ranking = self.engine.give_feedback(feedback, 0)
        print(ranking)

    def test__pseudo_feedback(self):
        q = 'nutria leon zorro'
        ranking = self.engine.search(q, 0)
        print(ranking)
        feedback = [
            (ranking[0]),
            (ranking[1]),
            (ranking[2]),
            (ranking[3]),
            (ranking[4]),
        ]
        ranking = self.engine.give_feedback(feedback, 0, True, 3)
        print(ranking)
        