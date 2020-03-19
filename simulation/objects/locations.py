from .general import Object

class GeoCoordinates(Object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class Business(Object):
    pass