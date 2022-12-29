# scamp
Scamp tutorials and knowledge base


## References

- [Homepage](http://scamp.marcevanstein.com/)
- [LoopMidi](https://www.tobias-erichsen.de/software/loopmidi.html)


## Installing
- pip3 install scamp
- pip3 install scamp_extensions

- Install Lilypond from [here](http://lilypond.org/development.html)

- pip3 install python-rtmidi --use-pep517

For python-rtmidi, you will first need to install:

![image](https://user-images.githubusercontent.com/12407183/209846499-611bf8ba-43e3-4943-8283-1fb85199566f.png)

Available from https://visualstudio.microsoft.com/visual-cpp-build-tools/

- pip3 install abjad==3.4



# Using LoopMidi with Scamp and Reaper

- Installed loopMIDI and add a new virtual MIDI port (MidiLoop) as shown.

![image](https://user-images.githubusercontent.com/12407183/209932117-50b917ec-eb81-4325-a015-2e32bcf7562c.png)

In Reaper go to Options->Preferences and double click the MidiLoop option

![image](https://user-images.githubusercontent.com/12407183/209932329-1ab6c0f3-afd3-4217-a119-73574e3c618e.png)

Check the "Enable input from this device" option and click OK and the click Apply on the main dialog.

![image](https://user-images.githubusercontent.com/12407183/209932371-a61b94fe-e91e-4321-b0d3-2043d90d243d.png)

Now select an instrument and set its midi input to MidiLoop

![image](https://user-images.githubusercontent.com/12407183/209932594-23a3a428-3fb7-4e49-803a-60c02479b0e5.png)




In MSP:
- Created a Smart Button
- Chose Send MIDI commands action
- Chose loopMIDI as the destination (note it was listed just as "MIDI")
- Created a control code action for a MIDI channel I don't use

in Reaper:
- Enabled loopMIDI for input in Midi Devices
- Created a dummy Track to receive the loopMIDI control codes relayed from MSP
- Armed that track and chose loopMIDI as the in FX source
- Installed ReaLearn (see https://www.helgoboss.org/projects/realearn/)
- Used "Learn Source" in ReaLearn and clicked the Smart Button - this automatically picks up the Smart Button CC I send, relayed via loopMIDI
- Used "Learn Target" to record the track I wanted to arm (could be any other Reaper action)

I repeated this with different control codes for each track I wanted to arm, and each track I wanted to disarm, adding all the mappings to ReaLearn - I only have to do this once.  I started at CC 100 but that was arbitrary.

Then in the MSP Smart Button for a Song I added multiple Send MIDI commands for disarming and arming the tracks I wanted for that song.   Now when I click the Smart Button in a Song it automatically arms/disarms the tracks corresponding to the virtual and physical instruments I want to use with my MIDI keyboards/pads/instruments for that song when playing "live".  Magic!
