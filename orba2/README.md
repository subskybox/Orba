# Orba 2 Tools

## What Utilities have I built?
This repository contains Orba 2 Utilities to help you perform advanced changes to your Orba 2. These utilities help you create custom User Presets. As I'm learning more about how the Orba 2 and *.artipreset* files correspond, I will publish other useful tools.

1. **Orba 2 SampleSet Generator**
>> A Python based script for generating a new Orba 2 Preset from a collection of .wav files

## Orba 2 SampleSet Generator
The Orba 2 SampleSet Generator takes a folder as an input and outputs the ```<SampleSet>``` node required to be added to a *.artipreset* file. The script supports many options and uses a naming convention similar to many common formats available on the web or from other musical DAW software.

### PREREQUISITES:
You must have Python 3.2 or greater to run this script. If you don't have Python installed, just Google "Install Python on Mac|PC". The easiest way to do this on Windows is to download Python from the Windows Store. For Mac, you can install directly from [Python.org](https://www.python.org/downloads/macos/) or install it via [Homebrew or MacPorts](https://www.scivision.dev/homebrew-macports-fink/)

### DOWNLOADING:
Make sure to be on the `Code` tab and then press the green `Code ▼` button to expand the drop-down. From the drop-down, choose `Download ZIP`. Once the file has completed downloading, unzip it to a suitable folder.

### USAGE:
 Navigate to the `orba2` folder in your terminal with:
```
cd [path_to_orba2_folder]
  (e.g. cd C:\Users\[user account]\Downloads\Orba-master\orba2) on PC
  (e.g. cd /Users/<your_user>/Downloads/Orba-master/orba2) on Mac
```
Then run the script with the following command:

**PC or Mac:**
```
python orba_sample_set_generator.py [path_to_wav_folder]
```

>**PRO TIP**: You can *Drag & Drop* your folder from the *File Explorer* or *Finder* directly to the Terminal window rather than typing [path_to_wav_folder].

This will output the ```<SampleSet>``` node which can be replaced into a *.artipreset* file. The best approach is to make a copy of a factory *.artipreset* file and rename it *Your_new_preset_name.artipreset*. After this, using a text editor, replace the ```<SampleSet>``` node with the one generated from the script.

The factory *.artipreset* files can be found here:

**PC:**
```
C:\Users\Public\Documents\Artiphon\Common\Presets\
```
**Mac:**
```
/Users/shared/Artiphon/Common/Presets/
```

### NOMENCLATURE:
```
Filename format for .wav files is as follows (< > denotes optional):

 NamePart1<_namePart2_namePartn>_Note<_Velocity><_LoopStart><_LoopEnd><_UUID>.wav

      Name: Can be any name and contains underscores if desired  
      Note: [A-G] character followed by a #|b (sharp|flat) followed by an octave # (e.g. A#3)
  Velocity: An integer from 0-127 or a music dynamic string from {ppp, pp, p, mp, mf, f, ff, fff}
 LoopStart: Any integer which represents the sample # of where the loop starts
   LoopEnd: Any integer which represents the sample # of where the loop ends
      UUID: Any legal UUID. Must be 32 characters mixed of [0-9] and [a-f]
```
>**PRO TIP**: Sample #s can be obtained from audio editing software such as [Audacity](https://www.audacityteam.org).

### FUTURE PLANS:
1. The script will allow you to supply the path to a *.artipreset* file and will make the replacement for you.

### DEMO:

https://user-images.githubusercontent.com/3968129/205837341-8818b2da-2b9b-4599-a261-ddabd6a2a5f6.mov
