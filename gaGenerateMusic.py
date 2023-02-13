from pyeasyga.pyeasyga import GeneticAlgorithm
from motif import *
from chord import *
from globals import *
from rythm import *


import random

ROOT_NOTE=60
NUMBER_OF_BARS = 2


class MusicGenerator():
    
    def __init__(self):
        self.session = Session()
        self.session.tempo = TEMPO
        self.__scale = scale = Scale.major(ROOT_NOTE,0,True)
        self.__chord = Chord("C Major" ,ROOT_NOTE,1,1,self.__scale)
        self.__rythm = Rythm(4,4)
        self.__rythm.generate()
        self.__violin = self.session.new_part("Violin")
        self.__rythmIterator =  iter(self.__rythm)
        self.__motif_data = [('pear', 50), ('apple', 35), ('banana', 40)]
        self.__ga =  GeneticAlgorithm(self.__motif_data, 100, 100, 0.8, 0.2, True, True)
        self.__ga.create_individual = self.create_individual
        self.__ga.crossover_function = self.crossover
        self.__ga.mutate_function = self.mutate
        self.__ga.selection_function = self.selection
        self.__ga.fitness_function = self.fitness
        self.__populationSize = 0


    def create_individual(self,motif_data):
        motif = Motif(self.__chord,self.__scale,self.__rythm,BEATS_PER_BAR,NUMBER_OF_BARS)
        motif.Generate()
        individual = motif.toGenome()
        self.__populationSize += 1
        print("Creating individual {}".format(self.__populationSize))
        return individual





    def crossover(self,parent_1, parent_2):
        crossover_index = random.randrange(1, len(parent_1)) # the crossover is on a note boundary, so this does not corrupt the pitch or lenght, it is basically mixxing two motifs
        child_1 = parent_1[:crossover_index] + parent_2[crossover_index:]
        child_2 = parent_2[:crossover_index] + parent_1[crossover_index:]
        return child_1, child_2




    def mutate(self,individual): # an individual is a list of notes in a motif
        #print("mutate : individual {}".format(individual))
        note_index = random.randrange(len(individual))
        notelist = individual[note_index]
        note = notelist[0]
        noteAsList = list(note)
        mutate_index = random.randrange(len(noteAsList))
        if noteAsList[mutate_index] == '0':
            noteAsList[mutate_index] = '1'
        else:
            noteAsList[mutate_index] = '0'
        note = ''.join(noteAsList)
        individual[note_index] = []
        individual[note_index].append(note)
        #print("mutation {}".format(individual[note_index]))


    def PlayMotif(self,individual):
        motif = Motif(self.__chord,self.__scale,self.__rythm,BEATS_PER_BAR,NUMBER_OF_BARS)
        motif.fromGenome(individual)
        print(".................")
        for note in motif.notes:
            if(note.pitch < 0):
                print("invalid pitch {}".format(note.pitch))
            else:    
                print("{}".format(note.show()))
                self.__violin.play_note(note.pitch,note.volume,note.length)
        print("....................")

    def selection(self,population):
        return random.choice(population)



    def fitness (self,individual, motif_data):
        fitness = 0
        motif = Motif(self.__chord,self.__scale,self.__rythm,BEATS_PER_BAR,NUMBER_OF_BARS)
        motif.fromGenome(individual)
        if(motif.isValidLength()):
            fitness = 1  
        if(motif.hasValidNotes()):
            fitness += 1
        if(motif.isValidMotif() == False):
            fitness -= 1
        #print("Fitness {}".format(fitness))
        return fitness

    def run(self):
        self.__ga.run()

    def showBestIndividual(self):
        print("Best : {}".format(self.__ga.best_individual()))        
        for individual in self.__ga.last_generation():
            fitness = individual[0]
            #print(individual)
            if(fitness > 1):
                self.PlayMotif(individual[1])


    def getBestIndividual(self):
        return self.__ga.best_individual()

mg = MusicGenerator()
mg.run()
mg.showBestIndividual()
mg.PlayMotif(mg.getBestIndividual()[1])
