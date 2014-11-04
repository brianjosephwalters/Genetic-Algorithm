'''
Created on Oct 17, 2014

@author: bjw
'''
import random, copy, math

from montecarlo import MonteCarlo

class Population:
    def __init__(self, genes=[], fitness=[]):
        """
            Initializes a new instance of a Population.
        """
        self.genes = genes                  # The genes of the population.
        self.fitness = fitness              # The fitness values corresponding to each gene
                                            #   in the population
        
        # Data used by particular kinds of population sets.
        self.crossedOverIndexes = {}        # Cross-over indexes
        self.crossedOverLocations = {}      # Cross-over locations
        self.mutationLocations = {}         # Mutation locations
        self.cheapCrosses = []              # A list of indexes where "bad" crossovers occurred.
        
    def __repr__(self):
        """
            A quick and dirty columnar representation of the population.
        """
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
    ### Queries
    def getGene(self, geneIndex):
        """
            Returns the gene at the provided index.
        """
        return self.genes[geneIndex]
    
    def getFitness(self, geneIndex):
        """
            Returns the fitness value for the gene
            at the provided index.
        """
        return self.fitness[geneIndex]
    
    def size(self):
        """
            Returns the number of genes in the population.
        """
        return len(self.genes)

    def indexesSortedByFitness(self):
        """
            Return a list of indexes for the genes in this population,
            sorted by their fitness.
        """
        return sorted(range(len(self.fitness)), key=lambda k:self.fitness[k], reverse=True)
    
    def splitElite(self, numElite):
        """
            Returns populations of the Elite genes and Non-Elite genes
            from this population.
        """
        # Create two new empty populations to store the results.
        one = Population(genes=[], fitness=[])
        two = Population(genes=[], fitness=[])
        
        # Get a list of the gene indexes in this population, sorted by fitness.
        indexes = self.indexesSortedByFitness()
        
        # Split the list of indexes into two sets - elite and non-elite
        eliteIndexes = indexes[:numElite]
        theRest = indexes[numElite:]
        
        # Populate the corresponding sets of elite and non-elite populations.
        for index in eliteIndexes:
            one.appendGene(self.genes[index], self.fitness[index])
        for index in theRest:
            two.appendGene(self.genes[index], self.fitness[index])
        return one, two
    
    def createCrossoverPopulation(self, numCrossovers):
        """ 
            Constructs a new Population containing the
            crossed-over genes from this Population.
        """
        crossPopulation = Population(genes=[], fitness=[])
        # Create a list of indexes for the genes of this population. 
        choices = range(self.size())
        tries = 0
        while crossPopulation.size() < (numCrossovers * 2):
            tries += 1
            # Get some genes to cross over by selecting from the list of indexes.
            geneIndexes = random.sample(choices, 2)
            gene1 = self.getGene(geneIndexes[0])
            gene2 = self.getGene(geneIndexes[1])
            # Get a random location on the genes at which to split.
            splitIndex = random.randint(0, len(self.genes[0]))
            # Create two new genes by crossing the selected ones at the specified index.
            first, second = gene1.cross(gene2, splitIndex)
            # Ensure that the crossed-over genes are valid genes.
            if (not first.hasConflict() and not second.hasConflict()):
                # Remove the genes we used to cross from the list of available
                # genes.
                choices.remove(geneIndexes[0])
                choices.remove(geneIndexes[1])
                # Add the successfully crossed genes to the new population.
                crossPopulation.appendGene(first, first.calculateFitness())
                crossPopulation.appendGene(second, second.calculateFitness())
                # Store some information about this process.
                crossPopulation.crossedOverIndexes[first] = geneIndexes         #MEMO 
                crossPopulation.crossedOverIndexes[second] = geneIndexes        #MEMO
                crossPopulation.crossedOverLocations[first] = splitIndex        #MEMO
                crossPopulation.crossedOverLocations[second] = splitIndex       #MEMO
            # If we are unable to produce a valid set of crossed-over genes
            # then fail "gracefully" by simply moving the genes on to the 
            # next generation.
            if tries > 100:
                # Get the highest and lowest index from the list of genes
                indexA = max(choices)
                indexB = min(choices)
                # Get those genes.
                geneA = self.genes[indexA]
                geneB = self.genes[indexB]
                # Add them to the new population.
                crossPopulation.appendGene(geneA, geneA.calculateFitness())
                crossPopulation.appendGene(geneB, geneB.calculateFitness())
                # Remove their indexes from the list of gene indexes
                choices.remove(indexA)
                choices.remove(indexB)
                #Store some information about this process.
                self.cheapCrosses.append(geneA)                                 #MEMO
                self.cheapCrosses.append(geneB)                                 #MEMO
        
        # Once crossover is complete, we want to store the uncrossed genes
        # in a population as well.
        uncrossedPopulation = Population(genes=[], fitness=[])
        # For any index that hasn't been removed as from crossover, move the
        # corresponding gene to the uncrossed population.
        for index in choices:
            gene = self.genes[index]
            uncrossedPopulation.appendGene(gene, gene.calculateFitness())
        
        return crossPopulation, uncrossedPopulation
    
    def chooseParentUsingFitness(self, choices):
        """
            Chooses a parent from a set of choices, using fitness to 
            effect the probability of choosing that parent.
        """
        # This should probably use something more like laplace smoothing. 
        # Right now, it only checks to ensure that the total probability is not 
        # zero.  But we should probably be using Laplace smoothing to ensure that
        # zero fitness scores have a (small) chance of being selected.  This is
        # only really important for the first few generations, whether there
        # are genes with zero fitness.
        totalFitness = sum([self.fitness[i] for i in choices])
        if totalFitness > 0:
            probOfChoices = [float(self.fitness[i])/float(totalFitness) for i in choices]
        else:   
            probOfChoices = [1/float(len(choices)) for i in choices]
            
        mc = MonteCarlo(choices, probOfChoices)
        return mc.getWeightedSelection()

    def chooseParentsUsingFitness(self, choices):
        """
            Chooses two parents from a set of choices.  Probabilities are
            readjusted after each parent is selected.
        """
        index1 = self.chooseParentUsingFitness(choices)
        newChoices = [i for i in choices if i != index1]
        index2 = self.chooseParentUsingFitness(newChoices)
        return index1, index2
        
    def createCrossoverPopulationWithIncreaseAndCooling(self, numCrossovers, generation):
        """
            Constructs a new Population containing the crossed-over genes from this Population.
            This algorithm uses a fitness and cooling standard to the crossed-over genes, as
            discussed in Halm, 2007.
        """
        crossPopulation = Population(genes=[], fitness=[])
        # Create a list of indexes for the genes of this population.
        choices = range(self.size())    #  A list of indexes available for crossover
        cooling = .3                    #  Initial cooling value
        cooling_rate = .99              #  Cooling rate
        tries = 0                       #  Number of tries before stop trying to crossover.
        while (crossPopulation.size() < (numCrossovers * 2) and
               len(choices) > 1):
            tries += 1
            accept = False
            # Get two parents and apply crossover to produce two children.
            parentIndex1, parentIndex2 = self.chooseParentsUsingFitness(choices)
            parent1, parent1Fitness = self.getGene(parentIndex1), self.getFitness(parentIndex1)
            parent2, parent2Fitness = self.getGene(parentIndex2), self.getFitness(parentIndex2)
            splitIndex = random.randint(0, len(self.genes[0]))
            first, second = parent1.cross(parent2, splitIndex)
            # Ensure there is no conflict with the children, otherwise try again.
            if not first.hasConflict() and not second.hasConflict():
                firstFitness = first.calculateFitness()
                secondFitness = second.calculateFitness()
                averageParentFitness = (parent1Fitness + parent2Fitness) / 2
                # Accept if the fitness of the children is better than the average fitness
                # of the two parents.
                if ( ( firstFitness >= averageParentFitness) and
                     ( secondFitness >= averageParentFitness)    ):
                    accept = True
                
                # Otherwise, accept randomly based on a cooled relation between the 
                # parent and child's fitnesses.
                randomNumber = random.random()
                c = (cooling * cooling_rate) * (generation+1 / 5)
                if ( ( randomNumber < math.exp(firstFitness - averageParentFitness) / c) and
                     ( randomNumber < math.exp(secondFitness - averageParentFitness) / c)    ):
                    accept = True

            if accept:
                # Finalize the crossover in the new population.
                choices.remove(parentIndex1)
                choices.remove(parentIndex2)
                crossPopulation.appendGene(first, first.calculateFitness())
                crossPopulation.appendGene(second, second.calculateFitness())
                # Store some information about this process.
                crossPopulation.crossedOverIndexes[first] = (parentIndex1, parentIndex2)        #MEMO 
                crossPopulation.crossedOverIndexes[second] = (parentIndex1, parentIndex2)       #MEMO
                crossPopulation.crossedOverLocations[first] = splitIndex                        #MEMO
                crossPopulation.crossedOverLocations[second] = splitIndex                       #MEMO
            # If we are unable to produce a valid set of crossed-over genes
            # then fail "gracefully" by simply moving the genes on to the 
            # next generation.
            if not accept and tries > 1000:
                print "HERE!"
                # Get the highest and lowest index from the list of genes
                indexA = max(choices)
                geneA = self.genes[indexA]
                choices.remove(indexA)
                
                indexB = min(choices)
                geneB = self.genes[indexB]
                choices.remove(indexB)
                
                # Add them to the new population.
                crossPopulation.appendGene(geneA, geneA.calculateFitness())
                crossPopulation.appendGene(geneB, geneB.calculateFitness())                
                
                #Store some information about this process.
                self.cheapCrosses.append(geneA)                                 #MEMO
                self.cheapCrosses.append(geneB)                                 #MEMO
        
        # Once crossover is complete, we want to store the uncrossed genes
        # in a population as well.
        uncrossedPopulation = Population(genes=[], fitness=[])
        # For any index that hasn't been removed as from crossover, move the
        # corresponding gene to the uncrossed population.
        for index in choices:
            gene = self.genes[index]
            uncrossedPopulation.appendGene(gene, gene.calculateFitness())
        
        return crossPopulation, uncrossedPopulation
    
    ### Commands ##########################################################
    def appendGene(self, gene, fitness=None):
        """
            Appends a gene to the current population
            NOTE: Use rather than direct assignment in order to ensure
                  a fitness value is calculated at the corresponding index.
        """
        self.genes.append(gene)
        if fitness is None:
            self.fitness.append(gene.calculateFitness())
        else:
            self.fitness.append(fitness)
            
    def removeGene(self, geneIndex):
        """
            Removes a gene and its fitness value from
            the population.
        """
        self.genes.pop(geneIndex)
        self.fitness.pop(geneIndex)
        
    def appendPopulation(self, population):
        """
            Append a population to the end of this population.
            Ensures that genes and fitness values correspond.
        """
        for index in range(population.size()):
            gene = population.getGene(index)
            fitness = population.getFitness(index)
            self.appendGene(gene, fitness)
    
    def getRandomDirection(self, oldTurn):
        # Identify a new state for the cell.
        turnList = ['F', 'L', 'R']
        turnList.remove(oldTurn)
        return random.choice(turnList)

        
    def mutatePopulation(self, numMutations):
        """
            Mutate the current population in place.
        """
        for _ in range(int(numMutations)):
            valid = False
            while not valid:
                # Get a random gene.
                geneIndex = random.randrange(len(self.genes))
                # Get a random cell on the gene
                turnIndex = random.randrange(len(self.genes[geneIndex]))
                # Store the current state of the cell.
                oldTurn = self.genes[geneIndex].getTurn(turnIndex)
                # Get new state for cell.
                newTurn = self.getRandomDirection(oldTurn)
                # Assign that new state to the cell.
                self.genes[geneIndex].setTurn(turnIndex, newTurn)
                
                # Check to see if the new state of the gene is a valid one.
                if not self.genes[geneIndex].hasConflict():
                    # If so, calculate the new fitness value for the new gene.
                    self.fitness[geneIndex] = self.genes[geneIndex].calculateFitness()
                    # And acknowledge the mutation.
                    valid = True
                    # Store some information about this process.
                    if self.mutationLocations.has_key(self.genes[geneIndex]):
                        self.mutationLocations[self.genes[geneIndex]].append(turnIndex)     #MEMO
                    else:
                        self.mutationLocations[self.genes[geneIndex]] = [turnIndex]         #MEMO
                else:
                    # If the new configuration was not valid, reset the gene
                    # to its previous state.
                    self.genes[geneIndex].setTurn(turnIndex, oldTurn)
    
    def mutatePopulationWithIncreaseAndCooling(self, numMutations, generation):
        """
            Mutate the current population in place.  This algorithm uses both a fitness
            and cooling standard, as discussed in Halm, 2007.
        """
        cooling = 2.0
        cooling_rate = .97
        for _ in range(int(numMutations)):
            # Get a gene for mutation
            geneIndex = random.randrange(len(self.genes))
            gene = self.genes[geneIndex]
            fitness = self.fitness[geneIndex]
            accept = False
            while not accept:
                # Choose a cell index
                turnIndex = random.randrange(gene.size())
                # Change directions
                oldTurn = gene.getTurn(turnIndex)
                newTurn = self.getRandomDirection(oldTurn)
                gene.setTurn(turnIndex, newTurn)
                # Check for conflicts
                if not gene.hasConflict():
                    # calculate new fitness
                    newFitness = gene.calculateFitness()
                    # Accept if new Fitness is better than or equals to old Fitness
                    if newFitness >= fitness:
                        self.genes[geneIndex] = gene
                        self.fitness[geneIndex] = newFitness
                        accept = True
                    # Accept if new Fitness is worse, but meets a random test (with cooling).
                    
                    else:
                        randomNumber = random.random()
                        c = (cooling * cooling_rate) * (generation+1 / 5)
                        if randomNumber < math.exp(newFitness - fitness) / c:
                            self.genes[geneIndex] = gene
                            self.fitness[geneIndex] = newFitness
                            accept = True
                if accept:
                    # Store some information about this process.
                    if self.mutationLocations.has_key(self.genes[geneIndex]):
                        self.mutationLocations[self.genes[geneIndex]].append(turnIndex)     #MEMO
                    else:
                        self.mutationLocations[self.genes[geneIndex]] = [turnIndex]         #MEMO
                            
                # Reset Gene if we did not have a successful mutation
                if not accept:
                    gene.setTurn(turnIndex, oldTurn)
        
    
