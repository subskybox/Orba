# Orba 2 Tools

## What Utilities have I built?
This repository contains Orba 2 Utilities to help you perform advanced changes to your Orba 2. These utilities help you create custom User Presets. As I'm learning more about how the Orba 2 and *.artipreset* files correspond, I will publish other useful tools.

1. **Orba 2 SampleSet Generator**
>> A Python based script for generating a new Orba 2 Preset from a collection of .wav files

## Orba 2 SampleSet Generator
The Orba 2 SampleSet Generator takes a folder as an input and outputs the ```<SampleSet>``` node required to be added to a *.artipreset* file. The script supports many options (including deployment) and uses a naming convention similar to many common formats available on the web or from other musical DAW software.

### PREREQUISITES:
You must have Python 3.8 or greater to run this script. If you don't have Python installed, just Google "Install Python on Mac|PC". The easiest way to do this on Windows is to download Python from the Windows Store. For Mac, you can install directly from [Python.org](https://www.python.org/downloads/macos/) or install it via [Homebrew or MacPorts](https://www.scivision.dev/homebrew-macports-fink/)

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
python orba_sample_set_generator.py [-h] [-d | -r] [-s] [-z] [-a [ARTIPRESET]] [--version] samplePath

positional arguments:
  samplePath            path to the samples folder.

options:
  -h, --help            show this help message and exit
  -d                    deploy the content to the Artiphon folder and Orba.
  -r                    remove the content to the Artiphon folder and Orba.
  -s                    suppress SampleSet node output to screen.
  -z                    zip the contents of the Common folder.
  -a [ARTIPRESET], --artipreset [ARTIPRESET]
                        path to an .artipreset file to use as starting template
  --version             show program's version number and exit
```
This will output the ```<SampleSet>``` node which can be replaced into an *.artipreset* file. The best approach is to add the `-a` flag and supply the path to an existing *.artipreset* file. This will create a `Common` folder in the *samplePath* with all the files & folders required to add the new Preset to the Orba 2 App. Once you are happy with the results, you can add the `-d` flag to deploy it.

>**PRO TIP**: You can *Drag & Drop* your folder from the *File Explorer* or *Finder* directly to the Terminal window rather than typing *samplePath*.

>**PRO TIP**: If a .png image file is found in the *samplePath*, it will be added to the `Common` folder when using `-a`

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

 NamePart1<_namePart2_namePartn>_Note<_Velocity><_LoopStart><_LoopEnd>.wav

      Name: Can be any name and contain underscores if desired  
      Note: [A-G] character, optionally followed by a #|b (sharp|flat), followed by an octave # (e.g. A#3)
  Velocity: An integer from 0-127 or a music dynamic string from {ppp, pp, p, mp, mf, f, ff, fff}
 LoopStart: Any integer which represents the sample # of where the loop starts
   LoopEnd: Any integer which represents the sample # of where the loop ends
```
>**PRO TIP**: Sample #s can be obtained from audio editing software such as [Audacity](https://www.audacityteam.org).

### FUTURE PLANS:
1. Bug Fixing
2. Adding more useful option flags

### EXAMPLE
[Clarinet.zip](https://github.com/subskybox/Orba/files/10275169/Clarinet.zip)

### DEMO:

https://user-images.githubusercontent.com/3968129/205837341-8818b2da-2b9b-4599-a261-ddabd6a2a5f6.mov
