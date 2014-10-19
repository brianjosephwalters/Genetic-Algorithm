from controller import loadDefaultData
from model.turns import TurnList
from model.population import Population
import montecarlo

class GeneticAlgorithm:
    def __init__(self, sequenceOfValues, 
                 populationSize=50, generations=200,
                 elitePercent=.10, crossoverPercent=.80, mutationPercent=.25):
        self.sequenceOfValues = sequenceOfValues
        self.geneLength = len(sequenceOfValues)
        self.populationSize = populationSize
        self.generations = generations
        self.elitePercent = elitePercent
        self.crossoverPercent = crossoverPercent
        self.mutationPercent = mutationPercent
        
        self.currentPopulation = Population(genes=[], fitness=[])
        self.newPopulation = Population(genes=[], fitness=[])
        
        self.history = []
    
    def __iter__(self):
        return self
    
    def next(self):
        if len(self.history) == 0:
            self.initializeNewPopulation()
            print "Initial Population Created"
            print "   Add to History: " + str(self.currentPopulation.getGene(0))
            print "   Added class: " + str(self.currentPopulation.getGene(0).__class__)
            self.history.append(self.currentPopulation.getGene(0))
            return len(self.history) - 1
        elif len(self.history) < self.generations:
            print "Generation: " + str(len(self.history))
            self.pullElites()
            print "  size: " + str(self.newPopulation.size())
            print "  elites pulled..."
            self.applyCrossOverAndMutate()
            print "  size: " + str(self.newPopulation.size())
            print "  crossed-over and mutated..."
            self.currentPopulation = self.newPopulation
            print "  best for generation:"
            print self.currentPopulation.getGene(0)
            print "   Create History: " + str(self.currentPopulation.getGene(0))
            print "   History class: " + str(self.currentPopulation.getGene(0).__class__)
            self.history.append(self.currentPopulation.getGene(0))
            self.newPopulation = Population(genes=[], fitness=[])
            return len(self.history) - 1
        else:
            raise StopIteration
    
    def initializeNewPopulation(self):
        for _ in range(self.populationSize):
            valid = False
            while not valid: 
                sequenceOfTurns = montecarlo.getDefaultMCSequence(self.geneLength)
                turnList = TurnList(sequenceOfTurns, self.sequenceOfValues)
                if not turnList.toCoordinates().hasConflict():
                    self.currentPopulation.appendGene(turnList)
                    valid = True
    
    def pullElites(self):
        numElites = int(self.populationSize * self.elitePercent)
        print "  NumElites: " + str(numElites)
        elites = self.currentPopulation.splitElite(numElites)
        print "  Elites count: " + str(elites.size())
        print "  CurrentPop Size: " + str(self.currentPopulation.size())
        self.newPopulation.appendPopulation(elites)
        print "  NewPop after elites: " + str(self.newPopulation.size())
    
    def applyCrossOverAndMutate(self):
        numCrossovers = int(self.crossoverPercent * self.populationSize / 2 )
        print "    Current Population Size: " + str(self.currentPopulation.size())
        crossed, uncrossed = self.currentPopulation.createCrossoverPopulation(numCrossovers)
        print "    Crossed Size: " + str(crossed.size()) + " Uncrossed Size: " + str(uncrossed.size())
        crossed.appendPopulation(uncrossed)
        numMutations = (self.mutationPercent * crossed.size() * len(crossed.getGene(0)))
        crossed.mutatePopulation(numMutations)
        self.newPopulation.appendPopulation(crossed)
        
    def run(self):
        self.initializeNewPopulation()
        self.history.append(self.currentPopulation)
        for i in range(self.generations):
            self.pullElites()
            self.applyCrossOverAndMutate()
            self.currentPopulation = self.newPopulation
            self.history.append(self.newPopulation.getGene(0))
            self.newPopulation = Population(genes=[], fitness=[])
        
if __name__ == '__main__':
    string = "pphpphhpphhppppphhhhhhhhhhpppppphhpphhpphpphhhhh"
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P', 'P', 'P', 'H', 'P', 'P']
    ga = GeneticAlgorithm(values, populationSize=10, generations=10)
    for gen in ga:
        print ga.history[gen]
    