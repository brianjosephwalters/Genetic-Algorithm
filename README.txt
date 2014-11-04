Genetic Algorithm Project
CSCI 6635 - Pattern Recogition

You need to develop a Genetic Algorithm (GA) (or, any other heuristics based
nondeterministic approach) based structural search algorithms. The algorithm for a given
sequences will search for the best conformation or will go for minimum Energy
conformation and it will visually show or draw the best conformation found in each
generations or in each steps along with the computed fitness value.

NOTE: I am not a biologist.  Throughout this project I used the term "gene" where
I probably should have used "chromosome".

Included Secondary Sources:
Halm, Eyal (2007) "Genetic Algorithm for Predicting Protein Folding in the 2D HP Model"

Requirements:
Python 2.7.3
Tkinter (should be included in the standard python library)

How to run the project:
1.  Ensure that Python 2.7.3 is installed.
2.  Extract the files to your computer.
3.  Run using: python genetic_algorithm.py

GUI Features:
Load a "valid" data files (as specified in the assignment).
Specify features such as:
    Data Set (drop-down menu)
    Population Size
    Number of Generations
    % Elite (genes to be preserved between generations.)
    % Crossover (genes on which to apply crossover.)
    % Mutation (gene components to be mutated.)
    
You may run the program in two ways.
1)  Run Data Set
    Runs the genetic algorithm on the selected data set for the specified
    number of generations.  The gene with the best fitness score is rendered as
    a 2D visualization, as well as printed in the log.
    
    Upon completion of a "run", a history is available.

2)  Walk Data Set
    Walking a data set allows a closer look at the generations.  Each generation 
    is produced, one at a time, with a detailed textual representation of the 
    population.  Each generation displays information about its origination:
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

   A walk can be canceled at any point.  