'''
Created on Oct 15, 2014

@author: bjw
'''
from collections import deque

from model.coordinates import CoordinateList
from model.walker import PathWalker

class TurnList:
    def __init__(self, turns=None, values=None):
        self.turns = []
        self.values = []
        if turns is not None:
            if values is None:
                print "Must provide values."
            if len(turns) != len(values):
                print "Require the same number of turns as values"
            for i in range(len(turns)):
                self.add(turns[i], values[i])

    def __len__(self):
        return self.size()

    def __repr__(self):
        string = "<"
        for index in range(len(self.turns)):
            string += str(self.turns[index]) + ", "
        return string + ">"
    
    def asString(self):
        return ''.join(self.turns).upper()

    def add(self, turn, status):
        if turn == 'F' or turn == 'L' or turn == 'R':
            self.turns.append(turn)
            self.values.append(status)

    def get(self, index):
        return self.turns[index], self.values[index]
    
    def getTurn(self, index):
        return self.turns[index]
    
    def set(self, index, turn, status):
        if turn == 'F' or turn == 'L' or turn == 'R':
            self.turns[index] = turn
            self.values[index] = status
            
    def setTurn(self, index, turn):
        if turn == 'F' or turn == 'L' or turn == 'R':
            self.turns[index] = turn
    
    def size(self):
        return len(self.turns)

    def split(self, index):
        firstTurns = self.turns[:index]
        firstValues =  self.values[:index]
        first = TurnList(firstTurns, firstValues)
        lastTurns = self.turns[index:]
        lastValues = self.values[index:]
        last = TurnList(lastTurns, lastValues)
        return first, last
    
    def join(self, other):
        self.turns.extend(other.turns)
        self.values.extend(other.values)
    
    def calculateFitness(self):
        return self.toCoordinates().countTopologicalNeighbors()

    def hasConflict(self):
        return self.toCoordinates().hasConflict()

    def toCoordinates(self):
        walker = PathWalker(self)
        return walker.walk()
    
if __name__ == '__main__':
    turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList = TurnList(turns, values)
    print turnList
    print turnList.hasConflict()
    
    turns2 = ['R', 'F', 'R', 'R', 'L', 'F', 'R']
    values2 = ['H', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList2 = TurnList(turns2, values2)
    print turnList2
    
    turnList.join(turnList2)
    print turnList
    
    print turnList2.split(3)
    print turnList.split(10)
    
    print turnList
    print turnList.hasConflict()
    print turnList.toCoordinates()
    print turnList2.hasConflict()
    
    