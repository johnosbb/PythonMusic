from scamp import *
from scamp_extensions.pitch import Scale
import random


class Rythm:
    def __init__(self):
        self.name = ""
        # self.pattern = [1,1,.5,.5,.5,.5]
        self.pattern = [1,1,1,1]
        self.current = self.pattern[0]

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):        
        n = self.pattern[self.current]
        self.current += 1
        if(self.current == len(self.pattern)):
            self.current = 0
        return n

    @property
    def pattern(self):
        """The pattern property."""
        return self.__pattern

    @pattern.setter
    def pattern(self, value):
        self.__pattern = value
