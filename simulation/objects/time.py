import datetime
from .general import Object

class Timestamp(Object):
    def __init__(self, time=None):
        self._time = time or datetime.datetime.now()
