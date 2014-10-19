'''
Created on Oct 18, 2014

@author: bjw
'''
import unittest
from model.turns import TurnList
from model.coordinates import CoordinateList

class TestCoordinateList(unittest.TestCase):


    def setUp(self):
        turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
        values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
        turnList = TurnList(turns, values)
        self.coordinates = turnList.toCoordinates()

    def testAppend(self):
        pass
    
    def testHasConflict(self):
        pass
    
    def testTopologicalNeighbors(self):
        pass
    
    def testCountTopologicalNeighbors(self):
        pass
    
    def testExtremes(self):
        pass
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()