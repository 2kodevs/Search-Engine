import os, re


fsre = rf'(?:.|\n)*From: (.+)\nSubject: (.*)\n((?:.|\n)*)'
sfre = rf'(?:.|\n)*Subject: (.+)\nFrom: (.*)\n((?:.|\n)*)'


class NewsGroup:
    @staticmethod
    def load(addr):
        with open(addr, 'rb') as fd:
            text = fd.read().decode('utf-8', errors='backslashreplace')
        try:
            [(author, title, text)] = re.findall(fsre, text)
        except ValueError:
            [(title, author, text)] = re.findall(sfre, text)
        return {
            'id': '',
            'text': text,
            'title': title,
            'author': author,
        }


    @staticmethod
    def read(addr):
        files = os.listdir(addr)
        data = []
        for f in files:
            data.append(NewsGroup.load(os.path.join(addr, f)))
        for i in range(len(data)):
            data[i]['id'] = str(i + 1)
        return data
