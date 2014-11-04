from itertools import chain
from controller import loadDefaultData
from model.turns import TurnList
from model.population import Population
import montecarlo

class GeneticAlgorithm:
    """
        An iterator that implements the genetic algorithm 
        on a population of TurnList genes.
    """
    def __init__(self, sequenceOfValues, 
                 populationSize=100, 
                 generations=200,
                 elitePercent=.10, 
                 crossoverPercent=.80, 
                 mutationPercent=.25):
        self.sequenceOfValues   = sequenceOfValues                      # Values
        self.geneLength         = len(sequenceOfValues)                 # Length of a gene
        self.populationSize     = populationSize                        # Size of the Population
        self.generations        = generations                           # Number of generations to run.
        self.elitePercent       = elitePercent                          # Percent of genes to preserve as elite.
        self.crossoverPercent   = crossoverPercent                      # Percent of genes to crossover.
        self.mutationPercent    = mutationPercent                       # Percent of gene turns to mutate.
        
        self.currentPopulation  = Population(genes=[], fitness=[])      # Stores the current Population
        self.newPopulation      = Population(genes=[], fitness=[])      # Temporary Population used to construct next new population.

        self.elites             = Population(genes=[], fitness=[])      # The elites set aside while constructing the new population.
        self.nonElites          = Population(genes=[], fitness=[])      # The non-elites identified from the previous generation.
        # Crossed and Uncrossed have references to genes
        # from the previous generations - but they will be in their
        # mutated form.  Use these Population sets for access to
        # crossedover indexes and locations.
        self.crossed            = Population(genes=[], fitness=[])      # The genes which have been crossed over for the new generation.
        self.uncrossed          = Population(genes=[], fitness=[])      # The genes which where not crossed for the new generation.
        # Mutations is the final form of the current generation, minus the 
        # elites.  Use for the information about mutation locations.
        self.mutations          = Population(genes=[], fitness=[])      # The crossed and uncrossed genes combined for mutation.
        
        self.history            = []
    
    def __iter__(self):
        return self
    
    def next(self):
        """
            Performs the genetic algorithm on the previous population to construct
            a new population.
            @return: int  the current generation.
        """
        generation = len(self.history)
        # If this is the first iteration of the genetic algorithm,
        # a new, random population needs to be created.
        if len(self.history) == 0:
            self.initializeOriginalPopulation()
            self.history.append(self.currentPopulation.getGene(0))
            return generation
        # For >1 generations, perform the following steps:
        elif len(self.history) < self.generations:
            # Prepares an empty new population.
            self.newPopulation = Population(genes=[], fitness=[])

            # 1) Identify the elites.
            self.pullElites()
            # 2) Perform crossover on the non-elites.
            self.createCrossover()
            # 3) Perform mutations on the non-elites.
            self.createMutations()
            # 4) Construct a new population from the elites and non-elites.
            self.createNewPopulation()
            # 5) Assign the new population to the current population. 
            self.currentPopulation = self.newPopulation
            
            # Create a history of the highest scoring member of the
            # current population.
            self.history.append(self.currentPopulation.getGene(0))
            
            return generation
        else:
            raise StopIteration
    
    def initializeOriginalPopulation(self):
        """
            Creates an original population from the values provided
            to this GeneticAlgorithm. 
        """
        for __ in range(self.populationSize):
            valid = False
            while not valid: 
                # 1) Produce a sequence of turns using the MonteCarlo algorithm.
                sequenceOfTurns = montecarlo.getDefaultMCSequence(self.geneLength)
                # 2) Create a TurnList from the sequence of turns and
                #    their corresponding values.
                turnList = TurnList(sequenceOfTurns, self.sequenceOfValues)
                # 3) Determine if the sequence of turns is valid.
                if not turnList.toCoordinates().hasConflict():
                    self.currentPopulation.appendGene(turnList)
                    valid = True
    
    def pullElites(self):
        """
            Construct a set of elite members of the population and
            a set of non-elite members of the population.
        """
        numElites = int(self.populationSize * self.elitePercent)
        self.elites, self.nonElites = self.currentPopulation.splitElite(numElites)
    
    def createCrossover(self):
        """
            Apply Crossover to the non-elite members of the current
            population.
            NOTE: New instances of the genes are created.
        """
        numCrossovers = int(self.crossoverPercent * self.populationSize / 2 )
        #self.crossed, self.uncrossed = self.nonElites.createCrossoverPopulation(numCrossovers)
        self.crossed, self.uncrossed = self.nonElites.createCrossoverPopulationWithIncreaseAndCooling(numCrossovers, len(self.history))

    def createMutations(self):
        """
            Mutate members of the current population which have
            been set aside as non-elite.
            NOTE: crossed-over genes have their new instances mutated,
                  however the non-crossed-over non-elites will have
                  their original genes (those in the current population)
                  effected.
        """
        self.mutations = Population(genes=[], fitness=[])
        self.mutations.appendPopulation(self.crossed)
        self.mutations.appendPopulation(self.uncrossed)
        numMutations = (self.mutationPercent * self.mutations.size() * len(self.mutations.getGene(0)))
        #self.mutations.mutatePopulation(numMutations)
        self.mutations.mutatePopulationWithIncreaseAndCooling(numMutations, len(self.history))
        
    def createNewPopulation(self):
        """
            Combines the elite genes of the current generation
            with those non-elite genes which have been crossed over
            and mutated.  Stores them in a new population.
        """
        self.newPopulation = Population(genes=[], fitness=[])
        self.newPopulation.appendPopulation(self.elites)
        self.newPopulation.appendPopulation(self.mutations)
          
    def displayStateChanges(self):
        """
            A visually useful manner of inspecting the current generation of
            this Genetic Algorithm.
              * The first row references the indexes of the parents
                from which the current gene has been crossed-over.
              * The second row provides indexes for the genes of the current
                generation.  An "!" indicates the gene was produced from a crossover
                operation that did not complete successfully.  A "x" indicates
                that the gene was the product of a crossover operation.
              * The following rows indicate the turn state of the gene at a particular
                cell.  A turn surrounded by "<" and ">" indicates a cross-over location
                from the previous generation.  An "!" indicates a mutation created this cell.
              * The final row indicates the fitness of the gene.  A "*" indicates an elite
                gene that was carried over directly from the previous generation.
        """
        I = (len(str(self.populationSize-1)) * 2) + 1
        if I < 5:
            I = 5
        crossedGenes = self.crossed.crossedOverIndexes.keys()
        numElites = int(self.populationSize * self.elitePercent)
        results = "\n"
        #  Identify each gene's cross-over parents (if they had any). 
        for geneIndex in range(len(self.currentPopulation.genes)):
            if self.currentPopulation.genes[geneIndex] in crossedGenes:
                sourceIndexes = self.crossed.crossedOverIndexes[self.currentPopulation.genes[geneIndex]]
                results += str( str(sourceIndexes[0] + numElites) + "x" + str(sourceIndexes[1] + numElites) ).center(I) + "|"
            else:
                results += str(" " * I) + "|"
        results += '\n'
        #  Identify the gene's current index, whether it was the product of a crossover
        #  operation, and whether that crossover operation was "bad".
        for geneIndex in range(len(self.currentPopulation.genes)):
            badCross = False
            cross = False
            
            if self.currentPopulation.genes[geneIndex] in self.nonElites.cheapCrosses:
                badCross = True
            if self.currentPopulation.genes[geneIndex] in crossedGenes:
                cross = True
            
            placed = ""
            if badCross:
                placed += "!"
            placed += str(geneIndex)
            if cross:
                placed += "x"
            results += placed.center(I) + "|"
        results += '\n'
        #  A divider.
        for geneIndex in range(len(self.currentPopulation.genes)):
            results += str("-" * I) + "|"
        results += "\n"
        
        #  Displays rows for the cell values of each gene, indicating
        #  crossover points and mutations.
        for cellIndex in range(len(self.currentPopulation.genes[0])):
            for geneIndex in range(len(self.currentPopulation.genes)):
                currentGene = self.currentPopulation.genes[geneIndex]
                mutation = False
                crossed = False
                if (self.mutations.mutationLocations.has_key(currentGene) and
                    cellIndex in self.mutations.mutationLocations[currentGene]):
                    mutation = True
                if (currentGene in crossedGenes and 
                    self.crossed.crossedOverLocations[currentGene] == cellIndex):
                    crossed = True
                placed = ""
                if crossed:
                    placed += "<"
                placed += str(self.currentPopulation.genes[geneIndex].get(cellIndex)[0])
                if mutation:
                    placed += "!"
                if crossed:
                    placed += ">"
                results += placed.center(I) + "|"
            results += '\n'
        # Another divider.
        for geneIndex in range(len(self.currentPopulation.genes)):
            results += str("-" * I) + "|"
        results += "\n"
        
        # Display the fitness value for each gene, indicating whether the gene was elite
        # and carried directly from the previous generation.
        for geneIndex in range(len(self.currentPopulation.genes)):
            if self.currentPopulation.genes[geneIndex] in self.elites.genes:
                results += str(str(self.currentPopulation.fitness[geneIndex]) + "*").center(I) + "|"
            else:
                results += str(self.currentPopulation.fitness[geneIndex]).center(I) + "|"
        return results + '\n'        
        
if __name__ == '__main__':
    string2 = list("HHHPPHPHPHPPHPHPHPPH")
    string = list("pphpphhpphhppppphhhhhhhhhhpppppphhpphhpphpphhhhh".upper())
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P', 'P', 'P', 'H', 'P', 'P']
    ga = GeneticAlgorithm(string, populationSize=10, generations=200, 
                          elitePercent=.1, crossoverPercent=.85, mutationPercent=.05)
    for gen in ga:
        print "Generation: " + str(gen)
        print ga.displayStateChanges()
