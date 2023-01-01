from scamp import *
from collections import namedtuple
import datetime


USE_PLAY_NOTE=True

class Note:
    def __init__(self,pitch,volume,clock):
        self.__duration = 0.0
        self.__pitch = pitch
        self.__volume = volume
        self.__clock = clock
    
    def show(self):    
        return "Pitch {}, Volume = {},  clock = {}, Duration = {}".format(self.__pitch,self.__volume,self.__clock, self.__duration)   

    @property
    def duration(self):
        """The duration property."""
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value  

    @property
    def pitch(self):
        """The pitch property."""
        return self.__pitch

    @pitch.setter
    def pitch(self, value):
        self.__pitch = value  
                  

class Manipulator:
    def __init__(self):
        self.session = Session()
        self.session.print_available_midi_output_devices()
        self.session.print_available_midi_input_devices()
        try:
            self.piano = self.session.new_midi_part("piano", midi_output_device=4, num_channels=8) # Scamp to QSynth
        except:
            print("Failed to open MidiLoop Port for output")      


        self.onTime = None
        self.offTime = None

    def midi_callback(self,midi_message):
        code, pitch, volume = midi_message
        print("Keyboard {}".format(midi_message))
        if(volume > 0): # this is an on-event
            self.onTime = datetime.datetime.now()
            self.note = Note(pitch,volume,self.onTime.timestamp())

        else:  
            self.offTime = datetime.datetime.now()
            delta = self.offTime - self.onTime
            self.note.duration = float(delta.total_seconds())

            # Eventually do something with the note here, but for now
            self.session.fork(self.playNote)
   
    def playNote(self):
        if(USE_PLAY_NOTE):
                self.piano.play_note(self.note.pitch,.8,self.note.duration) 
        else:
            noteReference = self.piano.start_note(self.note.pitch, .8)
            wait(self.note.duration)
            noteReference.end()


    def Run(self):

        try:     
            self.session.register_midi_listener(3, self.midi_callback) #[Port 4]: Input from Virtual Keyboard
        except:
            print("Failed to open MidiLoop Port for input")                
        self.session.wait_forever()


m = Manipulator()
m.Run()
