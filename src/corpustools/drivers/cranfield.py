import re

txtblock = "\n((?:(?=[^.])(?:.*\n))*)" 
docre = rf'\.I (.+)\n\.T{txtblock}\.A{txtblock}\.B{txtblock}\.W{txtblock}'
qryre = rf'\.I .+\n\.W{txtblock}'
relre = r'(.+) (.+) .+\n'

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

    
    @staticmethod
    def queries(query, rel):
        with open(query, 'r') as fd:
            querytext = fd.read()
        with open(rel, 'r') as fd:
            reltext = fd.read()
        q = re.findall(qryre, querytext)
        r = re.findall(relre, reltext)
        data = [
            {
                'rel':   [],
                'id':    str(id + 1),
                'query': text.lower(),
            } 
            for (id, text) in enumerate(q)
        ]
        for id, a in r:
            data[int(id) - 1]['rel'].append(int(a))
        return data
