from scamp import *
from scamp_extensions.pitch import Scale
import random
from chord import Chord
from note import Note
from rythm import Rythm
from globals import *
from motif import *






class Generator:
    def __init__(self):
        self.session = Session()
        self.session.tempo = TEMPO
        self.session.print_available_midi_output_devices()
        self.session.print_available_midi_input_devices()
        if(USE_MIDI):
            self.violin = self.session.new_midi_part("violin", midi_output_device=TO_REAPER, num_channels=8)
        else:
            self.violin = self.session.new_part("Violin")
        self.pentatonic = Scale.pentatonic(start_pitch = 60, cycle= True)
        self.level1 = 2
        self.level2 = 3
        self.duration = 0.25
        self.rythm = Rythm(4,4)
        self.rythm.generate()
        self.rythmIterator =  iter(self.rythm)
        

    def ShowScale(self):
        for i in range(20):
            note = Note(self.pentatonic[i],1,1)
            print("index {} -- pitch {} -- Note {} ".format(i,note.pitch,note.name))

    def GetValidNoteLength(self, total_beats):
        length = 0
        available_lengths = [1,.5,1,2,4,.5]
        valid_lengths = []
        for l in available_lengths:
            if (l + total_beats <= BEATS_PER_BAR ):
                valid_lengths.append(l)
                # print("total_beats to date={} l={} total={}".format(total_beats,l,total_beats+l))    
        if(len(valid_lengths) > 0):            
            length = random.choice(valid_lengths)
        else:
            print("Could not find a suitable length Total beats = {}".format(total_beats))    
        print("returning length {}".format(length))
        return length


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







    def CreateBar(self, is_first_bar, is_last_bar,currentPitchIndex = 7):
        # we start with the root note
        total_beats = 0
        volume = 0.8
        bar = []        
        if(is_first_bar):            
            length = next(self.rythmIterator)
            note = Note(self.pentatonic[currentPitchIndex],volume,length)
            print("Adding note : {} {} with index {} and length {}".format(note.pitch,note.name,currentPitchIndex,length))     
            bar.append(note)
            total_beats += 1
        while (total_beats < BEATS_PER_BAR) :
            #length = self.GetValidNoteLength(total_beats)
            length = next(self.rythmIterator)
            self.rythm
            noteIndex = self.GetNextNoteInterval( currentPitchIndex)
            note = Note(self.pentatonic[noteIndex],volume,length) 
            print("Adding note : {} {} with index {} and length {}".format(note.pitch,note.name,noteIndex,length))     
            currentPitchIndex = noteIndex      
            bar.append(note)
            total_beats = total_beats + length

        return bar,currentPitchIndex

    def CreatePhrase(self):
        # we start with the root note
        volume = 0.8
        phrase = []
        motif = Motif(None,self.pentatonic,Rythm(),BEATS_PER_BAR,2)
        print("Opening bar")
        bar,index = self.CreateBar( True, False,0)
        for note in bar:
            phrase.append(note)
        print("Middle bars") 
        motifNotes, index =    motif.Create(index)
        for r in range(3):
            print("Motif {}",r)
            for note in motifNotes:
                print("Motif: {}".format(note.name))
                phrase.append(note)
        newMotifNotes = motif.Clone(motifNotes)
        motif.Vary(newMotifNotes)
        print("Motif Variation {}",r+1)
        for note in newMotifNotes:
            print("Variation: {}".format(note.name))
            phrase.append(note)
        # bar,index = self.CreateBar(False, False,index)
        # for note in bar:
        #     phrase.append(note)
        print("closing bar")    
        bar,index = self.CreateBar(False, True,index)
        for note in bar:
            phrase.append(note)    
        return phrase

    def evaluateTone(self,chord,tone):
        if(tone):
            toneType = chord.identifyToneType(tone)
            print("Tone {} is  {}".format(tone,toneType))
        else:
            print("Tone {} is not valid".format(tone))   

    def PlayMotif(self,notes,chord):
        print("........{}.........".format(chord))
        for note in notes:
            print("{}".format(note.show()))
            self.violin.play_note(note.pitch,note.volume,note.length)
        print("....................")


    def PlayOutput(self):
        #self.session.start_transcribing()
        pitch = 0
        beat = 1
        CScale = [60,62,64,65,67,69,71,72]
        scale = Scale.major(60,0,True)
        # scale.pitch_to_degree(pitch)
        c = Chord("C Major" ,60,1,1,scale)
        f = Chord("C Major" ,65,1,1,scale)
        g = Chord("C Major" ,67,1,1,scale)
        a = Chord("C Major" ,69,1,1,scale)
        e = Chord("C Major" ,69,1,1,scale)
        for note in range(8):
            print("Degree {} Pitch {} ".format(note,scale.degree_to_pitch(note)))
        for note in CScale:
            print("pitch {} Degree {} ".format(note,scale.pitch_to_degree(note)))
        for n in range(2): 
            print("-----------------------------------")   
            motif = Motif(c,scale,self.rythm,BEATS_PER_BAR,2)
            CMotif = motif.Generate()
            genome = motif.toGenome()
            motif.Show()
            if(motif.isValid()):
                print("Motif is valid")
            else:
                print("Motif is invalid")    
            print("Motif Genome {}".format(genome))
            motif2 = Motif(c,scale,self.rythm,BEATS_PER_BAR,2)
            motif2.Show()

            print("-----------------------------------")
            self.PlayMotif(CMotif,"C")
            motif = Motif(g,self.pentatonic,self.rythm,BEATS_PER_BAR,2)
            GMotif = motif.Generate()
            self.PlayMotif(GMotif,"G")
            motif = Motif(a,self.pentatonic,self.rythm,BEATS_PER_BAR,2)
            AMotif = motif.Generate()
            self.PlayMotif(AMotif,"Am")
            motif = Motif(f,self.pentatonic,self.rythm,BEATS_PER_BAR,2)
            FMotif = motif.Generate()
            self.PlayMotif(FMotif,"F")

        # stop transcribing and save the
        # note events as a performance
        #performance = self.session.stop_transcribing()
        # quantize and convert the performance to
        # a Score object and open it as a PDF
        # (by default this is done via abjad)
        #performance.to_score(time_signature=["4/4"]).show()    
        # self.violin.play_note(passing,c.volume,c.length)
        # adjacent = c.getAdjacentNote(3,1)
        # self.violin.play_note(adjacent,c.volume,c.length)
        # passing = c.getPassingNote(3,5)
        # self.violin.play_note(passing,c.volume,c.length)
        # self.violin.play_chord(c.notes,c.volume,c.length,"arpeggiate") 
        # if(c.isChordTone(60)):
        #     print("This is a chord tone")
        # else:
        #     print("This is not a chord tone")  
        # phrase = self.CreatePhrase()
        # previous = phrase[0].pitch
        # # while True:
        # print("\n : Phrase start ")
        # if SHOW_SCORE:
        #     self.session.start_transcribing() 
        # for note in phrase:
        #     self.violin.play_note(note.pitch,note.volume,note.length)
        #     print("Pitch {} Note {} Length {} Interval {}".format(note.pitch,note.name,note.length,note.pitch - previous))
        #     previous = note.pitch
        # if SHOW_SCORE:
        #     self.performance = self.session.stop_transcribing()
        #     self.performance.to_score(time_signature=["4/4"]).show()



    def testGenome(self):
        scale = Scale.major(60,0,True)
        c = Chord("C Major" ,60,1,1,scale)
        print("-----------------------------------")   
        motif = Motif(c,scale,self.rythm,BEATS_PER_BAR,2)
        CMotif = motif.Generate()
        genome = motif.toGenome()
        motif.Show()
        if(motif.isValid()):
            print("Motif is valid")
        else:
            print("Motif is invalid")    
        print("Motif Genome {}".format(genome))
        motif2 = Motif(c,scale,self.rythm,BEATS_PER_BAR,2)
        motif2.fromGenome(genome)
        motif2.Show()
        print("-----------------------------------")




    def ShowLevels(self):
        print("Level 1: {}".format(self.level1))
        print("Level 2: {}".format(self.level2))
        print("Duration: {}".format(self.duration))

    def MidiControllerCallback(self,midi_message):
            print("Controller {}".format(midi_message))
            code, controlID, volume = midi_message
            if(controlID == BUTTON_1 and (volume == 0)):
                self.session.kill()    
            elif(controlID == BUTTON_2 and (volume == 0)):
                self.session.start_transcribing() 
            elif(controlID == BUTTON_3 and (volume == 0)):
                self.performance = self.session.stop_transcribing() 
            elif(controlID == BUTTON_4 and (volume == 0)):
                self.performance.to_score(time_signature=["4/4"]).show() 
                self.session.kill()    
            elif(controlID == 4 ):
                self.level2 =int(volume /25)
            elif(controlID == 11 ):
                self.duration = (volume/127)    
            #else:
                # print("Received unknown command {}".format(controlID))     

    def Run(self):
        if(LISTEN_FOR_MIDI):    
            try:
                print("Registering Controller listener for SZ_MINICONTROL") 
                self.session.register_midi_listener(SZ_MINICONTROL, self.MidiControllerCallback) #[Port 2]: SZ-MINICONTROL 2
            except:
                print("Failed to open SZ_MINICONTROL Port for input")                
        self.session.fork(self.PlayOutput) 
        self.session.wait_for_children_to_finish()       
        # self.session.wait_forever()               


m = Generator()
#m.ShowScale()
#m.Run()        
m.testGenome()

# myclass = Rythm()
# myiter = iter(myclass)
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
