#!/usr/bin/env python

import re


class SampleSet:
    MUSIC_NOTES = [('C', ''), ('C#', 'Db'), ('D', ''), ('D#', 'Eb'), ('E', 'Fb'), ('E#', 'F'), ('F#', 'Gb'),
                   ('G', ''), ('G#', 'Ab'), ('A', ''), ('A#', 'Bb'), ('B', ''), ('B#', '')]
    DYNAMIC_TO_VELOCITY = {'ppp': 16, 'pp': 33, 'p': 49, 'mp': 64, 'mf': 80, 'f': 96, 'ff': 112, 'fff': 127}

    def __init__(self, fn):
        self._filename = fn

        # Establish defaults
        self._name = ''
        self._note = ''
        self._velocity = 80
        self._loop_start = 0
        self._loop_end = 0
        self._uuid = None
        self._midi_note = None
        self._sample_index = None
        self._subdirectory = None

        note_pattern = re.compile('^[A-G][#|b]?[0-9]')
        uuid_pattern = re.compile('^[a-f0-9]{32}')
        tokens = fn.split('_')

        # Build the name property
        for idx, x in enumerate(tokens):
            if not note_pattern.match(x):
                self._name += (x + "_")
            else:
                self._name = self._name[:-1]
                break

        # If Note was not supplied, return a default SampleSet
        if self._name.endswith(".wav_"):
            self._name = self._name[:-5]
            return
        else:
            self._note = tokens[idx].split('.wav')[0]
            if idx + 1 == len(tokens):
                return

        # Parse the rest of the tokens
        if not tokens[idx + 1].endswith('.wav'):
            self._velocity = self.parse_velocity(tokens[idx + 1])
            if not tokens[idx+2].endswith('.wav'):
                self._loop_start = int(tokens[idx + 2])
                if not tokens[idx+3].endswith('.wav'):
                    self._loop_end = int(tokens[idx + 3])
                    if uuid_pattern.match(tokens[idx + 4]):
                        self._uuid = tokens[idx + 4][:-4]
                else:
                    if uuid_pattern.match(tokens[idx + 3]):
                        self._uuid = tokens[idx + 3][:-4]
                    else:
                        self._loop_end = int(tokens[idx + 3][:-4])
            else:
                if uuid_pattern.match(tokens[idx + 2]):
                    self._uuid = tokens[idx + 2][:-4]
                else:
                    self._loop_start = int(tokens[idx + 2][:-4])
        else:
            self._velocity = self.parse_velocity(tokens[idx + 1][:-4])

    @property
    def filename(self):
        return self._filename

    @property
    def name(self):
        return self._name

    @property
    def note(self):
        return self._note

    @property
    def velocity(self):
        return self._velocity

    @property
    def loop_start(self):
        return self._loop_start

    @property
    def loop_end(self):
        return self._loop_end

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, u):
        left_of_uuid = self._filename[:-4] if self._uuid is None else self._filename[:-37]
        self._uuid = u
        self._filename = left_of_uuid + '_' + self._uuid + '.wav'

    @property
    def sample_index(self):
        return self._sample_index

    @sample_index.setter
    def sample_index(self, i):
        self._sample_index = i

    @property
    def subdirectory(self):
        return self._subdirectory

    @subdirectory.setter
    def subdirectory(self, sd):
        self._subdirectory = sd

    @property
    def midi_note(self):
        if not self._note == '':
            return 12 * (int(self._note[-1])+1) + [idx for idx, n in enumerate(SampleSet.MUSIC_NOTES)
                                                   if self._note[:-1] in n][0]

    @property
    def pitch(self):
        if self.midi_note:
            return 440.0 * pow(2, (self.midi_note-69)/12)

    def parse_velocity(self, v):
        try:
            return int(v)
        except ValueError:
            pass
        try:
            return self.DYNAMIC_TO_VELOCITY[v]
        except KeyError:
            return self._velocity

    def __repr__(self):
        template = """      <SampledSound sampleIndex="{Index}" name="{Name}" loopStart="{LoopStart}" loopEnd="{LoopEnd}"
                    pitch="{Pitch}" fileName="{Filename}"
                    subdirectory="{Subdirectory}" pool="User"/>"""

        return template.format(Index=self.sample_index, Name=self.name,
                               LoopStart=self.loop_start, LoopEnd=self.loop_end,
                               Pitch=self.pitch, Filename=self.filename, Subdirectory=self.subdirectory)