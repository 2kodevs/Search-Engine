from ..indexer import Indexer
from math import sqrt, log10 as log

class SearchEngine():

    def __init__(self, corpus_dir, driver):
        self.indexer = Indexer()
        self.index = self.indexer.get_index(corpus_dir, driver)
        self.last_query = ''

    
    def search(self, q, threshold, a = 0.5):
        q = self.vectorize_query(q)
        w, wq = self.get_weights(q, a)

        self.last_query = q
        self.w = w
        self.wq = wq

        return self.get_ranking(w, wq, threshold)


    def get_ranking(self, w, wq, threshold):
        ranking = [0] * self.index['N']
        norm_w = ranking.copy()
        for i in range(len(wq)):
            for j in range(len(w[i])):
                ranking[j] += w[i][j] * wq[i]
                norm_w[j] += w[i][j] ** 2

        normq = sqrt(sum([wiq ** 2 for wiq in wq]))

        ranking = [(ranking[i] / (sqrt(norm_w[i]) * normq), i + 1) for i in range(len(ranking)) if norm_w[i] > 0]
        ranking.sort(reverse=True)
        ranking = list(filter(lambda sim: sim[0] >= threshold, ranking))
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

        w = [[tf[i][j] * idf[i] for j in range(N)] for i in range(len(v))]
        wq = [(a + (1 - a) * tfq[i]) * idf[i] for i in range(len(v))]
        return (w, wq)


    def vectorize_query(self, q):
        self.indexer.N = 1
        self.indexer.max_freq = [0]

        terms = Indexer.tokenize(self.get_tokenizable(q))
        self.indexer.vocabulary.clear()
        self.indexer.update_vocabulary(terms)
        return list(filter(lambda term: term in self.index['vocabulary'], self.indexer.vocabulary.keys()))


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


    def give_feedback(self, feedback, threshold, pseudo=False, k=50, alpha = 1, beta = 0.75, gamma = 0.15):
        fb = SearchEngine.process_feedback(feedback, pseudo, k)
        wq_new = self.rocchio(fb, alpha, beta, gamma)
        self.wq = wq_new
        
        return self.get_ranking(self.w, wq_new, threshold)


    def rocchio(self, feedback, alpha, beta, gamma):
        #feedback => [((sim, i), marked)]
        d, dr, dnr = feedback
        q = self.last_query
        w, wq = self.w, self.wq

        doc_vector = [0] * self.index['N']
        for i in range(len(wq)):
            for j in range(len(w[i])):
                doc_vector[j] += w[i][j]

        rv = beta / len(dr) * sum([dj for i, dj in enumerate(doc_vector) if d.get(i)])
        nrv = gamma / len(dnr) * sum([dj for i, dj in enumerate(doc_vector) if not d.get(i)])
        value = rv - nrv

        return [wqi * alpha + value for wqi in wq]


    @staticmethod
    def process_feedback(feedback, pseudo=False, k=50):
        d = dict()
        dr = list(filter(lambda d: d[1], feedback))
        dnr = 0

        if pseudo:
            dnr = list(filter(lambda d: not d[1], feedback))[:k]
            d = dict(map(lambda t: (t[0][1], t[1]), dr + dnr))
        else:
            dnr = list(filter(lambda d: not d[1], feedback))
            d = dict(map(lambda t: (t[0][1], t[1]), feedback))

        return (d, dr, dnr)
        