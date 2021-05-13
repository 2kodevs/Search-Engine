import json
from ..logging import LoggerFactory as Logger

log = None
stopwords = [',', '.', ';', ':', '\"', '\'', '(', ')', '-', '\n'] #//TODO: Determine best place for this

class Indexer:

    def __init__(self, idx_dir = './indices/'):
        global log
        log = Logger('Search-Engine').getChild('Indexer')

        self.N = 0
        self.max_freq = []
        self.vocabulary = dict()
        self.idx_dir = idx_dir


    def index(self, corpus_dir, driver):
        data = [] #call to get_data() of corpustools 

        self.N = len(data)
        self.max_freq = [0] * self.N

        terms = Indexer.tokenize(data)
        self.update_vocabulary(terms)
        self.save_index(driver)


    def save_index(self, corpus_name):
        import os
        if not os.path.exists(self.idx_dir):
            os.mkdir(self.idx_dir)
            log.info(f'Created folder {self.idx_dir}')

        files_count = len([name for name in os.listdir(self.idx_dir) if os.path.isfile(name)])
        with os.open(self.idx_dir + f'{corpus_name}_index_{files_count}') as fd:
            fd.write(self.to_json())
            log.info('Created index ' + f'{corpus_name}_index_{files_count}' + f' at {self.idx_dir}')


    def update_vocabulary(self, terms):
        terms.append(('zzzzz$$$$$&&&&&&', -1))
        unique_terms = list({ word for (word, _) in terms })
        unique_terms.sort()
        last_idx = 0

        for term in unique_terms:
            idx = terms[last_idx][1]
            freq = 0
            for i in range(last_idx, len(terms)):
                word, id = terms[i]

                if id != idx or word != term:
                    if (not self.vocabulary.get(term)):
                        self.vocabulary[term] = []
                    self.vocabulary[term].append((idx, freq))
                    self.max_freq[idx - 1] = max(freq, self.max_freq[idx - 1])
                    if word != term:
                        last_idx = i
                        break
                    idx = id
                    freq = 0
                
                freq += 1
                last_idx = i
        log.debug('Vocabulary updated')
        log.debug(f'Vocabulary: {self.vocabulary}')


    def to_json(self):
        temp = {
            'N': self.N,
            'max_freq': self.max_freq,
            'vocabulary': self.vocabulary,
        }
        return json.dump(temp)


    @staticmethod
    def tokenize(data):
        terms = []
        for doc in data:
            id = doc['ID']
            body = doc['Text'] + doc['Title']

            #//TODO: Consider to give more weight to terms in Title
            for word in body.split(' '):

                for sw in stopwords:
                    if sw in word:
                        word = word.replace(sw, '')

                if word == '': #for text with several spaces and blanck lines
                    continue

                terms.append((word, id))
            if doc['Author'] != '':
                terms.append((doc['Author'], id))
        terms.sort()
        log.debug('Corpus tokenized')
        log.debug(f'Terms: {terms}')
        return terms