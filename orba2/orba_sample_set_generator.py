#!/usr/bin/env python

import os
import re
import argparse
from itertools import groupby
from operator import attrgetter


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
            if (idx + 1 == len(tokens)):
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
        template = """  <SampledSound sampleIndex="{Index}" name="{Name}" loopStart="{LoopStart}" loopEnd="{LoopEnd}"
                pitch="{Pitch}" fileName="{Filename}"
                subdirectory="{Subdirectory}" pool="User"/>"""

        return template.format(Index=self.sample_index, Name=self.name,
                               LoopStart=self.loop_start, LoopEnd=self.loop_end,
                               Pitch=self.pitch, Filename=self.filename, Subdirectory=self.subdirectory)


def main(args):
    files = os.listdir(args.samplePath)
    subdirectory = os.path.basename(os.path.abspath(args.samplePath))
    sorted_sample_sets = sorted([(SampleSet(f)) for f in files], key=lambda x: (x.midi_note, x.velocity))

    # Inject the indexes and subdirectory info
    for idx, ss in enumerate(sorted_sample_sets):
        ss.sample_index = idx
        ss.subdirectory = subdirectory

    # Setup Lists based on the collection of sample sets
    grouped_by_notes = [list(g) for _, g in groupby(sorted_sample_sets, attrgetter('midi_note'))]
    sm = [[i.sample_index for i in j] for j in grouped_by_notes]
    sv = [[i.velocity for i in j] for j in grouped_by_notes]
    vt = [list([int(i * 0.5) for i in map(sum, zip(*t))]) for t in zip([x[1:] for x in sv], [x[:-1] for x in sv])]

    # Format Output strings
    note_thresholds = ','.join([str(ss.midi_note) for ss in sorted_sample_sets][:-1])
    velocity_thresholds = str(vt)[1:-1].replace(" ", "").replace("],[", "][")
    sample_map = str(sm)[1:-1].replace(" ", "").replace("],[", "][")
    template = """<SampleSet name="{Name}" noteThresholds="{NT}"
           velocityThresholds="{VT}" sampleMap="{SM}">"""

    # Print out the SampleSet node
    print(template.format(Name=subdirectory, NT=note_thresholds, VT=velocity_thresholds, SM=sample_map))
    print(*sorted_sample_sets, sep='\n')
    print("</SampleSet>")

    return


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument('samplePath', help='AbsolutePath to the samples folder.', type=str)

    # Optional arguments
    # parser.add_argument('-u', help='Updates/Adds a UUID to the .wav files and output', action='store_true')

    # Print version
    parser.add_argument('--version', action='version', version='%(prog)s - Version 0.92')

    # Parse arguments
    args = parser.parse_args()

    # Raw print arguments
    # print("You are running the script with arguments: ")
    # for a in args.__dict__:
    #     print(str(a) + ": " + str(args.__dict__[a]))

    return args


if __name__ == '__main__':
    main(parse_arguments())
