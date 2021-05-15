import os, re

filere   = r'reut.*\.sgm'
bodyre   = r'<BODY>((?:(?:.|\n)(?!/BODY>))*)</BODY>'
titlere  = rf'<TITLE>((?:(?:.|\n)(?!/TITLE>))*)</TITLE>'
authorre = rf'<AUTHOR>((?:(?:.|\n)(?!/AUTHOR>))*)</AUTHOR>'
docre    = rf'<REUTERS[^>]*>((?:(?:.|\n)(?!/REUTERS>))*)</REUTERS>'

def load(addr):
    with open(addr, 'r') as fd:
        text = fd.read()
    docs = re.findall(docre, text)
    data = [
        {
            'id': '',
            'title': 'NoTitle',
            'text': '',
            'author': 'Uknown',
        }
        for _ in range(len(docs))
    ]
    for i in range(len(docs)):
        author = re.findall(authorre, docs[i])
        if author: data[i]['author'] = author[0]
        body = re.findall(bodyre, docs[i])
        if body: data[i]['text'] = body[0]
        title = re.findall(titlere, docs[i])
        if title: data[i]['title'] = title[0]
    return data


def reuters(addr):
    print('hello')
    from pprint import pprint
    files = os.listdir(addr)
    data = []
    for f in files:
        if re.match(filere, f):
            data.extend(load(os.path.join(addr, f)))
    for i in range(len(data)):
        data[i]['id'] = str(i + 1)
    pprint(data)
    return data
