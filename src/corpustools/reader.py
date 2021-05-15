from .drivers import get_driver
import json, os

class CorpusReader:
    def __init__(self, addr, driver, parse_dir='./.parse/'):
        self.data = []
        self.addr = addr
        self.parse_dir = parse_dir
        print(driver)
        self.driver = get_driver(driver)
        print(self.driver)

        if not os.path.exists(self.parse_dir):
            os.mkdir(self.parse_dir)

    def get_dir(self):
        addr = self.addr.replace('/','-')
        return f'{self.parse_dir}{self.driver.__name__.lower()}-{addr}'
        
    def get_data(self):
        self.read(self.addr)

        tosave = ['id', 'title', 'author']
        self.simple = list(map(lambda item: {x:item[x] for x in tosave}, self.data))
        with open(self.get_dir(), 'w') as fd:
            json.dump(self.simple, fd)
        return self.data

    def get_info(self, rank):
        try:
            with open(self.get_dir(), 'r') as fd:
                self.simple = json.load(fd)
        except FileNotFoundError:
            self.get_data()
        details = []
        for (_, id) in rank:
            info = self.simple[id - 1]
            details.append((info['title'], info['author']))
        return details

    def read(self, addr):
        self.data.extend(self.driver.read(addr))
