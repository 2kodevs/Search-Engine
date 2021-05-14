import re

txtblock = "\n((?:(?=[^.])(?:.*\n))*)" 
docre = rf'\.I (.+)\n\.T{txtblock}\.A{txtblock}\.B{txtblock}\.W{txtblock}'

class Cranfield:
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
    @staticmethod
    def read(addr):
    with open(addr, 'r') as fd:
        doctext = fd.read()
    matchings = re.findall(docre, doctext)
    return [
        {
            'id':     id,
            'B':      b.lower(),
            'text':   text.lower(),
            'title':  title.lower(),
            'author': author.lower(),
        } 
        for (id, title, author, b, text) in matchings
    ]
