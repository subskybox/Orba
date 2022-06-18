const midiChannels = {0:"Lead",8:"Bass",9:"Drum",15:"Chord"};
const voices = ["Drum", "Bass", "Chord", "Lead"];
const voice = document.getElementById('voice');
const padButtons = document.querySelectorAll(".padButton");
const offsetInputs = document.querySelectorAll(".quantity__input");
const majOffsets = [0,2,4,5,7,9,11,12];
const minOffsets = [0,2,3,5,7,8,10,12];
const midiOctaveMidiNotes = [24,36,48,60,72,84];
var currentVoiceMode = "Chord";
var tableMode = "Offsets";
var currentScaleMode = "Maj";
var cNoteOffset = 48;
var midiAccessGlobal;
var modifierDataArr;
var uploadContent; // A string to hold the contents of the uploaded file.
var doc; // An XMLDocument object which can be parsed, edited and re-serialized.

document.addEventListener("DOMContentLoaded", function(event) { 
	// Load standard chord voicings
	var modifierData="AgAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAQgAAAAEAAAAAAAAAAABAAEAIAAAAAAABwwQAAcMDwAHDA8ABAcQAAQHDAADBwwAAwz8AAQM+wADBwAAAwgAAAQHAAADBwAAAwcAAAQHAAAEBwAAAwcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	loadModifierDataArr(modifierData);
	loadScalesJSON();

	// Request MIDI access
	if (navigator.requestMIDIAccess) {
	    console.log('This browser supports WebMIDI!');

	    // If Chrome removes requestMIDIAccess()[Deprecated], then swap to this line.
	    //navigator.requestMIDIAccess({sysex:true}).then(onMIDISuccess, onMIDIFailure);
	    navigator.requestMIDIAccess().then(onMIDISuccess, onMIDIFailure);

	} else {
	    console.log('WebMIDI is not supported in this browser.');
	}

	offsetInputs.forEach(counter => {
	  counter.addEventListener('change', (e) => {
	    e.preventDefault();
	    var value = counter.value;
	   	if (value < -127) {counter.value = -127;}
	    if (value > 127) {counter.value = 127;}
	    reportNewOffset(counter);
	  });
	});

  	const minusButtons = document.querySelectorAll(".quantity__minus");
  	minusButtons.forEach(minus => {
	  minus.addEventListener('click', (e) => {
	    e.preventDefault();
	    var counter = e.currentTarget.parentNode.getElementsByTagName('input')[0];
	    var value = counter.value;
	    if (value > -127) {value--;}
	    counter.value = value;
	    
	   	if (e.shiftKey) {
		    var i =e.currentTarget.parentNode.parentNode.cellIndex;
		    var inputs = chordOffsetTable.querySelectorAll("tr td:nth-child("+ (i + 1) +") .quantity__input");
		    inputs.forEach( i => { 
		    	i.value = value;
		    	reportNewOffset(i);
		    });
		} else {
			reportNewOffset(counter);
		}
	  });
	});
  
  	const plusButtons = document.querySelectorAll(".quantity__plus");
  	plusButtons.forEach(plus => {
	  plus.addEventListener('click', (e) => {
	    e.preventDefault();
	    var counter = e.currentTarget.parentNode.getElementsByTagName('input')[0];
	    var value = counter.value;
	    if (value < 127) {value++;}
	    counter.value = value;

	    if (e.shiftKey) {
		    var i =e.currentTarget.parentNode.parentNode.cellIndex;
		    var inputs = chordOffsetTable.querySelectorAll("tr td:nth-child("+ (i + 1) +") .quantity__input");
		    inputs.forEach( i => { 
		    	i.value = value;
		    	reportNewOffset(i);
		    });
		} else {
			reportNewOffset(counter);
		}
	  });
	});

  	padButtons.forEach(padButton => {
		padButton.addEventListener('mousedown', (e) => {
			sendPadMidi(e);
		});
		padButton.addEventListener('mouseup', (e) => {
			sendPadMidi(e);
		});
		padButton.addEventListener("keydown", function (e) {
		  e = e || window.event;
		  if (e.repeat) { return }
		  var code = e.keyCode || e.charCode;
		  if (code == 32 || code == 13) { // enter or space
		    sendPadMidi(e);
		  }
		});
		padButton.addEventListener("keyup", function (e) {
		  e = e || window.event;
		  if (e.repeat) { return }
		  var code = e.keyCode || e.charCode;
		  if (code == 32 || code == 13) { // enter or space
		    sendPadMidi(e);
		  }
		});
	});

  	let tableCaption = document.getElementsByClassName('tableCaption')[0];
  	tableCaption.addEventListener('click', (e) => {
		e.preventDefault();
		toggleTableMode();
	});

});

function loadScalesJSON () {
	
	//Load Major scale options
	for (var i = 0; i < scaleOffsets.majorScaleMode.length; i++) {
	    var optgroup = document.createElement("optgroup");
	    var lbl = Object.keys(scaleOffsets.majorScaleMode[i])[0];
	    optgroup.label = lbl;
	    MajScale.appendChild(optgroup);
		for (var j = 0; j < scaleOffsets.majorScaleMode[i][lbl].length; j++) {
			var option = document.createElement("option");
			option.text = Object.keys(scaleOffsets.majorScaleMode[i][lbl][j])[0];
			option.value = scaleOffsets.majorScaleMode[i][lbl][j][option.text];
			if (option.text == "Ioanian") { option.selected = true; }
			MajScale.getElementsByTagName('optgroup')[i].appendChild(option);
		}
	}

	//Load Minor scale options
	for (var i = 0; i < scaleOffsets.minorScaleMode.length; i++) {
	    var optgroup = document.createElement("optgroup");
	    var lbl = Object.keys(scaleOffsets.minorScaleMode[i])[0];
	    optgroup.label = lbl;
	    MinScale.appendChild(optgroup);
		for (var j = 0; j < scaleOffsets.minorScaleMode[i][lbl].length; j++) {
			var option = document.createElement("option");
			option.text = Object.keys(scaleOffsets.minorScaleMode[i][lbl][j])[0];
			option.value = scaleOffsets.minorScaleMode[i][lbl][j][option.text];
			if (option.text == "Aeolian") { option.selected = true; }
			MinScale.getElementsByTagName('optgroup')[i].appendChild(option);
		}
	}
}

// Update modifierData string after an Offset change
function reportNewOffset(c) {
	modifierDataArr[parseInt(c.id) + ((currentScaleMode == "Maj") ? 0 : 32)] = parseInt(c.value);
}

// Send Pad Midi Notes to Orba
function sendPadMidi(e) {
    e.preventDefault();
    var i =e.currentTarget.parentNode.cellIndex;
    var inputs = chordOffsetTable.querySelectorAll("tr td:nth-child("+ (i + 1) +") .quantity__input");
    var chordOffsets = [...inputs].map(x => parseInt(x.value));
    var baseMidiNote = cNoteOffset + parseInt(key.options[key.selectedIndex].value);
	var padBaseNote = (baseMidiNote + ((currentScaleMode == "Maj") ? majOffsets[i - 1] : minOffsets[i - 1]));
	var scaleModeOffset = ((currentScaleMode == "Maj") ? MajScale : MinScale).value.split(',').map( Number )[i-1];
	if (e.type == "mousedown" || e.type == "keydown") {
		if (tableMode == "Offsets") {
			for (let i = 0; i < 4; i++) {
			  var note = padBaseNote + chordOffsets[i];
			  sendMidiNoteOn(note,100);
			  noteOn(note);
			}
		} else {
			sendMidiNoteOn(padBaseNote + scaleModeOffset,100);
			noteOn(padBaseNote + scaleModeOffset);
		}
	} else {
		if (tableMode == "Offsets") {
			for (let i = 0; i < 4; i++) {
			  var note = padBaseNote + chordOffsets[i];
			  sendMidiNoteOff(note,100);
			  noteOff(note);
			}
		} else {
			sendMidiNoteOff(padBaseNote + scaleModeOffset,100);
			noteOff(padBaseNote + scaleModeOffset);
		}
	}
}

// Function to run when requestMIDIAccess is successful
function onMIDISuccess(midiAccess) {
	midiAccessGlobal = midiAccess;
    var inputs = midiAccess.inputs;
    var outputs = midiAccess.outputs;

    // Attach MIDI event "listeners" to each input
    for (var input of midiAccess.inputs.values()) {
        input.onmidimessage = getMIDIMessage;
    }

    //DEBUG with this if there are More Midi devices in the future
    // for (var output of midiAccess.outputs.values()) {
    //     console.log(output);
    // }
}

// Function to run when requestMIDIAccess fails
function onMIDIFailure() {
    console.log('Error: Could not access MIDI devices.');
    alert("Error: Could not access MIDI devices.");
}

// Function to parse the MIDI messages we receive
// For this app, we're only concerned with the actual note value,
// but we can parse for other information, as well
// NOTE: a velocity value might not be included with a noteOff command
function getMIDIMessage(message) {
    var command = message.data[0];
    var note = message.data[1];
    var velocity = (message.data.length > 2) ? message.data[2] : 0;

    //console.log(command, note );

    switch (command) {
        case 153: //DrumOn
        case 152: //BassOn
        case 159: //ChordOn
        case 144: //LeadOn
        	 let channel = parseInt(command)&15;
        	 setVoiceMode(channel);
             noteOn(note);
             break;
        case 137: //DrumOff
        case 136: //BassOff
        case 143: //ChordOff
        case 128: //LeadOff 
             noteOff(note);
             break;
        case 200: //Voice Change
			 setVoiceMode(getKeyByValue(midiChannels,voices[note]));
    	 	 break;
	 	case 176: //Controller Message (with value 123) sent after Orba App Uploads Preset Voice to Orba
	 		 // console.log('Patch Loaded'); 
    }
}

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}

function setVoiceMode(c) {

	 if (currentVoiceMode == midiChannels[c]) {
	 	return;
	 }

	 currentVoiceMode = midiChannels[c];
     voice.textContent = currentVoiceMode;
     voice.className = currentVoiceMode.toLowerCase();

     let container = document.getElementsByClassName('container')[0];
     
     switch (currentVoiceMode) {
     	case "Drum":
			container.classList.add('fadeOut');
			break;
		case "Bass":
		case "Lead":
			container.classList.remove('fadeOut');
			setTableMode("Scales");
			break;
		case "Chord":
			container.classList.remove('fadeOut');
			setTableMode("Offsets");
			break;
     }
}

function toggleTableMode() {
	if (tableMode == "Scales") {
		setTableMode("Offsets");
	} else {
		setTableMode("Scales");
	}
}

function setTableMode(mode) {

	let voices = document.querySelectorAll('.voice');
	let assignments = document.getElementsByClassName('assignments')[0];
	let tableCaption = document.getElementsByClassName('tableCaption')[0];

	if (mode == "Scales") {
		tableMode = "Scales";
		dataType.textContent = tableCaption.textContent = "Scale Selections";
		voices.forEach( v => { v.classList.add('collapsed'); });
		assignments.classList.add('expanded');
	} else {
		tableMode = "Offsets";
		dataType.textContent = tableCaption.textContent = "Chord Offsets";
		voices.forEach( v => { v.classList.remove('collapsed'); });
		assignments.classList.remove('expanded');
	}
}

function sendMidiNoteOn(pitch, velocity) {
	if (midiAccessGlobal) {
	 const NOTE_ON = 0x90;
	 const device = midiAccessGlobal.outputs.values().next().value;
	 const msgOn = [NOTE_ON, pitch, velocity];
 	 if (device) { device.send(msgOn) };
 	}
}
function sendMidiNoteOff(pitch, velocity) {
	if (midiAccessGlobal) {
	 const NOTE_OFF = 0x80;
	 const device = midiAccessGlobal.outputs.values().next().value;
	 const msgOff = [NOTE_OFF, pitch, velocity];
 	 if (device) { device.send(msgOff) };
 	}
}

// Function to handle noteOn messages (ie. key is pressed)
// Think of this like an 'onkeydown' event
function noteOn(note) {
    //console.log("On: " + note);
	var kbn = document.querySelector('[data-midi-note="' + note + '"]');

	if (kbn) {
		if (kbn.classList.contains('white')) {
			kbn.classList.add('whiteSelected');
		} else {
			kbn.classList.add('blackSelected');
		}
		
	}
}

// Function to handle noteOff messages (ie. key is released)
// Think of this like an 'onkeyup' event
function noteOff(note) {
    //console.log("Off: " + note);
	var kbn = document.querySelector('[data-midi-note="' + note + '"]');

	if (kbn) {
		if (kbn.classList.contains('white')) {
			kbn.classList.remove('whiteSelected');
		} else {
			kbn.classList.remove('blackSelected');
		}
		
	}
}

function setScaleMode(selectObject) {
	var value = selectObject.value;
  	if (value == "Maj") {
  		currentScaleMode = "Maj";
  		selectObject.classList.remove( 'theme-artiphon-minor' );
  		selectObject.classList.add( 'theme-artiphon-major' );
  		offsetInputs.forEach(counter => {
			counter.value = modifierDataArr[parseInt(counter.id)];
	  	});
  	} else {
  		currentScaleMode = "Min";
  		selectObject.classList.remove( 'theme-artiphon-major' );
  		selectObject.classList.add( 'theme-artiphon-minor' );
  		offsetInputs.forEach(counter => {
			counter.value = modifierDataArr[parseInt(counter.id) + 32];
	  	});
  	}
}

// Bind each key to a Click event
const pianoKeys = document.querySelectorAll("li");
  	pianoKeys.forEach(pianoKey => {
	  pianoKey.addEventListener('mousedown', (e) => {
	    sendMidiNoteOn(e.target.getAttribute('data-midi-note'),100);
	  });
	});
	pianoKeys.forEach(pianoKey => {
	  pianoKey.addEventListener('mouseup', (e) => {
	    sendMidiNoteOff(e.target.getAttribute('data-midi-note'),100);
	  });
	});

holder.ondragover = function() {
    this.className = 'hover';
    return false;
};
holder.ondragleave = function() {
    this.className = '';
    return false;
};
holder.ondrop = function(e) {
    this.className = '';
    e.preventDefault();

    var file = e.dataTransfer.files[0];

	if (file.name.endsWith('.orbapreset')) {
		var reader = new FileReader();
    	reader.onload = function(event) {
	        currentFile.textContent = file.name;
	        uploadContent = event.target.result;
	        parseOrbaPresetFile(uploadContent);
    	};
    	reader.readAsText(file);
    	document.getElementById('file_download').value = file.name;

	} else {
		alert('The file selected is not an .orbapreset file.');
	}
};

file_upload.onchange = function(e) {
	var file = e.target.files[0];
    var reader = new FileReader();
	currentFile.textContent = file.name;
    reader.onload = function(event) {
	    currentFile.textContent = file.name;
	    uploadContent = event.target.result;
    };
    reader.readAsText(file);
    document.getElementById('file_download').value = file.name;
};

downloadBtn.onclick = function(e) {
	if (uploadContent) {
		let modifierDataNode = doc.documentElement.getElementsByTagName('ModifierList')[0].firstElementChild;
		var tmpModifierArr, tmpSeekerArr;
		if (tableMode == "Offsets") {
			tmpModifierArr = modifierDataArr.map(x => x << 24 >>> 24);
		} else {
			tmpModifierArr = modifierDataArr.map(x => x);
			for (var i = 0; i < 8; i++) {
				var padMajScaleOffset = MajScale.value.split(',').map( Number )[i];
				var padMinScaleOffset = MinScale.value.split(',').map( Number )[i];
				tmpModifierArr[50+(i*4)] = tmpModifierArr[51+(i*4)] = tmpModifierArr[52+(i*4)] = tmpModifierArr[53+(i*4)] = padMajScaleOffset;
				tmpModifierArr[82+(i*4)] = tmpModifierArr[83+(i*4)] = tmpModifierArr[84+(i*4)] = tmpModifierArr[85+(i*4)] = padMinScaleOffset;
			}
			var remappedArr = tmpModifierArr.map(x => x << 24 >>> 24);
			tmpModifierArr = remappedArr;
		}
		
		tmpModifierArr[0] = 2; // Modify required ModifierData pointers to apply note offsets

		// Modify required SeekerData pointers to apply note offsets
		let seekerDataNode = doc.documentElement.getElementsByTagName('SeekerList')[0].firstElementChild;
		tmpSeekerArr = fromBase64(seekerDataNode.getAttribute('seekerData'));
		tmpSeekerArr[1] = 11;
		tmpSeekerArr[4] = 32;
		seekerDataNode.getAttributeNode('seekerData').value = toBase64(tmpSeekerArr);	

		modifierDataNode.getAttributeNode('modifierData').value = toBase64(tmpModifierArr);
		modifierDataNode.removeAttribute("modifierUuid");
		modifierDataNode.removeAttribute("gestureUuid");
		modifierDataNode.removeAttribute("uuid");
		const serializer = new XMLSerializer();
		uploadContent = serializer.serializeToString(doc);
		download(document.getElementById('file_download').value, uploadContent);

	} else {
		alert('You must choose a Starting Template before you can download the edited .orbapreset file.');
	}	
};

function download(filename, text) {
	var pom = document.createElement('a');
	pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	pom.setAttribute('download', filename);

	if (document.createEvent) {
	    var event = document.createEvent('MouseEvents');
	    event.initEvent('click', true, true);
	    pom.dispatchEvent(event);
	}
	else {
	    pom.click();
	}
}

function toBase64(u8) {
	return btoa(String.fromCharCode.apply(null, u8));
}

function fromBase64(str) {
	return atob(str).split('').map(function (c) { return c.charCodeAt(0); });
}

function loadModifierDataArr (md) {
	modifierDataArr = fromBase64(md).map(x => x << 24 >> 24);
	offsetInputs.forEach(counter => {
	  counter.value = modifierDataArr[counter.id];
	});
}

function parseOrbaPresetFile(xmlStr) {
	const parser = new DOMParser();
	doc = parser.parseFromString(xmlStr, "application/xml");
	var errorNode = doc.querySelector("parsererror");
	if (errorNode) {
	  console.log("error while parsing");
	} else {
	  var modifierDataNode = doc.documentElement.getElementsByTagName('ModifierList')[0].firstElementChild;
	  loadModifierDataArr(modifierDataNode.getAttribute('modifierData'));
	  cNoteOffset = doc.documentElement.getElementsByTagName('TuningEntry')[0].getAttribute('midiOctave');
	  cNoteOffset = midiOctaveMidiNotes[cNoteOffset] || 48;
	}
}