from .drivers import get_driver

class CorpusReader:
    def __init__(self, addr, driver, file_corpus):
        self.data = []
        self.addr = addr
        self.file_corpus = file_corpus
        self.driver = get_driver(driver)
        
    def get_data(self):
        if self.file_corpus: self.read(self.addr)
        else: self.read_addr(self.addr)
        return self.data

    def read(self, addr):
        self.data.extend(self.driver(addr))

    def read_addr(self, addr):
        raise NotImplementedError()
