import json, os
from ..logging import LoggerFactory as Logger
from ..corpustools import CorpusReader

log = None
stopwords = [',', '.', ';', ':', '\"', '\'', '(', ')', '-', '\n'] #//TODO: Determine best place for this
class Indexer:

    def __init__(self, idx_dir = './.index/'):
        global log
        log = Logger('Search-Engine').getChild('Indexer')

        self.N = 0
        self.max_freq = []
        self.vocabulary = dict()
        self.idx_dir = idx_dir

        if not os.path.exists(self.idx_dir):
            os.mkdir(self.idx_dir)
            log.info(f'Created folder {self.idx_dir}')
            with open(self.idx_dir + 'dirs.json', 'w') as fd:
                json.dump([], fd)


    def get_index(self, corpus_dir, driver):
        index = self.load_index(corpus_dir, driver)
        if index:
            return index

        reader = CorpusReader(corpus_dir, driver)
        data = reader.get_data()

        self.N = len(data)
        self.max_freq = [0] * self.N

        terms = Indexer.tokenize(data)
        self.update_vocabulary(terms)
        return self.save_index(corpus_dir, driver)


    def load_index(self, corpus_dir, driver):
        try:
            with open(self.idx_dir + 'dirs.json', 'r') as fd_json:
                dirs = json.load(fd_json)
                for idx, item in enumerate(dirs):
                    addr, d = item
                    if corpus_dir == addr and driver == d:
                        with open(self.idx_dir + f'{driver}_index_{idx + 1}', 'r') as fd:
                            return json.load(fd)
            log.debug(f'({corpus_dir}, {driver}) not found in dirs.json')
        except FileNotFoundError:
            log.info('Index not found, proceding to create one...')
        return None


    def save_index(self, corpus_dir, driver):
        dirs = []
        with open(self.idx_dir + 'dirs.json', 'r') as fd_json:
            dirs = json.load(fd_json)
        with open(self.idx_dir + 'dirs.json', 'w') as fd_json:
            dirs.append((corpus_dir, driver))
            json.dump(dirs, fd_json)

            with open(self.idx_dir + f'{driver}_index_{len(dirs)}', 'w') as fd:
                index = self.to_dto()
                json.dump(index, fd)
                log.info('Created index ' + f'{driver}_index_{len(dirs)}' + f' at {self.idx_dir}')
                return index


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


    def to_dto(self):
        return {
            'N': self.N,
            'max_freq': self.max_freq,
            'vocabulary': self.vocabulary,
        }


    @staticmethod
    def tokenize(data):
        terms = []
        for doc in data:
            id = int(doc['id'])
            body = doc['text'] + doc['title']

            #//TODO: Consider to give more weight to terms in Title
            for sw in stopwords:
                if sw in body:
                    body = body.replace(sw, ' ')

            for s in body.split(' '):
                for word in s.split('\n'):
                    if word == '': #for text with several spaces and blanck lines
                        continue
                    terms.append((word, id))
                    
            if doc['author'] != '':
                author = doc['author']
                for sw in stopwords:
                    if sw in author:
                        author = author.replace(sw, '')
                terms.append((author, id))
        terms.sort()
        log.debug('Corpus tokenized')
        log.debug(f'Terms: {terms}')
        return terms
        
