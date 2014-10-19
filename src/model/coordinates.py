'''
Created on Oct 10, 2014

@author: bjw
'''

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
        return len(self.coordinates) != len(set(self.coordinates))
    
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
                        i - 1 > 0 and                                  # Check if the other pair is connected on the path
                        other != self.coordinates[i-1] and             
                        i + 1 < len(self.coordinates) and
                        other != self.coordinates[i+1] and
                        (pair, other) not in neighbors and             # Check if the pair has already been found.
                        (other, pair) not in neighbors):
                        neighbors.append( (pair, other) )
        return neighbors

    def extremes(self):
        minX = 0
        minY = 0
        maxX = 0
        maxY = 0
        for pair in self.pairs:
            #print pair
            if pair[0] > maxX:
                maxX = pair[0]
            if pair[0] < minX:
                minX = pair[0]
            if pair[1] > maxY:
                maxY = pair[1]
            if pair[1] < minY:
                minY = pair[1]
        return (minX, maxX, minY, maxY)        

    def countTopologicalNeighbors(self):
        return len(self.topologicalNeighbors())

if __name__ == '__main__':
    from model.turns import TurnList
    turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList = TurnList(turns, values)
        
    print turnList
    
    coordinates = turnList.toCoordinates()
    print coordinates
    print turnList
    print turnList.hasConflict()
    print coordinates.hasConflict()
    print coordinates.topologicalNeighbors()
    print coordinates.countTopologicalNeighbors()
    print coordinates.extremes()
    
    
    