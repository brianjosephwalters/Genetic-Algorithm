'''
Created on Oct 17, 2014

@author: bjw
'''
import random, copy
class Population:
    def __init__(self, genes=[], fitness=[]):
        self.genes = genes
        self.fitness = fitness
        
        self.eliteIndexes = []
        self.crossedOverIndexes = []
        
    def __repr__(self):
        results = "\n"
        if len(self.genes) > 0:
            for geneIndex in range(len(self.genes)):
                results += str(geneIndex) + "| "
            results += '\n'
            for cellIndex in range(len(self.genes[0])):
                for geneIndex in range(len(self.genes)):
                    results += self.genes[geneIndex].get(cellIndex)[0] + "| "
                results += '\n'
            for geneIndex in range(len(self.genes)):
                results += str(self.fitness[geneIndex]) + "| "
        return results + '\n'
        
    def appendGene(self, gene, fitness=None):
        self.genes.append(gene)
        if fitness is None:
            self.fitness.append(gene.calculateFitness())
        else:
            self.fitness.append(fitness)
            
    def removeGene(self, geneIndex):
        self.genes.pop(geneIndex)
        self.fitness.pop(geneIndex)
        
    def appendPopulation(self, population):
        for index in range(population.size()):
            gene = population.getGene(index)
            fitness = population.getFitness(index)
            self.appendGene(gene, fitness)
                
    def getGene(self, geneIndex):
        return self.genes[geneIndex]
    
    def getFitness(self, geneIndex):
        return self.fitness[geneIndex]
    
    def size(self):
        return len(self.genes)
    
    def getDeepCopy(self):
        return copy.deepcopy(self)
    
    def createCrossoverPopulation(self, numCrossOvers):
        crossPopulation = Population(genes=[], fitness=[])
        choices = range(self.size())
        tries = 0
        while crossPopulation.size() < (numCrossOvers * 2):
            tries += 1
            geneIndexes = random.sample(choices, 2)
            gene1, gene2 = self._createCrossover(geneIndexes)
            if not gene1.hasConflict() and not gene2.hasConflict():
                choices.remove(geneIndexes[0])
                choices.remove(geneIndexes[1])
                crossPopulation.appendGene(gene1, gene1.calculateFitness())
                crossPopulation.appendGene(gene2, gene2.calculateFitness())
            if tries > 100:
                indexA = max(geneIndexes)
                indexB = min(geneIndexes)
                geneA = self.genes[indexA]
                geneB= self.genes[indexB]
                
                crossPopulation.appendGene(geneA, geneA.calculateFitness())
                crossPopulation.appendGene(geneB, geneB.calculateFitness())
                choices.remove(indexA)
                choices.remove(indexB)
        
        uncrossedPopulation = Population(genes=[], fitness=[])
        for index in choices:
            gene = self.genes[index]
            uncrossedPopulation.appendGene(gene, gene.calculateFitness())
        return crossPopulation, uncrossedPopulation
    
    def _createCrossover(self, geneIndexes):
        splitIndex = random.randint(0, len(self.genes[0]))
        first, second = self.genes[geneIndexes[0]].split(splitIndex)
        third, fourth = self.genes[geneIndexes[1]].split(splitIndex)
        first.join(fourth)
        third.join(second)
        return first, third
    
    def mutatePopulation(self, numMutations):
        for _ in range(int(numMutations)):
            valid = False
            while not valid:
                geneIndex = random.randrange(len(self.genes))
                turnIndex = random.randrange(len(self.genes[geneIndex]))
                oldTurn = self.genes[geneIndex].get(turnIndex)[0]
                turnList = ['F', 'L', 'R']
                turnList.remove(oldTurn)
                newTurn = random.choice(turnList)
                self.genes[geneIndex].setTurn(turnIndex, newTurn)
                if not self.genes[geneIndex].hasConflict():
                    self.fitness[geneIndex] = self.genes[geneIndex].calculateFitness()
                    valid = True
                else:
                    #print "mutating..."
                    self.genes[geneIndex].setTurn(turnIndex, oldTurn)
    
    def splitElite(self, numElite):
        indexList = self._getEliteIndexes(numElite)
        elitePopulation = Population(genes=[], fitness=[])
        for index in indexList:
            if self.genes[index].hasConflict():
                print "========Elite gene " + str(index) + " has a conflict!==========="
            elitePopulation.appendGene(self.genes[index], self.fitness[index])
            self.removeGene(index)
        return elitePopulation
        
    def splitNonElite(self, numElite):
        eliteIndexList = self._getEliteIndexes(numElite)
        nonEliteIndexList = [i for i in range(len(self.genes)) if i not in eliteIndexList]
        nonElitePopulation = Population(genes=[], fitness=[])
        for index in nonEliteIndexList:
            nonElitePopulation.appendGene(self.genes[index], self.fitness[index])
        return nonElitePopulation
    
    def _getEliteIndexes(self, count):
        indexList = []
        while (len(indexList) < count):
            highestValue = self.fitness[0]
            highestIndex = 0
            for i in range(len(self.genes)):
                if self.fitness[i] > highestValue and i not in indexList:
                    highestValue = self.fitness[i]
                    highestIndex = i
            indexList.append(highestIndex)
        return indexList


if __name__ == '__main__':
    from model.turns import TurnList
    turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList = TurnList(turns, values)
    
    turns2 = ['R', 'L', 'L', 'F', 'L', 'F', 'R']
    values2 = ['H', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList2 = TurnList(turns2, values2)
    
    values3 = list("pphpphhpphhppppphhhhhhhhhhpppppphhpphhpphpphhhhh".upper())
    turns3 = ['L', 'F', 'F', 'L', 'L', 'L', 'L', 'F', 'L', 'L', 'L', 'R', 'L', 'R', 'F', 'F', 
              'F', 'L', 'F', 'R', 'F', 'F', 'R', 'L', 'R', 'L', 'F', 'F', 'F', 'R', 'L', 'L', 
              'R', 'L', 'F', 'F', 'R', 'R', 'L', 'F', 'R', 'F', 'L', 'F', 'F', 'F', 'R', 'R']
    turnList3 = TurnList(turns3, values3)
    print "Does it have a conflict? " + str(turnList3.hasConflict())
    
    population = Population(genes=[],fitness=[])
    population.appendGene(turnList, turnList.calculateFitness())
    population.appendGene(turnList2, turnList2.calculateFitness())
    print "Population1"
    print population
#     print "Population2"
#     population2 = population.getDeepCopy()
#     population2.mutatePopulation(4)
#     print population2
    
#     crossPop = population.createCrossOverPopulation(1)
#     print 'CrossPop\n'
#     print crossPop
#     print 'Population\n'
#     print population
#     
#     elitePop = population.splitElite(1)
#     print elitePop
#     population.appendPopulation(elitePop)
#     print population
    
