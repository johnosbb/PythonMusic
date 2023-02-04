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

    def __init__(self,pitch,volume,length):
        self.__pitch = pitch
        self.__volume = volume
        self.__length = length
        self.__name = self.PitchToNote(int(pitch))

    
    def show(self):    
        return "Pitch {}, Volume = {}, length = {}".format(self.__pitch,self.__volume, self.__length)   

    def PitchToNote(self,number: int) -> tuple:
        octave = number // self.NOTES_IN_OCTAVE
        assert octave in self.OCTAVES, self.errors['notes']
        assert 0 <= number <= 127, self.errors['notes']
        note = self.NOTES[number % self.NOTES_IN_OCTAVE]

        return note, octave

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

