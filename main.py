from src import SearchEngine, LoggerFactory as Logger


def init_logger(args):
    log = Logger(name='Search-Engine', log=args.file)
    log.setLevel(args.level)
    return log


def visual(args):
    log = init_logger(args)
    log.info('Starting the app', 'visual')


def cmd(args):
    log = init_logger(args)
    log.info('Running the indexer', 'cmd')

    se = SearchEngine(args.corpus_dir, args.driver)
    ranking = se.search(args.query, args.sim)
    print(ranking)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Search Engine parser")
    subparsers = parser.add_subparsers()

    cmdline = subparsers.add_parser('cmd', help="Solve a query from cmd")
    cmdline.add_argument('-d', '--driver', type=str,   required=True,       help='driver to use in the corpus parsing proccess')
    cmdline.add_argument('-c', '--corpus', type=str,   required=True,       help='corpus address')
    cmdline.add_argument('-f', '--file',   type=bool,  action='store_true', help='use the logs file')
    cmdline.add_argument('-l', '--level',  type=str,   default='INFO',      help='log level')
    cmdline.add_argument('-q', '--query',  type=str,   required=True,       help='query to retrive')
    cmdline.add_argument('-s', '--sim',    type=float, default=0,           help='Minimum sim value')
    cmdline.set_defaults(command=cmd)

    app = subparsers.add_parser('visual', help="Open the visual application")
    app.set_defaults(file=True)
    app.set_defaults(level='INFO')
    app.set_defaults(command=visual)

    args = parser.parse_args()
    if not hasattr(args, 'command'): parser.print_help()
    else: args.command(args)
