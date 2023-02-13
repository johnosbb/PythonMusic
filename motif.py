from chord import Chord
from note import Note
from scamp import *
from scamp_extensions.pitch import Scale
import random
from globals import *
from rythm import Rythm




class Motif:

    def __init__(self,referenceChord: Chord,referenceScale: Scale,rythm: Rythm,beatsPerBar: int,motifLengthInBars):
        self.__referenceChord = referenceChord
        self.__referenceScale = referenceScale
        self.__motifLengthInBars = motifLengthInBars
        self.__beatsPerBar = beatsPerBar
        self.__rythm = rythm
        self.__rythmIterator =  iter(self.__rythm)
        self.__notes = []

        # creates an n note pattern that can be repeated
    def Create(self, currentPitchIndex = 7):    
        motif = [] 
        total_beats = 0
        volume = 0.8
        for bar in self.__motifLengthInBars:
            while (total_beats < self.__beatsPerBar) :
                #length = self.GetValidNoteLength(total_beats)
                length = next(self.__rythmIterator)
                # self.rythm
                noteIndex = self.GetNextNoteInterval( currentPitchIndex)
                note = Note(self.__referenceScale[noteIndex],volume,length) 
                print("Adding note to motif: {} {} with index {} and length {}".format(note.pitch,note.name,noteIndex,length))     
                currentPitchIndex = noteIndex      
                motif.append(note)
                total_beats = total_beats + length
        return motif,currentPitchIndex    

    def isValidLength(self):
        # check that length of each bar is valid
        overallLength = 0.0
        for note in self.__notes:
            overallLength = overallLength + note.length
        if(overallLength != (self.__beatsPerBar * self.__motifLengthInBars)) :
            return False
        else:
            return True    

    def isValidMotif(self):
        for note in self.__notes:
            if(note.name == "INVALID" or (note.pitch < 0)):
                return False
        return True

    def hasValidNotes(self):
        for note in self.__notes:
            if(note.name == "INVALID"):
                return False
            if(self.__referenceChord.identifyToneType(note.pitch) == "Non Chord Tone"):
                return False
        return True                

    def splitGenome(self,genome: list,chunkSize : int):
        splitList = [genome[i:i + chunkSize] for i in range(0, len(genome), chunkSize)]
        return splitList


    def toGenome(self) -> list:
        genome = []
        for note in self.__notes:
            genome.append(note.toGenome())
        return genome

    def splitByN(self,s, n):
        if len(s) < n:
            return []
        elif len(s) == n:
            return [s]
        else:
            return self.splitByN(s[:n], n) + self.splitByN(s[n:], n)

    


    def fromGenome(self,genome: list) -> list:
        self.__notes = []
        #print("Motif: fromGenome : genome {}".format(genome))
        for part in genome:
            note = Note()
            note.fromGenome(part)
            self.__notes.append(note)
        return self.__notes    
 

    def GenerateNextTone(self,previousTone,previousDirection):
        if(previousDirection == 1):
            direction = random.choice([-1,1,1])
        else:
            direction = random.choice([-1,1,-1])    
        #length = self.GetValidNoteLength(total_beats)
        length = next(self.__rythmIterator)
        # self.rythm
        if(previousTone == None):
            tone = self.__referenceChord.generateChordTone()   
            #print("Generate: First Tone chosing chord tone {} - direction = {}".format(tone,direction)) 
        elif(self.__referenceChord.isChordTone(previousTone)): 
            nextChoice = random.choice([0,1,0])  
            if(nextChoice == 1):   
                tone = self.__referenceChord.getPassingTone(previousTone,direction)
            else:         
                tone = self.__referenceChord.generateChordTone()
            #print("Generate: previousTone was chord tone {} chosing passing tone {} - direction = {}".format(previousTone,tone,direction))
        elif(self.__referenceChord.isPassingTone(previousTone)):
            tone = self.__referenceChord.getAdjacentTone(previousTone,direction)
            #print("Generate: previousTone was passing tone {} chosing adjacent tone {} - direction = {}".format(previousTone,tone,direction))
        else:
            print("Generate: Could not map this previous tone {}".format(previousTone))
        return tone,direction, length    

    # generate a motif based on a chord using the given rythm and scale
    def Generate(self):  
        
        volume = 0.8
        previousTone = None
        previousDirection = 1
        for bar in range(self.__motifLengthInBars):
            total_beats = 0
            while (total_beats < self.__beatsPerBar) :
                tone,direction,length = self.GenerateNextTone(previousTone,previousDirection)
                if(previousTone == tone):
                    print("Detecting repition")        
                note = Note(tone,1,length)    
                self.__notes.append(note)
                total_beats = total_beats + length
                previousTone = tone
                previousDirection = direction
        return self.__notes   

    def GetNextNoteInterval(self, currentPitchAsIndex):
        interval = 0
        if(currentPitchAsIndex == 0):
            interval = random.choice([0,1,2,3])
            nextInterval = currentPitchAsIndex + interval
        else:
             while True:               
                interval = random.choice([-3,-2,-2,-1,-1,-1,0,1,1,1,2,2,3])
                nextInterval = currentPitchAsIndex + interval    
                print("current Interval {}  ---  next interval {}".format(currentPitchAsIndex, nextInterval))
                if(nextInterval >  -1):
                    break
                else:
                     print("next interval {} was rejected".format(nextInterval))
                
        
        return nextInterval

    def Clone(self, motifNotes):    
        newMotif = [] 
        for note in motifNotes:
            newNote = Note(note.pitch,note.volume,note.length)
            newMotif.append(newNote)
        return newMotif

    def Show(self):    
        print("Motif")        
        for note in self.__notes:
            print("{} {}".format(note.pitch,note.length))
   

    def Vary(self, motif):
        for note in motif:
            mutate = random.choice([0,1])
            if(mutate):
                interval = random.choice([-3,-2,-1,1,2,3])
                pitch = note.pitch + interval
                note.pitch = self.__referenceScale.ceil(pitch)
                note.Update(note.pitch)


    @property
    def notes(self):
        """The notes property."""
        return self.__notes

    @notes.setter
    def notes(self, value):
        self.__notes = value 
