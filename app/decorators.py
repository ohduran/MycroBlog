"""Decorators module."""
from threading import Thread


def async(f):
    """Have a function work asyncronously."""
    def wrapper(*args, **kwargs):
        thread = Thread(target=f, args=args, kwargs=kwargs)
        thread.start()
        return wrapper
