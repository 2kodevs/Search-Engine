from .drivers import get_driver

class CorpusReader:
    def __init__(self, addr, driver, corpus_type):
        self.addr = addr
        self.driver = get_driver(driver)
        self.corpus = corpus_type
        if corpus_type == 'file': self.read(addr)
        else: self.read_addr(addr)

    def read(self):
        raise NotImplementedError()

    def read_addr(self, addr):
        raise NotImplementedError()
