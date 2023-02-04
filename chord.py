from scamp import *
from scamp_extensions.pitch import Scale
import random

class Chord:
    def __init__(self, name, root, length, volume, referenceScale):
        self.__notes = []
        self.__root = root
        self.__notes.append(root)
        self.__referenceScale = referenceScale
        self.__name = name
        self.__length = length
        self.__volume = volume

    def generateNotes(self):
        third = self.__referenceScale.degree_to_pitch(3)
        fifth = self.__referenceScale.degree_to_pitch(5)
        self.__notes.append(third)
        self.__notes.append(fifth)

    def isChordTone(self,note):
        if(note in self.__notes):
            return True
        else:
            return False    

    def getPassingNote(self,degreeFirstNote,degreeSecondNote):
        passing  = self.__referenceScale.degree_to_pitch(degreeFirstNote)
        if(degreeFirstNote < degreeSecondNote):
            passing = self.__referenceScale.degree_to_pitch(degreeFirstNote + 1)
        else:
            passing = self.__referenceScale.degree_to_pitch(degreeSecondNote - 1)
        return passing    


    def getAdjacentNote(self,degree,direction):
        adjacent  = self.__referenceScale.degree_to_pitch(degree)
        if(direction == 1):
            adjacent = self.__referenceScale.degree_to_pitch(degree + 1)
        else:
            adjacent = self.__referenceScale.degree_to_pitch(degree - 1)
        return adjacent   

    @property
    def notes(self):
        """The notes property."""
        return self.__notes

    @notes.setter
    def notes(self, value):
        self.__notes = value 


    @property
    def length(self):
        """The length property."""
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value 

    @property
    def volume(self):
        """The volume property."""
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = value 

    @property
    def name(self):
        """The name property."""
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value 


    @property
    def root(self):
        """The root property."""
        return self.__root

    @root.setter
    def root(self, value):
        self.__root = value      
