# Scamp
Scamp tutorials and knowledge base


## References

- [Homepage](http://scamp.marcevanstein.com/)
- [LoopMidi](https://www.tobias-erichsen.de/software/loopmidi.html)
- [Scamp Thesis](http://marcevanstein.com/Writings/Evanstein_MAT_Thesis_SCAMP.pdf)
- [Jack Audio](https://jackaudio.org/downloads/)


## Installing
- pip3 install scamp
- pip3 install scamp_extensions

- Install Lilypond from [here](http://lilypond.org/development.html)

- pip3 install python-rtmidi --use-pep517

For python-rtmidi, you will first need to install:

![image](https://user-images.githubusercontent.com/12407183/209846499-611bf8ba-43e3-4943-8283-1fb85199566f.png)

Available from https://visualstudio.microsoft.com/visual-cpp-build-tools/

- pip3 install abjad==3.4



## Using LoopMidi with Scamp and Reaper

- Installed loopMIDI and add a new virtual MIDI port (MidiLoop) as shown.

![image](https://user-images.githubusercontent.com/12407183/209932117-50b917ec-eb81-4325-a015-2e32bcf7562c.png)

In Reaper go to Options->Preferences and double click the MidiLoop option

![image](https://user-images.githubusercontent.com/12407183/209932329-1ab6c0f3-afd3-4217-a119-73574e3c618e.png)

Check the "Enable input from this device" option and click OK and the click Apply on the main dialog.

![image](https://user-images.githubusercontent.com/12407183/209932371-a61b94fe-e91e-4321-b0d3-2043d90d243d.png)

Now select an instrument and set its midi input to MidiLoop

![image](https://user-images.githubusercontent.com/12407183/209932594-23a3a428-3fb7-4e49-803a-60c02479b0e5.png)




## Sending and Receiving Midi with Scamp

![midipaths](https://user-images.githubusercontent.com/12407183/210153089-4b8599cc-d62c-4600-a742-7f48ee91e2d9.jpg)

[LoopMidi](https://www.tobias-erichsen.de/software/loopmidi.html) is used to create two virtual midi channels.
Notes are then sent from virtualKeys piano keyboard to Scamp and Scamp then redirects that data to [QSynth](https://qsynth.sourceforge.io/).

See the send_receive.py example in the repository


