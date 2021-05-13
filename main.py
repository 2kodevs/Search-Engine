from src import Indexer, LoggerFactory as Logger

if __name__ == '__main__':
    #//TODO: Get args
    args = None

    log = Logger(name='Search-Engine', log=args.file)
    log.setLevel(args.level)

    corpus_addr = args.dir
    driver = args.driver

    idx = Indexer()
    
    data = idx.get_index(corpus_addr, driver)
    print(data)
    
