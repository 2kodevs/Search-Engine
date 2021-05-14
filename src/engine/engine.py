from ..indexer import Indexer
from math import sqrt, log10 as log

class SearchEngine():

    def __init__(self, corpus_dir, driver):
        self.indexer = Indexer()
        self.index = self.indexer.get_index(corpus_dir, driver)

    
    def search(self, q, threshold, a = 0.5):
        q = self.vectorize_query(q)
        q = list(filter(lambda term: term in self.index['vocabulary'], q))

        w, wq = self.get_weights(q, a)

        ranking = [0] * self.index['N']
        norm_w = ranking.copy()
        for i in range(len(q)):
            for j in range(len(w[i])):
                ranking[j] += w[i][j] * wq[i]
                norm_w[j] += w[i][j] ** 2

        normq = sqrt(sum([wiq ** 2 for wiq in wq]))

        ranking = [ranking[i] / (norm_w[i] * normq)]
        ranking.sort()
        ranking = filter(lambda sim: sim >= threshold, ranking)
        return ranking


    def get_weights(self, v, a):
        n = [len(self.index['vocabulary'][term]) for term in v ]
        N = self.index['N']
        #idf_i = log(N, n_i)
        idf = [log(N / n_i) for n_i in n]

        max_freq = self.index['max_freq']
        max_freq_q = self.indexer.max_freq[0]
        #tf_{i, j} = freq_{i, j} / max_l freq_{l, j}
        tf = [[0] * N for _ in range(len(v))]
        tfq = [freq / max_freq_q for [(_, freq)] in self.indexer.vocabulary.values()]

        for i, term in enumerate(v):
            for (docID, freq) in self.index['vocabulary'][term]:
                tf[i][docID - 1] = freq / max_freq[docID - 1]

        w = [[tf[i][j] * idf[i] for j in range(len(tf[i]))] for i in range(len(v))]
        wq = [(a + (1 - a) * tfq[i]) * idf[i] for i in range(len(v))]
        return (w, wq)


    def vectorize_query(self, q):
        self.indexer.N = 1
        self.indexer.max_freq = [0]

        terms = self.indexer.tokenize(self.get_tokenizable(q))
        self.indexer.update_vocabulary(terms)
        return list(self.indexer.vocabulary.keys())


    def get_tokenizable(self, q):
        return [
            {
                'id':       1,
                'B':        '',
                'text':     q,
                'title':    '',
                'author':   '',
            }
        ]
        
