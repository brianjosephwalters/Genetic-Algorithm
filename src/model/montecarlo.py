'''
Created on Oct 10, 2014

@author: bjw
'''
import random

class MonteCarlo:
    def __init__(self, inputs, probabilities):
        if len(inputs) != len(probabilities):
            print "Error: You must provide probabilities for each input type"
        if sum(probabilities) < .999 or sum(probabilities) > 1.001:
            print "Error: Probabilities should add to 1."
        self.inputs = inputs
        self.probabilities = probabilities
        
    def produceSimpleSequence(self, size):
        return random.sample(self.inputs, size)
    
    def produceWeightedSequence(self, size):
        results = []
        for i in range(size):
            results.append(self.getWeightedSelection())
        return results
    
    def getWeightedSelection(self):
        number = random.random() * 1000
        for i, probability in enumerate(self.probabilities):
            if (number - (probability * 1000)) > 0:
                number -= probability * 1000
            else:
                return self.inputs[i]
    
def getDefaultMCSequence(size):
    inputs = ['F', 'L', 'R']
    probabilities = [.3333, .3333, .3334]
    mc = MonteCarlo(inputs, probabilities)
    return mc.produceWeightedSequence(size)


if __name__ == '__main__':
    inputs = ['F', 'L', 'R']
    probabilities = [.3333, .3333, .3334]
    mc = MonteCarlo(inputs, probabilities)
    print mc.produceWeightedSequence(20)
    
    