from src import SearchEngine, SessionState, CorpusReader #, LoggerFactory as Logger
from src.corpustools.drivers import drivers
import streamlit as st


# def init_logger(args):
#     log = Logger(name='Search-Engine', log=args.file)
#     log.setLevel(args.level)
#     return log


def visual(args):
    # log = init_logger(args)

    session = SessionState(code='test')

    st.title('Search Engine App')
    st.sidebar.title('Settings')
    with st.sidebar.form('config'):
        corpus = st.text_input('Corpus Directory:', help='The directory where the corpus is stored')
        driver = st.selectbox('Driver:', help='The driver needed to parse the corpus', options=[d.__name__ for d in drivers])
        with st.beta_expander("Advanced"):
            sim = st.slider("Minimum percent of similarity between query and documents:", min_value=0.0, max_value=100.0, value=45.0, format="%f%%")
        st.write('Press save to persist the changes')
        savebutton = st.form_submit_button(label='Save')

    if corpus and driver:
        with st.form('query-section'):
            query = st.text_input('Query', help='Type what are you looking for')
            fbutton = st.form_submit_button(label='Search')

        if query: 
            if fbutton or savebutton:
                session.se = SearchEngine(corpus, driver)
                session.rank = session.se.search(query, sim/100)
            
            with st.form('retro'):
                data, selection = [], False
                cr = CorpusReader(corpus, driver)
                for ((p, id), (t, a)) in zip(session.rank, cr.get_info(session.rank)):
                    left, rigth = st.beta_columns([5, 1])
                    with left:
                        st.write(t)
                        st.caption(a)
                        # st.write(id)
                    v = rigth.checkbox('', key=f'check{corpus}-{driver}-{query}{id}')
                    data.append(((p, id), v))
                    selection |= v
                left, right = st.beta_columns([1, 3])
                with left:
                    rbutton = st.form_submit_button()
                with right:
                    st.write("Select and submit the relevant files to improve results")

            if rbutton:
                if selection:
                    session.rank = session.se.give_feedback(data, sim/100) 
                else:
                    st.error('You need to mark some data as relevant')    
        else:
            st.warning('A non empty query required')            
        
    else:
        st.header('An initial configuration is needed. Please fill the settings section in order to procced.')
        if not corpus: st.warning('Corpus setting required')
        if not driver: st.warning('Driver setting required')


def cmd(args):
    # log = init_logger(args)
    # log.info('Running the indexer', 'cmd')

    se = SearchEngine(args.corpus, args.driver)
    ranking = se.search(args.query, args.sim/100)
    print(ranking)


def evaluation(args):
    from src.corpustools.drivers import get_driver

    queries = get_driver(args.driver).queries(*args.params) 
    engine = SearchEngine(args.corpus, args.driver)

    precisions, recalls = [], []
    for query_data in queries:
        q = query_data['query']
        ranking = engine.search(q, 0)
        p, r = engine.evaluate_ranking(ranking, query_data, args.recover)
        precisions.append(p)
        recalls.append(r)

    fails = len(list(filter(lambda r: r == 0, recalls)))

    print(f'Precision mean: {sum(precisions) / len(precisions)}')
    print(f'Recall mean: {sum(recalls) / len(recalls)}')
    print(f'Queries with wrong results: {fails} ({fails * 100 / len(queries)}%)')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Search Engine parser")
    subparsers = parser.add_subparsers()

    cmdline = subparsers.add_parser('cmd', help="Solve a query from cmd")
    cmdline.add_argument('-d', '--driver', type=str,   required=True,  help='driver to use in the corpus parsing proccess')
    cmdline.add_argument('-c', '--corpus', type=str,   required=True,  help='corpus dir')
    cmdline.add_argument('-f', '--file',   action='store_true',        help='use the logs file')
    cmdline.add_argument('-l', '--level',  type=str,   default='INFO', help='log level')
    cmdline.add_argument('-q', '--query',  type=str,   required=True,  help='query to retrive')
    cmdline.add_argument('-s', '--sim',    type=float, default=45,      help='Minimum sim value')
    cmdline.set_defaults(command=cmd)

    app = subparsers.add_parser('visual', help="Open the visual application")
    app.set_defaults(file=True)
    app.set_defaults(level='INFO')
    app.set_defaults(command=visual)

    evaluator = subparsers.add_parser('eval', help="Run the search engine evaluation")
    evaluator.add_argument('-d', '--driver',  type=str,   required=True,  help='driver to use in the corpus parsing proccess')
    evaluator.add_argument('-c', '--corpus', type=str,   required=True,  help='corpus dir')
    evaluator.add_argument('-p', '--params',  nargs='+',  default=[],     help="Driver parameters")
    evaluator.add_argument('-s', '--sim',     type=float, default=45,      help='Minimum sim value')
    evaluator.add_argument('-r', '--recover', type=int,  default=20,      help='Minimum sim value')
    evaluator.add_argument('-f', '--file',    action='store_true',        help='use the logs file')
    evaluator.add_argument('-l', '--level',   type=str,   default='INFO', help='log level')
    evaluator.set_defaults(command=evaluation)

    args = parser.parse_args()
    if not hasattr(args, 'command'): parser.print_help()
    else: args.command(args)
