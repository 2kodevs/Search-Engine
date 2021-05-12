import re

docre = r'\.I (.+)\n\.T\n((?:(?=[^.])(?:.*\n))*)\.A\n((?:(?=[^.])(?:.*\n))*)\.B\n((?:(?=[^.])(?:.*\n))*)\.W\n((?:(?=[^.])(?:.*\n))*)'

def cranfield(addr):
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
