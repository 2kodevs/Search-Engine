from src import SearchEngine #, LoggerFactory as Logger
from src import SessionState
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
        corpus = st.text_input('Corpus Address:', help='The address where the corpus is stored')
        driver = st.text_input('Driver:',         help='The driver needed to parse the corpus')
        with st.beta_expander("Advanced"):
            sim = st.slider("Minimum percent of similarity between query and documents:", min_value=0.0, max_value=100.0, value=0.0, format="%f%%")
        st.write('Press submit to persist the changes')
        st.form_submit_button()

    if corpus and driver:
        with st.form('query-section'):
            query = st.text_input('Query', help='Type what are you looking for')
            fbutton = st.form_submit_button(label='Search')

        if query: 
            if fbutton:
                session.se = SearchEngine(corpus, driver)
                session.rank = session.se.search(query, sim)
            
            with st.form('retro'):
                data = []
                for (a, b) in session.rank:
                    left, rigth = st.beta_columns([5, 1])
                    left.write(b)
                    v = rigth.checkbox('', key=f'check{corpus}-{driver}-{query}{b}')
                    data.append(((a, b), v))
                left, rigth = st.beta_columns(2)
                with left:
                    rbutton = st.form_submit_button()
                with rigth:
                    st.write("Select and submit the relevant files")

            if rbutton:
                session.rank = session.se.give_feedback(data, sim)     
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
    ranking = se.search(args.query, args.sim)
    print(ranking)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Search Engine parser")
    subparsers = parser.add_subparsers()

    cmdline = subparsers.add_parser('cmd', help="Solve a query from cmd")
    cmdline.add_argument('-d', '--driver', type=str,   required=True,  help='driver to use in the corpus parsing proccess')
    cmdline.add_argument('-c', '--corpus', type=str,   required=True,  help='corpus address')
    cmdline.add_argument('-f', '--file',   action='store_true',        help='use the logs file')
    cmdline.add_argument('-l', '--level',  type=str,   default='INFO', help='log level')
    cmdline.add_argument('-q', '--query',  type=str,   required=True,  help='query to retrive')
    cmdline.add_argument('-s', '--sim',    type=float, default=0,      help='Minimum sim value')
    cmdline.set_defaults(command=cmd)

    app = subparsers.add_parser('visual', help="Open the visual application")
    app.set_defaults(file=True)
    app.set_defaults(level='INFO')
    app.set_defaults(command=visual)

    args = parser.parse_args()
    if not hasattr(args, 'command'): parser.print_help()
    else: args.command(args)
