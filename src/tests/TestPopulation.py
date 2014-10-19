'''
Created on Oct 18, 2014

@author: bjw
'''
import unittest

from model.population import Population
from model.turns import TurnList

class TestPopulation(unittest.TestCase):


    def setUp(self):
        turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
        values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
        turnList = TurnList(turns, values)
        
        turns2 = ['R', 'L', 'L', 'F', 'L', 'F', 'R']
        values2 = ['H', 'P', 'H', 'P', 'H', 'H', 'P']
        turnList2 = TurnList(turns2, values2)
        
        self.pop1 = Population(turnList, turnList.calculateFitness())
        self.pop2 = Population(turnList2, turnList.calculateFitness())
        self.emptyPopulation = Population()

    def testAppendGene(self):
        pass
    
    def testAppendPopulation(self):
        pass
    
    def testGetGene(self):
        pass
    
    def testGetFitness(self):
        pass
    
    def testSize(self):
        pass
    
    def testGetDeepCopy(self):
        pass
    
    def testCreateCrossoverPopulation(self):
        pass
    
    def testMutatePopulation(self):
        pass
    
    def testSplitElite(self):
        pass
    
    def testSplitNonElite(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()