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
                idx = dirs.index([corpus_dir, driver])
                with open(self.idx_dir + f'{driver}_index_{idx + 1}', 'r') as fd:
                    return json.load(fd)
        except ValueError:
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
        freq = 1
        terms.append((None, None))
        for i in range(1, len(terms)):
            if terms[i] != terms[i - 1]:
                term, id = terms[i - 1]
                if term not in self.vocabulary:
                    self.vocabulary[term] = []
                self.vocabulary[term].append((id, freq))
                self.max_freq[id - 1] = max(freq, self.max_freq[id - 1])
                freq = 0
            freq += 1
        terms.pop()
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

            for words in body.split(' '):
                terms.append((word, id))
                    
            if doc['author'] != '':
                author = doc['author']
                for sw in stopwords:
                    author = author.replace(sw, '')
                terms.append((author, id))
        terms.sort()
        log.debug('Corpus tokenized')
        log.debug(f'Terms: {terms}')
        return terms
        
