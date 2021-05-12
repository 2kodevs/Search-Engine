import re

docre = r'\.I (.+)\n\.T\n((?:(?=[^.])(?:.*\n))*)\.A\n((?:(?=[^.])(?:.*\n))*)\.B\n((?:(?=[^.])(?:.*\n))*)\.W\n((?:(?=[^.])(?:.*\n))*)'

def cranfield(addr):
    '''
    parse corpus files of the form:
        .I #
        .T
        <multiline text for doc title>
        .A
        <multiline text for doc author>
        .B
        <multiline text for //TODO: What is this>
        .W
        <multiline text for doc text>
    repeated any number of times.
    '''
    with open(addr, 'r') as fd:
        doctext = fd.read()
    matchings = re.findall(docre, doctext)
    return [
        {
            'B':      b,
            'id':     id,
            'text':   text,
            'title':  title,
            'author': author,
        } 
        for (id, title, author, b, text) in matchings
    ]
