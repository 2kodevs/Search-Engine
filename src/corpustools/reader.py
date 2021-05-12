from .drivers import get_driver

class CorpusReader:
    def __init__(self, addr, driver, corpus_type):
        self.data = []
        self.addr = addr
        self.corpus_type = corpus_type
        self.driver = get_driver(driver)
        
    def get_data(self):
        if self.corpus_type == 'file': self.read(addr)
        else: self.read_addr(addr)
        return self.data

    def read(self, addr):
        self.data.extend(self.driver.read(addr))

    def read_addr(self, addr):
        raise NotImplementedError()
