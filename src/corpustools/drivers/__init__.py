from .cranfield import Cranfield
from .newsgroup import NewsGroup
from .reuters import Reuters

drivers = [
    Cranfield,
    Reuters,
    NewsGroup,
]

def get_driver(name):
    for driver in drivers:
        if driver.__name__.lower() == name.lower():
            return driver
    raise NameError(f'Driver <{name}> not found')
