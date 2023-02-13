from scamp import *
from scamp_extensions.pitch import Scale
import random


class Rythm:
    def __init__(self, numerator, denominator):
        self.name = ""
        self.__pattern = []
        #self.pattern = [1,1,1,1] # 1,.5,.5,1,.5,.5
        #self.pattern = [1,1,.5,.5,1]
        
        self.__numerator = numerator #number of beats in a bar (for exampe in 3/4 time, 3 beats per bar)
        self.__denominator = denominator #whole note division = beat value (the value of the beat in note time, in 3/4 time, a quarter note)

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):        
        n = self.__pattern[self.current]
        self.current += 1
        if(self.current == len(self.__pattern)):
            self.current = 0
        return n

    # generate a rythm based on a particulr time signature
    def generate(self):
        baseNoteLength = 1
        lengthOptions = []
        lengthOptions.append(baseNoteLength)
        lengthOptions.append(baseNoteLength) # we favour this
        lengthOptions.append(baseNoteLength * 2) 
        lengthOptions.append(baseNoteLength + (baseNoteLength/2))
        lengthOptions.append(baseNoteLength/2) 
        lengthOptions.append(baseNoteLength/2) # we favour this also
        lengthOptions.append(baseNoteLength/2 + (baseNoteLength/4))
        lengthOptions.append(baseNoteLength/4)
        lengthOptions.append(baseNoteLength/4 + (baseNoteLength/8))
        lengthOptions.append(baseNoteLength/8)
        print("lenght Options {}".format(lengthOptions))
        overallLength=0
        while(1):
            length  = random.choice(lengthOptions) 
            
            if((overallLength + length) <= self.__numerator):
                self.__pattern.append(length) 
                overallLength = overallLength + length
                print("Length: {} overall Length: {}".format(length,overallLength))
                if(overallLength == self.__numerator):
                    break
        print("achived target length {}".format(overallLength))   
        self.current = self.__pattern[0]     

    @property
    def pattern(self):
        """The pattern property."""
        return self.__pattern

    @pattern.setter
    def pattern(self, value):
        self.__pattern = value
