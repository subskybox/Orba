# Orba Tools

## What is an Orba?
Orba is a musical instrument designed for your hands. It is a synth, looper and controller that lets you create songs with intuitive gestures like tapping, sliding, and waving.
Orba is made by [Artiphon](https://artiphon.com/pages/orba-by-artiphon).
Orba software is avaible in the [Downloads](https://artiphon.com/pages/downloads) section of their website but is known to be fairly feature limited compared to what their customers would like see. For this reason, I am sharing a few Orba Utilities I have built.

## What Utilities have I built?
This repository currently contains 3 Orba Utilities to help you perform advanced changes to your Orba. These 3 utilities help you to edit Preset voices and are listed here:

1. **Orba Virtual Piano**
>> An HTML (Chrome Browser) based virtual piano that interfaces (MIDI-IN | MIDI-OUT) with your Orba
2. **Orba Chord Fiddler**
>> An HTML (Chrome Browser) data modifier that helps you modify Chord Preset voices. This allows you to create custom chords. Almost any chord can be made but not for any Pad.
3. **Orba Update Thumbnail Script**
>> A script to help simplify the task of changing a Preset voice's thumbnail as seen in the Orba App.

## Orba Virtual Piano
A MIDI GUI keyboard that works bidirectionally with Orba! I was surprised that Google Chrome has a native MIDI interface so I was able to not only play the Orba patches from the webpage I made, but also visualize the notes being played on the Orba. This was instrumental(no pun intented) in figuring out what MIDI data was coming out of the Orba.
I was lucky to find Philip Zastrow's [CSS Piano](https://codepen.io/zastrow/pen/kxdYdk) as a starting point. This repo includes *OrbaVirtualPiano.html* which will show you which notes are being emitted from the Orba and will also send MIDI notes to the Orba. (It might even support MIDI from other devices).

To set this up, launch the Orba app and connect to the Orba. Now open the *OrbaVirtualPiano.html* page in the Chrome Browser. You may have to use only a wired connection to get the connection working in both directions. This app is a huge help when trying to design your own chords.

## Orba Chord Fiddler
Each Orba Chord Preset voice contains a string named `ModifierData` that controls voice/note offsets. This utility allows you to modify the characters in the string and quickly deploy them to the Orba App. I have included known behaviors for each character. I'm sure my discoveries are not yet complete!
### USAGE:
Start by launching the *OrbaDeployDaemon*. This can be run from either the Windows Powershell console or the Mac Terminal. An even easier way is to launch it from the file itself. Simply double click the *OrbaDeployDaemon.sh* in your Mac Finder to run it in your Terminal app or right-click *OrbaDeployDaemon.ps1* in Windows and choose 'Run in PowerShell'. You may have to give this script permission since you've downloaded it from the internet.

Once the daemon is listening, open the *OrbaChordFiddler.html* file in the Chrome Browser and adjust the *Offsets*. Click the `View` buttons to see what each character does to the chords. Fiddle Away! I recommend you only change a few offsets at a time as it can be difficult to understand what is going on. For example, setting some voice's offsets to negative offsets can cause the previous voice to lower by a semitone (or more)! This can be an undesired (or sometimes desired) effect.

Once you are ready to hear your changes, click the `DEPLOY` button and wait about 5 seconds. The Orba App should appear. Now you need to manually load the *Disentangle* Chord Preset to your Orba. Once this is done, listen for changes or switch over to the *OrbaVirtualPiano* to see the changes.

Rinse and Repeat. I hope you enjoy...

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


## Credits
Special thanks to @AndreaMannoci, @QuadPlex and especially @BJG145 from the [Orba Hacking Forum](https://artiphon.freshdesk.com/support/discussions/topics/44001013185)
