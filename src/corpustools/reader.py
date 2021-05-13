from .drivers import get_driver

class CorpusReader:
    def __init__(self, addr, driver):
        self.data = []
        self.addr = addr
        self.driver = get_driver(driver)
        
    def get_data(self):
        self.read(self.addr)
        return self.data

    def read(self, addr):
        self.data.extend(self.driver(addr))
