import time
from .general import Object
from .persons import *

class Choreography(Object):
    def __init__(self):
        p = Person(None)
    
    def run(self):
        print('run')