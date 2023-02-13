from scamp import *
from scamp_extensions.pitch import Scale
import random

class Note:

    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    OCTAVES = list(range(11))
    NOTES_IN_OCTAVE = len(NOTES)

    errors = {
        'program': 'Bad input, please refer this spec-\n'
                'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/program_change.htm',
        'notes': 'Bad input, please refer this spec-\n'
                'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm'
    }

    def __init__(self,pitch=60,volume=1,length=1):
        self.__pitch = pitch
        self.__volume = volume
        self.__length = length
        self.__name = self.PitchToNote(int(pitch))

    def toGenome(self) -> list:
        pitch = format(int(self.__pitch), '08b')        
        length = format(int(self.__length * 32), '08b')
        genome = pitch + length
        return genome.split()

    def splitByN(self,genome, n):
        s = ''.join(genome)
        if len(s) < n:
            return []
        elif len(s) == n:
            return [s]
        else:
            return self.splitByN(s[:n], n) + self.splitByN(s[n:], n)

    def splitGenome(self,genome: list,chunkSize : int):
        for i in range(0, len(genome), chunkSize):
            yield genome[i:i + chunkSize]

    def fromGenome(self,genome: list) -> tuple:
        #print(" Note: fromGenome: genome {}".format(genome))
        parts = self.splitByN(genome,8)
        # partsList = list(self.splitGenome(genome,8))
        # pitchPart = ''.join(partsList[0])
        # lengthPart = ''.join(partsList[1])
        self.__pitch = int(parts[0],2)    
        self.__length = int(parts[1],2)/32  
        self.__name = self.PitchToNote(int(self.__pitch))
        return self.__pitch,self.__length   
    
    def show(self):    
        return "Name {}, Pitch {}, Volume = {}, length = {}".format(self.__name,self.__pitch,self.__volume, self.__length)   

    def PitchToNote(self,number: int) -> tuple:
        octave = number // self.NOTES_IN_OCTAVE
        if(octave not in self.OCTAVES):
            return 'INVALID', 0
        #assert octave in self.OCTAVES, self.errors['notes']
        if(0 <= number <= 127):
            note = self.NOTES[number % self.NOTES_IN_OCTAVE]
            return note, octave
        else:
            return 'INVALID', 0    
        

    def Update(self,pitch):
        self.__name = self.PitchToNote(int(pitch))
        self.__pitch = pitch

    def NoteToPitch(self,note: str, octave: int) -> int:
        assert note in self.NOTES, self.errors['notes']
        assert octave in self.OCTAVES, self.errors['notes']
        note = (self.NOTES_IN_OCTAVE * octave)
        assert 0 <= note <= 127, self.errors['notes']

        return note

    @property
    def length(self):
        """The length property."""
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value  

    @property
    def pitch(self):
        """The pitch property."""
        return self.__pitch

    @pitch.setter
    def pitch(self, value):
        self.__pitch = value  

    @property
    def name(self):
        """The name property."""
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value  


    @property
    def volume(self):
        """The volume property."""
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = value  

