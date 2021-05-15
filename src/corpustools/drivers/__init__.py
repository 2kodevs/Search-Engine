from .cranfield import Cranfield

drivers = [
    Cranfield,
]

def get_driver(name):
    for driver in drivers:
        if driver.__name__.lower() == name.lower():
            return driver
    raise NameError(f'Driver <{name}> not found')
