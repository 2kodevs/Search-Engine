import json

class Indexer:

    def __init__(self, idx_dir = './indices/'):
        self.N = 0
        self.max_freq = []
        self.vocabulary = dict()
        self.idx_dir = idx_dir

    def index(self):
        data = [] #call to get_data() of corpustools 

        self.N = len(data)
        self.max_freq = [0] * self.N

        terms = Indexer.get_raw_terms(data)
        self.update_vocabulary(terms)
        self.save_index()


    def save_index(self):
        import os
        if not os.path.exists(self.idx_dir):
            os.mkdir(self.idx_dir)
            
        files_count = len([name for name in os.listdir(self.idx_dir) if os.path.isfile(name)])
        with os.open(self.idx_dir + f'index_{files_count}') as fd:
            fd.write(self.to_json())

    def update_vocabulary(self, terms):
        unique_terms = { word for (word, _) in terms }
        last_idx = 0

        for term in unique_terms:
            idx = terms[last_idx][1]
            freq = 0
            for i in range(last_idx, len(terms)):
                word, id = terms[i]
                if (word != term):
                    break
                if (id != idx):
                    if (not self.vocabulary[word]):
                        self.vocabulary[word] = []
                    self.vocabulary[word].append((idx, freq))
                    self.max_freq[idx] = max(freq, self.max_freq[idx])
                    idx = id
                    freq = 0
                
                freq += 1
                last_idx = i

    def to_json(self):
        temp = {
            'N': self.N,
            'max_freq': self.max_freq,
            'vocabulary': self.vocabulary,
        }
        return json.dump(temp)


    @staticmethod
    def get_raw_terms(data):
        terms = []
        for doc in data:
            id = doc['ID']
            body = doc['Text'] + doc['Title']

            #//TODO: Consider to give more weight to terms in Title
            for word in body.split(' '):
                if word is None: #for text with several spaces
                    continue
                terms.append((word, id))
            if doc['Author'] != '':
                terms.append((doc['Author'], id))
        terms.sort()
        return terms