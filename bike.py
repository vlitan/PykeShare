import json
from pprint import pprint

def printBike(bike):
    pprint (bike)

class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getJson(self):
        result = {}
        result['x'] = self.x
        result['y'] = self.y
        return result

class Bike(object):
    def __init__(self, id, status, location):
        self.id = id
        self.status = status
        self.location = location

    def getJson(self):
        result = {}
        result['id'] = self.id
        result['location'] = self.location.getJson()
        result['status'] = self.status
        return result

    def getText(self):
        return json.dumps(self.getJson())
