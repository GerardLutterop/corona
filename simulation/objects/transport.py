from .general import Object, Objects

class Transport(Object):
    def __init__(self):
        pass

class Walk(Transport):
    """Take walk in the fresh air"""
    
class PublicTransport(Transport):
    """Any public transport"""

class Train(PublicTransport):
    """Long distance"""
    
class Bus(PublicTransport):
    """Shorter distance"""

class Plane(PublicTransport):
    """International and intercontinental"""

class Taxi(PublicTransport):
    """Short distance, small groups"""

class PrivateTransport(Transport):
    """Not publicly accessible"""

class Car(PrivateTransport):
    """Short, medium and long distance, mostly by individuals and families."""

class Bike(PrivateTransport):
    """Short distance, single driver or with small kids"""

