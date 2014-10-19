'''
Created on Oct 15, 2014

@author: bjw
'''

"""
    An iterator to walk over a TurnList path.
    Given a TurnList: FLFFRRLFF
    Iteratively returns a series of coordinates such as
    (0,1), (-1,1), (-2,1), (-3,1), (-3,2), (-2,2), ...
    NOTE: (0,0) is _not_ the first coordinate
"""
from model.coordinates import CoordinateList
class PathWalker:
    def __init__(self, turnList, start=(0,0), facing='N'):
        self.turnList = turnList
        self.start = start  
        self.facing = facing
    
    def walk(self):
        current_location = self.start
        coordinates = CoordinateList()
        for index in range(self.turnList.size()):
            turn, value = self.turnList.get(index)
            if   (turn == 'F'):
                next_location = self._forward(current_location)
            elif (turn == 'L'):
                next_location = self._turnLeft(current_location)
            elif (turn == 'R'):
                next_location = self._turnRight(current_location)
            else:
                print "Unexpected Path: " + turn
            coordinates.append(next_location, value)
            current_location = next_location
        return coordinates

    def _forward(self, location):
        x, y = location
        if   self.facing == 'N':
            return (x,y+1)
        elif self.facing == 'E':
            return (x+1,y)
        elif self.facing == 'S':
            return (x,y-1)
        elif self.facing == 'W':
            return (x-1, y)     
    
    def _turnLeft(self, location):
        if   self.facing == 'N':
            self.facing = 'W'
        elif self.facing == 'E':
            self.facing = 'N'
        elif self.facing == 'S':
            self.facing = 'E'
        elif self.facing == 'W':
            self.facing = 'S'
        return self._forward(location)
    
    def _turnRight(self, location):
        if   self.facing == 'N':
            self.facing = 'E'
        elif self.facing == 'E':
            self.facing = 'S'
        elif self.facing == 'S':
            self.facing = 'W'
        elif self.facing == 'W':
            self.facing = 'N'
        return self._forward(location)
