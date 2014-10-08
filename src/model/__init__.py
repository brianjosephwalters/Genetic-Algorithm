from collections import deque

class TurnList:
    def __init__(self, turns=None, values=None):
        self.turns = deque()
        self.values = deque()
        if turns is not None:
            if values is None:
                print "Must provide values."
            if len(turns) != len(values):
                print "Require the same number of turns as values"
            for i in range(len(turns)):
                self.add(turns[i], values[i])
        
    def __len__(self):
        return len(self.turns)
        
    def __repr__(self):
        return str(self.turns)
        
    def add(self, turn, status):
        if turn == 'F' or turn == 'L' or turn == 'R':
            self.turns.append(turn)
            self.values.append(status)
    
    def get(self):
        return ( self.turns.popleft(), self.values.popleft() )
        
    def toCoordinates(self):
        coordinates = CoordinateList()
        for pair, value in PathWalker(self):
            coordinates.append(pair, value)
        return coordinates
        

"""
    An iterator to walk over a TurnList path.
    Given a TurnList: FLFFRRLFF
    Iteratively returns a series of coordinates such as
    (0,1), (-1,1), (-2,1), (-3,1), (-3,2), (-2,2), ...
    NOTE: (0,0) is _not_ the first coordinate
"""
class PathWalker:
    def __init__(self, path, start=(0,0), facing='N'):   
        self.location = start
        self.facing = facing
        self.path = path
    
    def __iter__(self):
        return self
    
    def next(self):
        if (len(self.path) == 0):
            raise StopIteration
        turn, value = self.path.get()
        #print "facing: " + self.facing + " turning: " + turn
        if   (turn == 'F'):
            self.location = self._forward()
        elif (turn == 'L'):
            self.location = self._turnLeft()
        elif (turn == 'R'):
            self.location = self._turnRight()
        else:
            print "Unexpected Path: " + turn
        return self.location, value

    def _forward(self):
        x, y = self.location
        if   self.facing == 'N':
            return (x,y+1)
        elif self.facing == 'E':
            return (x+1,y)
        elif self.facing == 'S':
            return (x,y-1)
        elif self.facing == 'W':
            return (x-1, y)
            
    
    def _turnLeft(self):
        if   self.facing == 'N':
            self.facing = 'W'
        elif self.facing == 'E':
            self.facing = 'N'
        elif self.facing == 'S':
            self.facing = 'E'
        elif self.facing == 'W':
            self.facing = 'S'
        return self._forward()
    
    def _turnRight(self):
        if   self.facing == 'N':
            self.facing = 'E'
        elif self.facing == 'E':
            self.facing = 'S'
        elif self.facing == 'S':
            self.facing = 'W'
        elif self.facing == 'W':
            self.facing = 'N'
        return self._forward()

class CoordinateList:
    def __init__(self):
        self.coordinates = []
        self.pairs = {}
        
    def __repr__(self):
        results = '['
        for c in self.coordinates:
            results += str(c) + ": " + str(self.pairs[c]) + ','
        results += ']'
        return results
        
    def append(self, pair, status):
        self.coordinates.append(pair)
        self.pairs[pair] = status
                
    def hasConflict(self):
        return len(self.coordinates) == len(set(self.coordinates))
    
    def topologicalNeighbors(self):
        neighbors = []
        for i in range(len(self.coordinates)):                          # For every pair of coordinates in the list...
            pair = self.coordinates[i]
            if self.pairs[pair] == 'H':                                 # If it is an 'H'
                north = (pair[0],   pair[1]+1)
                east  = (pair[0]+1, pair[1])
                south = (pair[0],   pair[1]-1)
                west  = (pair[0]-1, pair[1])
                for other in (north, east, south, west):               # For all of the neighbors...
                    if (self.pairs.has_key( other ) and                # Check if the other pair is on the map.
                        self.pairs[other] == 'H' and                   # Check if the other pair has a value of 'H'
                        other != self.coordinates[i-1] and             # Check if the other pair is connected on the path
                        other != self.coordinates[i+1] and
                        (pair, other) not in neighbors and             # Check if the pair has already been found.
                        (other, pair) not in neighbors):
                        neighbors.append( (pair, other) )
        return neighbors

    def countTopologicalNeighbors(self):
        return len(self.topologicalNeighbors())
        
        
if __name__ == '__main__':
    turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList = TurnList(turns, values)
        
    print turnList
    
    coordinates = turnList.toCoordinates()
    print coordinates
    
    print coordinates.topologicalNeighbors()
    print coordinates.countTopologicalNeighbors()
    
    
    