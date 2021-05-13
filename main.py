from src import LoggerFactory as Logger

if __name__ == '__main__':
    #//TODO: Get args
    args = None

    log = Logger(name='Search-Engine', log=args.file)
    log.setLevel(args.level)