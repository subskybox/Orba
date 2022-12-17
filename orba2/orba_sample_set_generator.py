#!/usr/bin/env python

import os
import re
import glob
import hashlib
import argparse
from shutil import rmtree
from shutil import copyfile
from itertools import groupby
from operator import attrgetter
from collections import OrderedDict
from classes.artipreset import SampleSet

def main(args):
    # Build relevant collections and base names
    files = [os.path.basename(x) for x in glob.glob(os.path.abspath(args.samplePath) + '/*.wav')]
    sorted_sample_sets = sorted([(SampleSet(f)) for f in files], key=lambda x: (x.midi_note, x.velocity))
    subdirectory = os.path.basename(os.path.abspath(args.samplePath))
    sample_set_name = subdirectory

    # Append a uuid to the sample directory if this flag is set
    if (args.artipreset):
        subdirectory += '_' + hashlib.md5(subdirectory.encode('utf-8')).hexdigest()

    # Inject the indexes and subdirectory.
    for idx, ss in enumerate(sorted_sample_sets):
        ss.sample_index = idx
        ss.subdirectory = subdirectory
        # If the -a flag is present, add the uuid
        if(args.artipreset):
            file = os.path.abspath(args.samplePath) + '/' + ss.filename
            with open(file, 'rb') as file_for_uuid:
                ss.uuid = hashlib.md5(file_for_uuid.read()).hexdigest()

    # Setup Lists based on the collection of sample sets
    grouped_by_notes = [list(g) for _, g in groupby(sorted_sample_sets, attrgetter('midi_note'))]
    sm = [[i.sample_index for i in j] for j in grouped_by_notes]
    sv = [[i.velocity for i in j] for j in grouped_by_notes]
    vt = [list([int(i * 0.5) for i in map(sum, zip(*t))]) for t in zip([x[1:] for x in sv], [x[:-1] for x in sv])]

    template = """    <SampleSet name="{Name}" noteThresholds="{NT}"
               velocityThresholds="{VT}" sampleMap="{SM}">"""

    # Format output strings
    note_thresholds = ','.join(list(OrderedDict.fromkeys([str(ss.midi_note) for ss in sorted_sample_sets]))[:-1])
    velocity_thresholds = str(vt)[1:-1].replace(" ", "").replace("],[", "][")
    sample_map = str(sm)[1:-1].replace(" ", "").replace("],[", "][")
    sample_set_node = template.format(Name=sample_set_name, NT=note_thresholds, VT=velocity_thresholds, SM=sample_map)
    sample_set_node += '\n' + '\n'.join(map(str, sorted_sample_sets))
    sample_set_node += '\n' + '    </SampleSet>'

    # Print out the SampleSet node
    print(sample_set_node)

    # Create the Preset files & folder structure if this flag is set
    if (args.artipreset):
        # Remove any previous versions
        rmtree(os.path.abspath(args.samplePath) + '/Common', ignore_errors=True)

        # Read the content from the chosen .artipreset file
        with open(args.artipreset, 'r') as f:
            content = f.read()

        # Create the 'Presets' folder
        arti_folder = '/Common/Presets/' + os.path.basename(os.path.abspath(os.path.dirname(args.artipreset)))
        os.makedirs(os.path.abspath(args.samplePath) + arti_folder, mode=0o777, exist_ok=True)

        # Substitute the new information into the .artipreset content
        artipreset_uuid = hashlib.md5((arti_folder + sample_set_name).encode('utf-8')).hexdigest()
        png_filename = os.path.basename(glob.glob(os.path.abspath(args.samplePath) + '/*.png')[0])
        img_uuid = hashlib.md5(png_filename.encode('utf-8')).hexdigest()
        img_filename = png_filename[:-4] + '_' + img_uuid + '.png'
        sample_set_name += '_' + artipreset_uuid
        content_sub1 = re.sub('(uuid=".*?")', 'uuid="' + artipreset_uuid + '"', content)
        content_sub2 = re.sub('(coverImageRef=".*?")', 'coverImageRef="' + img_filename + '"', content_sub1)
        content_sub3 = re.sub('(    <SampleSet.*</SampleSet>)', sample_set_node, content_sub2, flags=re.DOTALL)

        # Write the altered content back to the new .artipreset file
        with open(os.path.abspath(args.samplePath) + arti_folder + '/' + sample_set_name + '.artipreset', 'w') as f:
            f.write(content_sub3)

        # Create an 'Images' folder and copy in png file with uuid
        img_folder = '/Common/Images/'
        os.makedirs(os.path.abspath(args.samplePath) + img_folder, mode=0o777, exist_ok=True)
        copyfile(os.path.join(os.path.abspath(args.samplePath), png_filename),
                 os.path.join(os.path.abspath(args.samplePath) + img_folder, img_filename))

        # Create a 'SamplePools' folder and appropriate subfolders
        wav_folder = '/Common/SamplePools/User/' + subdirectory
        os.makedirs(os.path.abspath(args.samplePath) + wav_folder, mode=0o777, exist_ok=True)

        # Copy the .wav files (with their uuids appended) into the new folder
        for ss in sorted_sample_sets:
            copyfile(os.path.join(os.path.abspath(args.samplePath), ss.filename[:-37] + '.wav'),
                     os.path.join(os.path.abspath(args.samplePath) + wav_folder, ss.filename))

    return

def files_only(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument('samplePath', help='Path to the samples folder.', type=str)

    # Optional arguments
    # parser.add_argument('-u', help='Updates/Adds a UUID to the .wav files and output', action='store_true')
    parser.add_argument('-a', '--artipreset', nargs='?', const='arg_was_not_given',
                        help='Path to an .artipreset file to use as starting template')

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
