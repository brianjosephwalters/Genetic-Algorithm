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
        self.turnList1 = TurnList(turns, values)
        
        turns2 = ['R', 'L', 'L', 'F', 'L', 'F', 'R']
        values2 = ['H', 'P', 'H', 'P', 'H', 'H', 'P']
        self.turnList2 = TurnList(turns2, values2)
        
        turns3 = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
        values3 = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
        self.turnList3 = TurnList(turns3, values3)
        
        bigValues1 = list("PPHPPHHPPHHPPPPPHHHHHHHHHHPPPPPPHHPPHHPPHPPHHHHH")
        bigTurns1 = list("FRFRLFLFRFLFFRLFLRRLLRRFRFLFRLLRFRLFLFRLFFFFRLLF")
        self.bigTL1 = TurnList(bigTurns1, bigValues1)
        
        bigValues2 = list("PPHPPHHPPHHPPPPPHHHHHHHHHHPPPPPPHHPPHHPPHPPHHHHH")
        bigTurns2 = list("FRFRLFLFRFLFFRLFLRRLLRRFRFLFRLLRFRLFLFRLFFFFRLLF")
        self.bigTL2 = TurnList(bigTurns2, bigValues2)
        
        self.pop1 = Population([self.turnList1], [self.turnList1.calculateFitness()])
        self.pop2 = Population([self.turnList2], [self.turnList2.calculateFitness()])
        self.pop3 = Population([self.turnList3], [self.turnList3.calculateFitness()])
        self.bigPop1 = Population([self.bigTL1], [self.bigTL1.calculateFitness()])
        self.bigPop2 = Population([self.bigTL2], [self.bigTL2.calculateFitness()])
        self.emptyPopulation = Population()

    def testAppendGene(self):
        self.pop1.appendGene(self.turnList2)
        self.assertEquals(self.pop1.getGene(1), self.turnList2)
        self.pop2.appendGene(self.turnList1)
        self.assertEquals(self.pop2.getGene(1), self.turnList1)
        self.pop2.appendGene(self.turnList1)
    
    def testAppendPopulation(self):
        self.pop1.appendPopulation(self.pop2)
        self.assertEquals(self.pop1.getGene(1), self.turnList2)
        self.assertTrue(self.pop1.size() == 2)
        self.pop2.appendPopulation(self.pop1)
        self.assertEquals(self.pop2.getGene(1), self.turnList1)
        self.assertEquals(self.pop2.getGene(2), self.turnList2)
        self.assertTrue(self.pop2.size() == 3)
        # Since these are pass-by-reference, updates to one member of the population
        # can result in updates to different members of the population.
        self.pop2.appendPopulation(self.pop2)
        self.pop2.getGene(2).setTurn(0, 'L')
            
    def testGetGene(self):
        self.assertEquals(self.pop1.getGene(0), self.turnList1)
        self.assertEquals(self.pop2.getGene(0), self.turnList2)
    
    def testGetFitness(self):
        self.assertEquals(self.pop1.getFitness(0), self.turnList1.calculateFitness())
        self.assertEquals(self.pop2.getFitness(0), self.turnList2.calculateFitness())
    
    def testSize(self):
        self.assertEquals(self.pop1.size(), 1)
        self.assertEquals(self.pop2.size(), 1)
        
    def testMutatatePopulationWithIncreaseAndCooling(self):
        print "Ensure advanced mutation algorithm is increase fitness faster than simple mutations."
        print "{:10s} {:10s}".format("Normal", "Advanced")
        for gen in range(100):
            self.bigPop1.mutatePopulation(1)
            self.bigPop2.mutatePopulationWithIncreaseAndCooling(1, gen)
            print "{:10d} {:10d}".format(self.bigPop1.getFitness(0), self.bigPop2.getFitness(0))
        self.assertTrue(self.bigPop1.getFitness(0) <= self.bigPop2.getFitness(0))
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()