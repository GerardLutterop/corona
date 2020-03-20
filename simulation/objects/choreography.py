import time
from .general import Object
from .persons import *

__all__ = ['Choreography']

class Choreography(Object):
    def __init__(self):
        self.persons = Persons()
        for _ in range(17000):
            self.persons.append(Person())
    
    def run(self):
        print('run')
        self.persons.move()