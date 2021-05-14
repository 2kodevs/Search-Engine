import unittest
from src import Indexer

class IndexerTestCase(unittest.TestCase):
    def setUp(self):
        self.Indexer = Indexer()
        self.maxDiff = None

    def test_tokenizer(self):
        #data ok 1 doc
        data = [{
            'id': 1,
            'title': 'some random title',
            'author': 'alan brito',
            'text': """
                here lies the test of tests, the supreme test, first 2kodevs test using python.

                this day should be remembered forever, the future of the tests depends on it. we have a heavy burden for now on.
            """,
        }]

        terms = Indexer.tokenize(data)
        ans = [
            ('some', 1), ('random', 1), ('title', 1), ('alan brito', 1), ('here', 1), ('lies', 1),
            ('the', 1), ('test', 1), ('of', 1), ('tests', 1), ('the', 1), ('supreme', 1), ('test', 1),
            ('first', 1), ('2kodevs', 1), ('test', 1), ('using', 1), ('python', 1), ('this', 1), ('day', 1),
            ('should', 1), ('be', 1), ('remembered', 1), ('forever', 1), ('the', 1), ('future', 1), ('of', 1),
            ('the', 1), ('tests', 1), ('depends', 1), ('on', 1), ('it', 1), ('we', 1), ('have', 1), ('a', 1),
            ('heavy', 1), ('burden', 1), ('for', 1), ('now', 1), ('on', 1),
        ]
        ans.sort()
        self.assertEqual(terms, ans)

        #data with many stopwords and blank spaces 1 doc
        data = [{
            'id': 1,
            'title': 'some random title',
            'author': 'alan brito',
            'text': """
                here lies the   test of ... tests, the supreme-test, first \n2kodevs\n test using python.


                this day should be; remembered: . forever, the future   of the tests ,,,depends on it. we have a heavy burden for now on.

            """,
        }]

        terms = Indexer.tokenize(data)
        ans = [
            ('some', 1), ('random', 1), ('title', 1), ('alan brito', 1), ('here', 1), ('lies', 1),
            ('the', 1), ('test', 1), ('of', 1), ('tests', 1), ('the', 1), ('supreme', 1), ('test', 1),
            ('first', 1), ('2kodevs', 1), ('test', 1), ('using', 1), ('python', 1), ('this', 1), ('day', 1),
            ('should', 1), ('be', 1), ('remembered', 1), ('forever', 1), ('the', 1), ('future', 1), ('of', 1),
            ('the', 1), ('tests', 1), ('depends', 1), ('on', 1), ('it', 1), ('we', 1), ('have', 1), ('a', 1),
            ('heavy', 1), ('burden', 1), ('for', 1), ('now', 1), ('on', 1),
        ]
        ans.sort()
        self.assertEqual(terms, ans)

        #data ok 2 doc
        data = [{
            'id': 1,
            'title': 'some random title',
            'author': 'alan brito',
            'text': """
                here lies the test of tests, the supreme test, first 2kodevs test using python.

                this day should be remembered forever, the future of the tests depends on it. we have a heavy burden for now on.
            """,
        },
        {
            'id': 2,
            'title': 'some random title 2',
            'author': 'susana horia',
            'text': """
                less meaningfuls words around here, still testing tests with some test
            """,
        }
        ]

        terms = Indexer.tokenize(data)
        ans = [
            ('some', 1), ('random', 1), ('title', 1), ('alan brito', 1), ('here', 1), ('lies', 1),
            ('the', 1), ('test', 1), ('of', 1), ('tests', 1), ('the', 1), ('supreme', 1), ('test', 1),
            ('first', 1), ('2kodevs', 1), ('test', 1), ('using', 1), ('python', 1), ('this', 1), ('day', 1),
            ('should', 1), ('be', 1), ('remembered', 1), ('forever', 1), ('the', 1), ('future', 1), ('of', 1),
            ('the', 1), ('tests', 1), ('depends', 1), ('on', 1), ('it', 1), ('we', 1), ('have', 1), ('a', 1),
            ('heavy', 1), ('burden', 1), ('for', 1), ('now', 1), ('on', 1), ('some', 2), ('random', 2), ('title', 2),
            ('2', 2), ('susana horia', 2), ('less', 2), ('meaningfuls', 2), ('words', 2), ('around', 2),
            ('here', 2), ('still', 2), ('testing', 2), ('tests', 2), ('with', 2), ('some', 2), ('test', 2)
        ]
        ans.sort()
        self.assertEqual(terms, ans)

    def test_update_vocabulary(self):
        data = [{
            'id': 1,
            'title': 'some random title',
            'author': 'alan brito',
            'text': """
                here lies the test of tests, the supreme test, first 2kodevs test using python.
            """,
        },
        {
            'id': 2,
            'title': 'some random title 2',
            'author': 'susana horia',
            'text': """
                less meaningfuls words around here, still testing tests with some test
            """,
        }
        ]

        terms = Indexer.tokenize(data)
        self.Indexer.max_freq = [0, 0]
        self.Indexer.update_vocabulary(terms)

        ans = {
            'some': [(1, 1), (2, 2)],
            'random': [(1, 1), (2, 1)],
            'title': [(1, 1), (2, 1)],
            'alan brito': [(1, 1)],
            'here': [(1, 1), (2, 1)],
            'lies': [(1, 1)],
            'the': [(1, 2)],
            'test': [(1, 3), (2, 1)],
            'of': [(1, 1)],
            'tests': [(1, 1), (2, 1)],
            'supreme': [(1, 1)],
            'first': [(1, 1)],
            '2kodevs': [(1, 1)],
            'using': [(1, 1)],
            'python': [(1, 1)],
            'susana horia': [(2, 1)],
            '2': [(2, 1)],
            'less': [(2, 1)],
            'meaningfuls': [(2, 1)],
            'around': [(2, 1)],
            'still': [(2, 1)],
            'testing': [(2, 1)],
            'words': [(2, 1)],
            'with': [(2, 1)],
        }
        self.assertDictEqual(self.Indexer.vocabulary, ans)
        self.assertEqual(self.Indexer.max_freq, [3, 2])
