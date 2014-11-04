'''
Created on Oct 01, 2014

@author: bjw
'''
import unittest
from model.turns import TurnList

class TestTurnList(unittest.TestCase):


    def setUp(self):
        turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
        values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
        self.turnList = TurnList(turns, values)
        
        turns2 = ['R', 'F', 'R', 'L', 'L', 'R', 'L']
        values2 = ['H', 'P', 'H', 'P', 'H', 'H', 'P']
        self.turnList2 = TurnList(turns2, values2)

    def tearDown(self):
        pass

    def testAdd(self):
        self.turnList.add('L', 'P')
        turn = self.turnList.get(7)
        self.assertEquals(turn[0], 'L')
        self.assertEquals(turn[1], 'P')

    def testGet(self):
        turn = self.turnList.get(3)
        self.assertEquals(turn[0], 'F')
        self.assertEquals(turn[1], 'P')
        
    def testGetTurn(self):
        turn = self.turnList.getTurn(3)
        self.assertEquals(turn, 'F')
    
    def testSet(self):
        turn = self.turnList.get(2)
        self.assertEquals(turn[0], 'L')
        self.assertEquals(turn[1], 'H')
        self.turnList.set(2, 'F', 'P')
        turn = self.turnList.get(2)
        self.assertEquals(turn[0], 'F')
        self.assertEquals(turn[1], 'P')
    
    def testSetTurn(self):
        turn = self.turnList.get(2)
        self.assertEquals(turn[0], 'L')
        self.assertEquals(turn[1], 'H')
        self.turnList.setTurn(2, 'F')
        turn = self.turnList.get(2)
        self.assertEquals(turn[0], 'F')
        self.assertEquals(turn[1], 'H')
    
    def testSplit(self):
        first, second = self.turnList.split(3)
        self.assertTrue(first.size() == 3)
        self.assertTrue(second.size() == 4)
        self.assertEquals(first.get(0)[0], 'F')
        self.assertEquals(first.get(0)[1], 'P')
        self.assertEquals(first.get(2)[0], 'L')
        self.assertEquals(first.get(2)[1], 'H')
        self.assertEquals(second.get(0)[0], 'F')
        self.assertEquals(second.get(0)[1], 'P')
        self.assertEquals(second.get(3)[0], 'R')
        self.assertEquals(second.get(3)[1], 'P')
    
    def testJoin(self):
        self.turnList.join(self.turnList)
        self.assertTrue(self.turnList.size() == 14)
        self.assertEquals(self.turnList.get(0), self.turnList.get(7))
        self.assertEquals(self.turnList.get(6), self.turnList.get(13))
        
    def testCross(self):
        one, two = self.turnList.cross(self.turnList2, 3)
        self.assertEquals(str(one), "<F, L, L, L, L, R, L, >")
        self.assertEquals(str(two), "<R, F, R, F, R, F, R, >")
        # Crossing at 0 should produce no cross.
        one, two = self.turnList.cross(self.turnList2, 0)
        self.assertEquals(str(one), "<R, F, R, L, L, R, L, >")
        self.assertEquals(str(two), "<F, L, L, F, R, F, R, >")
        # Crossing at len() - 1 should cross the last cell in the genes
        one, two = self.turnList.cross(self.turnList2, len(self.turnList2) - 1)
        self.assertEquals(str(one), "<F, L, L, F, R, F, L, >")
        self.assertEquals(str(two), "<R, F, R, L, L, R, R, >")
        
    
    def testCalculateFitness(self):
        self.assertEquals(self.turnList.calculateFitness(), 0)
        self.assertEquals(self.turnList.hasConflict(), 
                          self.turnList.toCoordinates().hasConflict())
        
    
    def testHasConflict(self):
        self.assertFalse(self.turnList.hasConflict())
    
    def testToCoordinates(self):
        coor = self.turnList.toCoordinates()
        self.assertEquals(len(coor.coordinates), self.turnList.size())
        self.assertEquals(coor.coordinates[0], (0,1))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()