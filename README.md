# Orba Tools

## What is an Orba?
Orba is a musical instrument designed for your hands. It is a synth, looper, and controller that lets you create songs with intuitive gestures like tapping, sliding, and waving.
Orba is made by [Artiphon](https://artiphon.com/pages/orba-by-artiphon).
Orba software is available in the [Downloads](https://artiphon.com/pages/downloads) section of their website but is known to be fairly feature-limited compared to what their customers would like to see. For this reason, I am sharing a few Orba Utilities I have built.

## What Utilities have I built?
This repository contains several Orba Utilities to help you perform advanced changes to your Orba. These utilities help you to edit Preset voicings (i.e. apply custom chords and scales that are transposable). Some of these utilities have been moved to the `archived` folder as the tools have been combined/simplified. As I'm learning more about how the Orba and .orbapreset files correspond, I may modify the structure further.

1. **Orba Chord and Scale Editor**
>> An HTML based Editor that interfaces (MIDI-IN | MIDI-OUT) with your Orba
2. **Orba Update Thumbnail Script**
>> A script to help simplify the task of changing a Preset voice's thumbnail as seen in the Orba App.

## Orba Chord and Scale Editor
An Orba Preset voice editor that allows you to completely customize Chords & Scales for any Orba Preset! It features a  GUI-MIDI keyboard that works bi-directionally with Orba, as well as a fluid editing interface to edit Chord voicings and/or Major/Minor Scale sets.
### USAGE:
Make sure to be on the `Code` tab and then press the green `Code ▼` button to expand the drop-down. From the drop-down, choose `Download ZIP`. Once the file has completed downloading, unzip it to a suitable folder.

To set this up, launch the Orba app and connect to the Orba. Now open the *OrbaChordAndScaleEditor.html* page in the *Chrome* or *Edge with Chrome* Browser. You may have to use only a wired connection to get the connection working in both directions. The Editor will switch to the natural context of your Orba's current Mode. For example, if you are in Bass/Lead mode the editor defaults to the Scale drop-downs. If you are in Chord mode, the Editor defaults to the 4 voice Offsets grid. You can toggle the Editor mode by clicking on the Table Caption/Header. Choose the Key and Major/Minor settings you'd like to work with and click the mouse on the virtual keyboard to send notes to the Orba.

#### Setup:
Start by choosing a starting Preset. Load your Orba with the Preset you would like to edit and then drag & drop that Preset (.orbapreset file) from the Presets folder into the *Starting Template* box at the bottom of the Editor. Play a few notes on the Orba and the Editor should switch to the corresponding mode and highlight the notes you've played on the virtual keyboard. You're ready to start editing.

#### Chord Mode:
Each value controls the note offset for the corresponding voice in semitones from that chord's corresponding root note. Each Pad Button plays a 4 voice chord as defined by the offsets in the tables. Toggling between Major/Minor mode will re-populate these values with the corresponding offsets. The values are maintained for each mode. In this way you can store 8 chords for Major mode and 8 chords for Minor mode. Chords do not need to be 4 voices. You can have 3 voice chords by simply doubling one of the voice offsets to land on the same note. This can also be used with 2 notes to create melodic harmonies/couterpoint.
>**PRO TIP**: Holding `SHIFT` while clicking the `+/-` buttons will copy that value to the rest of the voices for that Pad.

>**PRO TIP**: Values can be entered manually and the Tab order has been set to move in rows.

#### Scale Mode:
Two drop-downs appear. One defines the scale that will be applied to the Major mode and the the other defines the scale applied to the Minor mode. Clicking the Pad Buttons will allow you to hear/see that scale. Scales can be customized by adding the appropriate offset values to the *orba-scales.json* file in the `data` folder.
>**PRO TIP**: You can toggle to Chord mode by clicking the Table Caption/Header. By modifying all 4 voices to the same value, you can work out what offsets need to be added to the *orba-scales.json* file.

#### Saving your new Preset:
When you're happy with your changes, provide an appropriate filename for your new Preset in the *Save As* Filename textbox at the bottom of the Editor. The default filename is the name of the file you've selected for the *Starting Template*. Press the `Download` Button in the *Save As* area. This will download the file in the same way that you download any other file from the internet. Many browsers default to store downloaded files into the user's *Downloads* folder but is usually also visible within the browser. As a final step, move the the file you've just downloaded into the appropriate Presets folder used by your Orba app and then load the new Preset into your Orba in the regular way. 

Watch the Demo video below to better understand the workflow.

## Orba Update Thumbnail Script
This script makes it easy to change the thumbnail image for any *.orbapreset* file. The Orba app installs the Preset voices in the following locations:

**PC:**
```
C:\Users\[user account]\AppData\Roaming\Artiphon\Orba\Presets\
```
**Mac:**
```
/Users/<your_user>/Library/Artiphon/Orba/Presets/
```

### USAGE:
**PC:**
```
.\OrbaUpdateThumbnail.ps1 [orbapreset file] [png file]
```
**Mac:**
```
./OrbaUpdateThumbnail.sh [orbapreset file] [png file]
```
The script will update the *.orbapreset* file at the specified path and replace the encoded thumbnail image with the one specified at the png file path. **NOTE:** The png file must be a valid png file with the dimensions 120px x 120px. There are many ways to resize your images but both Windows and Mac come with included software to do this. Windows users can crop/resize using Paint3D and Mac users can crop/resize using Preview.

## Demo

https://user-images.githubusercontent.com/3968129/174461267-e6fa73c7-07fe-4922-98ac-c76c3fe31279.mov

## Credits
Special thanks to @BJG145 from the [Orba Hacking Forum](https://artiphon.freshdesk.com/support/discussions/topics/44001013185)
