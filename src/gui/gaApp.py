'''
Created on Oct 17, 2014

@author: bjw
'''
import Tkinter
import ttk
import tkFileDialog

import controller
from model.ga import GeneticAlgorithm

class gaApp(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.circleRadius = 5
        self.gridDistance = 20
        self.initialize()
                
    def initialize(self):
        #self._createMenu()

        self.canvasFrame = Tkinter.Frame(self)
        self.canvasFrame.grid(column=0, row=0, sticky="NW")
        self.canvas = Tkinter.Canvas(self.canvasFrame, width=500, height=300, background='green')
        self.canvas.grid(column=0, row=0, sticky="NW", padx=5, pady=5)
        self.hbar = Tkinter.Scrollbar(self.canvasFrame, orient=Tkinter.HORIZONTAL)
        self.hbar.grid(column=0, row=1, sticky="EW")
        self.vbar = Tkinter.Scrollbar(self.canvasFrame, orient=Tkinter.VERTICAL)
        self.vbar.grid(column=1, row=0, stick="NS")
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        
        self.frame = Tkinter.Frame(self)
        self.frame.grid(column=1, row=0, sticky="NE")
        
        self.initializeGAFrame()

        self.runFrame = Tkinter.Frame(self.frame)
        self.runFrame.grid(column=0, row=1, sticky="NW")
        
        self.runButton = Tkinter.Button(self.runFrame, text="Run Data Set", 
                                        command=self.runData, state=Tkinter.DISABLED)
        self.runButton.grid(column=0, row=0)
        self.genLabel = Tkinter.Label(self.runFrame, text="Generation:")
        self.genLabel.grid(column=0, row=1)
        self.genValue = Tkinter.StringVar(self.runFrame, "")
        self.genEntry = Tkinter.Entry(self.runFrame, textvariable=self.genValue,
                                      state=Tkinter.DISABLED)
        self.genEntry.grid(column=0, row=2)
        
        self.fitnessLabel = Tkinter.Label(self.runFrame, text="Best Fitness: ")
        self.fitnessLabel.grid(column=1, row=1)
        self.fitnessValue = Tkinter.StringVar(self.runFrame, "")
        self.fitnessEntry = Tkinter.Entry(self.runFrame, textvariable=self.fitnessValue,
                                          state=Tkinter.DISABLED)
        self.fitnessEntry.grid(column=1, row=2)

        self.generationsBox = ttk.Combobox(self.runFrame, state="readonly")
        self.generationsBox.grid(column=0, row=4, sticky="W", pady=2)
        self.displayButton = Tkinter.Button(self.runFrame, text="Display Generation", 
                                            command=self.displayHistory)
        self.displayButton.grid(column=1, row=4, pady=2)
        
        self.initializeResultsFrame()

    def initializeGAFrame(self):
        self.gaFrame = Tkinter.Frame(self.frame, relief=Tkinter.SUNKEN, bd=1)
        self.gaFrame.grid(column=0, row=0, columnspan=2, sticky="NWE", pady=5, padx=2)
        
        self.loadButton = Tkinter.Button(self.gaFrame, text="Load Data Set...", command=self.openFile)
        self.loadButton.grid(column=0, row=0)
        self.dataBox = ttk.Combobox(self.gaFrame, state="readonly")
        self.dataBox.grid(column=1, row=0)
        
        self.populationLabel = Tkinter.Label(self.gaFrame, text="Population Size")
        self.populationLabel.grid(column=0, row=1)
        self.populationValue = Tkinter.StringVar(self.gaFrame, "10")
        self.populationEntry = Tkinter.Entry(self.gaFrame, textvariable=self.populationValue,
                                             state=Tkinter.DISABLED)
        self.populationEntry.grid(column=0, row=2)
        
        self.generationsLabel = Tkinter.Label(self.gaFrame, text="Generations")
        self.generationsLabel.grid(column=1, row=1)
        self.generationsValue = Tkinter.StringVar(self.gaFrame, "10")
        self.generationsEntry = Tkinter.Entry(self.gaFrame, textvariable=self.generationsValue,
                                              state=Tkinter.DISABLED)
        self.generationsEntry.grid(column=1, row=2)
        
        self.elitesLabel = Tkinter.Label(self.gaFrame, text="% Elite")
        self.elitesLabel.grid(column=0, row=3)
        self.elitesValue = Tkinter.StringVar(self.gaFrame, ".10")
        self.elitesEntry = Tkinter.Entry(self.gaFrame, textvariable=self.elitesValue,
                                         state=Tkinter.DISABLED)
        self.elitesEntry.grid(column=0, row=4)
        
        self.crossoverLabel = Tkinter.Label(self.gaFrame, text="% Crossover")
        self.crossoverLabel.grid(column=1, row=3)
        self.crossoverValue = Tkinter.StringVar(self.gaFrame, ".80")
        self.crossoverEntry = Tkinter.Entry(self.gaFrame, textvariable=self.crossoverValue,
                                            state=Tkinter.DISABLED)
        self.crossoverEntry.grid(column=1, row=4)

        self.mutationLabel = Tkinter.Label(self.gaFrame, text="% Mutation")
        self.mutationLabel.grid(column=2, row=3)
        self.mutationValue = Tkinter.StringVar(self.gaFrame, ".25")
        self.mutationEntry = Tkinter.Entry(self.gaFrame, textvariable=self.mutationValue,
                                           state=Tkinter.DISABLED)
        self.mutationEntry.grid(column=2, row=4)

    def initializeResultsFrame(self):
        self.resultsFrame = Tkinter.Frame(self.frame, relief=Tkinter.SUNKEN, bd=1)
        self.resultsFrame.grid(column=0, row=2, columnspan=2)
        self.resultsScrollbar = Tkinter.Scrollbar(self.resultsFrame)
        self.resultsScrollbar.grid(column=1, row=0, sticky="NS")
        self.resultsBox = Tkinter.Text(self.resultsFrame, wrap='word', yscrollcommand=self.resultsScrollbar.set)
        self.resultsBox.grid(column=0, row=0, sticky="NSEW")  
        self.resultsScrollbar.config(command=self.resultsBox.yview)


    def drawTurnList(self, turnList):
        self.canvas.delete("all")
        coordinates = turnList.toCoordinates()
        last_pair = None
        for pair in coordinates.coordinates:
            bbox = self._getCircleBBox(pair)
            value = coordinates.pairs[pair]
            if (value == 'P'):
                color = 'black'
            else:
                color = 'blue'
            self.canvas.create_oval(bbox, fill=color)
            if last_pair is not None:
                color = 'white'
                self.canvas.create_line(self._getCoordinates(last_pair), 
                                        self._getCoordinates(pair), 
                                        fill=color)
            last_pair = pair
        self.canvas.update()
    
    def drawTurnList2(self, turnList):
        self.canvas.delete("all")
        coordinates = turnList.toCoordinates()
        last_pair = None
        for i, pair in enumerate(coordinates.coordinates):
            bbox = self._getCircleBBox(pair)
            value = coordinates.pairs[pair]
            if (value == 'P'):
                color = 'black'
            else:
                color = 'blue'
            self.canvas.create_text(bbox[0],bbox[1], anchor="nw", fill=color, text=str(i))
            if last_pair is not None:
                color = 'white'
                self.canvas.create_line(self._getCoordinates(last_pair), 
                                        self._getCoordinates(pair), 
                                        fill=color)
            last_pair = pair
        self.canvas.update()

    
    def _getCoordinates(self, pair):
        width = int(self.canvas.cget("width"))
        height = int(self.canvas.cget("height"))
        center_x = width / 2
        center_y = height / 2
        draw_x = center_x + (pair[0] * self.gridDistance)
        draw_y = center_y + (pair[1] * self.gridDistance)
        return (draw_x, draw_y)
    
    def _getCircleBBox(self, pair):
        width = int(self.canvas.cget("width"))
        height = int(self.canvas.cget("height"))
        center_x = width / 2
        center_y = height / 2
        draw_x = center_x + (pair[0] * self.gridDistance)
        draw_y = center_y + (pair[1] * self.gridDistance)
        bbox_ul_x = draw_x - self.circleRadius
        bbox_ul_y = draw_y - self.circleRadius
        bbox_br_x = draw_x + self.circleRadius
        bbox_br_y = draw_y + self.circleRadius
        return (bbox_ul_x, bbox_ul_y, bbox_br_x, bbox_br_y)
    
    def _createMenu(self):
        menubar = Tkinter.Menu(self)
        menubar.add_command(label="Open Data File...", command=self.openFile)
        self.config(menu=menubar)
        
    def enableGUI(self):
        self.runButton.config(state=Tkinter.NORMAL)
        self.populationEntry.config(state=Tkinter.NORMAL)
        self.generationsEntry.config(state=Tkinter.NORMAL)
        self.elitesEntry.config(state=Tkinter.NORMAL)
        self.crossoverEntry.config(state=Tkinter.NORMAL)
        self.mutationEntry.config(state=Tkinter.NORMAL)
        
    def openFile(self):
        f = tkFileDialog.askopenfile(mode='r', parent=self, title="Open a file...")
        if f is not None:
            lines = f.readlines()
            self.loadData(lines)
            self.enableGUI()
            f.close()
    
    def loadData(self, lines):
        self.resultsBox.insert(Tkinter.END, "Loading Data File...\n")
        self.data = controller.getData(lines)
        self.resultsBox.insert(Tkinter.END, "  " + str(len(self.data[0])) + " entries loaded.\n")
        self.dataBox['values'] = self.data[0]
        self.dataBox.set(self.data[0][0])
        
    def displayHistory(self):
        index = self.generationsBox.current()
        self.drawTurnList2(self.history[index])
        self.genValue.set(index)
        self.fitnessValue.set(self.history[index].calculateFitness())         

        self.resultsBox.insert(Tkinter.END, "Displaying Generation: " + str(index) + "\n")
        self.resultsBox.insert(Tkinter.END, "  " + self.history[index].asString() + "\n")
        self.resultsBox.insert(Tkinter.END, "  Fitness: " + str(self.history[index].calculateFitness()) + "\n")
        
    def runData(self):
        line = self.dataBox.get()
        setIndex = self.dataBox.current()
        if line is not None:
            self.resultsBox.insert(Tkinter.END, "Running Data Set:\n")
            self.resultsBox.insert(Tkinter.END, "  Known Fitness: " + str(abs(self.data[1][setIndex])) + "\n")
            self.resultsBox.insert(Tkinter.END, "  " + str(self.data[0][setIndex].upper()) + "\n")
            ga = GeneticAlgorithm(list(line.upper()), 
                                  populationSize=int(self.populationValue.get()), 
                                  generations=int(self.generationsValue.get()),
                                  elitePercent=float(self.elitesValue.get()),
                                  crossoverPercent=float(self.crossoverValue.get()),
                                  mutationPercent=float(self.mutationValue.get()))
            for gen in ga:
                currentBestFitness = ga.currentPopulation.getFitness(0)
                currentBestGene = ga.currentPopulation.getGene(0)
                self.genValue.set(gen)
                self.fitnessValue.set(currentBestFitness)         
                self.resultsBox.insert(Tkinter.END, 
                                       "Generation " + str(gen) + ": " + str(currentBestFitness) + "\n")
                self.resultsBox.insert(Tkinter.END,
                                       "  " + currentBestGene.asString() + '\n')
                self.drawTurnList2(currentBestGene)
            self.history = ga.history
            self.generationsBox['values'] = ga.history
            self.generationsBox.set(ga.history[0])
        
    
if __name__ == '__main__':
    from model.turns import TurnList
    turns = ['F', 'L', 'L', 'F', 'R', 'F', 'R']
    values = ['P', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList = TurnList(turns, values)

    turns2 = ['R', 'L', 'L', 'F', 'L', 'F', 'R']
    values2 = ['H', 'P', 'H', 'P', 'H', 'H', 'P']
    turnList2 = TurnList(turns2, values2)
    app = gaApp(None)
    app.title("Genetic Algorithm Application")
    app.drawTurnList2(turnList)
    app.mainloop()
    
    