#!/usr/bin/env python

import os
import re
import glob
import hashlib
import pathlib
import argparse
import time
from shutil import copy, rmtree, copytree, make_archive
from itertools import groupby
from operator import attrgetter
from collections import OrderedDict
from classes.artipreset import SampleSet
from classes.orba_utils import deploy_preset, remove_preset


def main(args):
    # Build relevant collections and base names
    files = [os.path.basename(x) for x in glob.glob(os.path.abspath(args.samplePath) + '/*.wav')]
    sorted_sample_sets = sorted([(SampleSet(f)) for f in files], key=lambda x: (x.midi_note, x.velocity))
    subdirectory = os.path.basename(os.path.abspath(args.samplePath))
    sample_set_name = subdirectory
    os.system("")
    # orba_home = None

    # Append a uuid to the sample directory if this flag is set
    if args.b:
        subdirectory += '_' + hashlib.md5(subdirectory.encode('utf-8')).hexdigest()

    # Inject the indexes and subdirectory.
    for idx, ss in enumerate(sorted_sample_sets):
        ss.sample_index = idx
        ss.subdirectory = subdirectory
        # If this flag is present, add the uuid
        if args.b:
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
    if not args.s:
        print(sample_set_node)

    # Build the Preset files & folder structure if this flag is set
    if args.b:
        print('{}Build{}: Evaluating assets.'.format('\033[94m', '\033[0m'))
        # Remove any previous versions
        rmtree(os.path.abspath(args.samplePath) + '/Common', ignore_errors=True)

        # Read the content from the .artipreset file
        artipreset_files = glob.glob(os.path.abspath(args.samplePath) + '/*.artipreset')
        artipreset_filename = os.path.basename(artipreset_files[0]) if len(artipreset_files) > 0 else None

        if not artipreset_filename:
            print('>> No template file was found. Please add an .artipreset template file into the samplePath folder.')
            return
        else:
            # Other .artipreset validations could happen here.
            # For example, check for presence of an existing SampleSet node
            print('>> Template found:', artipreset_filename)

        with open(os.path.abspath(args.samplePath) + '/' + artipreset_filename, 'r') as f:
            content = f.read()

        # Create the 'Presets' folder
        arti_folder = '/Common/Presets/' + re.search('mode="(Drum|Bass|Chord|Lead)', content).groups()[0]
        os.makedirs(os.path.abspath(args.samplePath) + arti_folder, mode=0o777, exist_ok=True)

        # Substitute the new information into the .artipreset content
        artipreset_uuid = hashlib.md5((arti_folder + sample_set_name).encode('utf-8')).hexdigest()
        content = re.sub('(PresetEntry name=".*?")', 'PresetEntry name="' + sample_set_name + '"', content)
        content = re.sub('(SoundPreset name=".*?")', 'SoundPreset name="' + sample_set_name + '"', content)
        content = re.sub('(readOnly=".*?")', 'readOnly="0"', content)
        content = re.sub('(factory=".*?")', 'factory="0"', content)
        content = re.sub('(uuid=".*?")', 'uuid="' + artipreset_uuid + '"', content)
        content = re.sub('( {4}<SampleSet.*</SampleSet>)', sample_set_node, content, flags=re.DOTALL)

        # If this template is a Stem template, make a few more adjustments
        if re.search('(stemArtist)', content):
            print('>> Template is a Stem type')
            tuning = ', '.join(list(OrderedDict.fromkeys([str(ss.midi_note) for ss in sorted_sample_sets])))
            content = re.sub('(tuning=".*?")', 'tuning="' + tuning + '"', content)
            content = re.subn('(pitch=".*?")', 'pitch="-1"', content)[0]

        # Check if a png file is present
        png_files = glob.glob(os.path.abspath(args.samplePath) + '/*.png')
        png_filename = os.path.basename(png_files[0]) if len(png_files) > 0 else None

        # Make all adjustments needed if a .png image has been supplied
        if png_filename:
            print('>> Image found:', png_filename)
            img_uuid = hashlib.md5(png_filename.encode('utf-8')).hexdigest()
            img_filename = png_filename[:-4] + '_' + img_uuid + '.png'
            content = re.sub('(coverImageRef=".*?")', 'coverImageRef="' + img_filename + '"', content)
            img_folder = '/Common/Images/'
            img_file = img_folder + img_filename
            os.makedirs(os.path.abspath(args.samplePath) + img_folder, mode=0o777, exist_ok=True)
            copy(os.path.join(os.path.abspath(args.samplePath), png_filename),
                 os.path.join(os.path.abspath(args.samplePath) + img_folder, img_filename))
        else:
            default_img = 'User_16b5545b4f1b42379c14815d73209225.png'
            content = re.sub('(coverImageRef=".*?")', 'coverImageRef="' + default_img + '"', content)

        # Write the altered content back to the new .artipreset file
        arti_file = arti_folder + '/' + sample_set_name + '_' + artipreset_uuid + '.artipreset'
        with open(os.path.abspath(args.samplePath) + arti_file, 'w') as f:
            f.write(content)

        # Create a 'SamplePools' folder and appropriate subfolders
        wav_folder = '/Common/SamplePools/User/' + subdirectory
        os.makedirs(os.path.abspath(args.samplePath) + wav_folder, mode=0o777, exist_ok=True)

        # Copy the .wav files (with their uuids appended) into the new folder
        for ss in sorted_sample_sets:
            copy(os.path.join(os.path.abspath(args.samplePath), ss.filename[:-37] + '.wav'),
                 os.path.join(os.path.abspath(args.samplePath) + wav_folder, ss.filename))

        print('{}Build{}: Preset complete.'.format('\033[94m', '\033[0m'))

        if args.z:
            print('{}Zip{}: Archive created.'.format('\033[94m', '\033[0m'))
            make_archive(os.path.abspath(args.samplePath) + '/' + sample_set_name, 'zip',
                         os.path.abspath(args.samplePath), 'Common')

        # Deploy the Preset files & folder structure if this flag is set
        if args.d:
            deploy_preset(os.path.abspath(args.samplePath) + '/Common/')
            # src = os.path.abspath(args.samplePath) + '/Common/'
            # dst = str(pathlib.Path.home()) + '/Documents/Artiphon/Common/'
            # print('{}Deploy{}: Adding files to'.format('\033[94m', '\033[0m'), dst)
            # copytree(src, dst, ignore=None, copy_function=copy, dirs_exist_ok=True)
            #
            # print('{}Deploy{}: Adding files to Orba'.format('\033[94m', '\033[0m'))
            # orba_home, err = connect_to_orba()
            # if err:
            #     print(err)
            #
            # # Deploy onto the Orba if found
            # if orba_home:
            #     time.sleep(2)  # Appears to be a waiting period until file system is fully accessible.
            #     src = os.path.abspath(args.samplePath) + '/Common/Presets/'
            #     dst = orba_home + 'Presets/'
            #     copytree(src, dst, ignore=None, copy_function=copy, dirs_exist_ok=True)
            #     src = os.path.abspath(args.samplePath) + '/Common/SamplePools/'
            #     dst = orba_home + 'SamplePools/'
            #     copytree(src, dst, ignore=None, copy_function=copy, dirs_exist_ok=True)
            #
            # # Need to investigate a better way of monitoring end of file I/O
            # disconnect_orba()

        # Remove the Preset if this flag is set
        if args.r:
            remove_preset(img_file, arti_file, wav_folder)

            # # Remove the Preset from the Artiphon User Preset location
            # dst = str(pathlib.Path.home()) + '/Documents/Artiphon'
            # print('{}Remove{}: Removing files from'.format('\033[94m', '\033[0m'), dst)
            # if os.path.isfile(dst + img_file):
            #     os.remove(dst + img_file)
            # if os.path.isfile(dst + arti_file):
            #     os.remove(dst + arti_file)
            # if os.path.exists(dst + wav_folder):
            #     rmtree(dst + wav_folder, ignore_errors=True)

            # # Remove the Preset from the Orba
            # print('{}Remove{}: Removing files from Orba'.format('\033[94m', '\033[0m'))
            # orba_home, err = connect_to_orba()
            # if err:
            #     print(err)
            #
            # if orba_home:
            #     if os.path.isfile(orba_home + arti_file[8:]):
            #         os.remove(orba_home + arti_file[8:])
            #     if os.path.isfile(orba_home + arti_file[8:-11] + '.crc'):
            #         os.remove(orba_home + arti_file[8:-11] + '.crc')
            #     if os.path.exists(orba_home + wav_folder[8:]):
            #         rmtree(orba_home + wav_folder[8:], ignore_errors=True)
            #
            # # Need to investigate a better way of monitoring end of file I/O
            # disconnect_orba()

    return


def files_only(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument('samplePath', help='path to the samples folder.', type=str)

    # Optional arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', help='deploy the content to the Artiphon folder and Orba.', action='store_true')
    group.add_argument('-r', help='remove the content to the Artiphon folder and Orba.', action='store_true')
    parser.add_argument('-b', help='build the Preset folder structure and files.', action='store_true')
    parser.add_argument('-s', help='suppress SampleSet node output to screen.', action='store_true')
    parser.add_argument('-z', help='zip the contents of the Common folder.', action='store_true')
    # parser.add_argument('-a', '--artipreset', nargs='?', const='arg_was_not_given',
    #                     help='path to an .artipreset file to use as starting template')

    # Print version
    parser.add_argument('--version', action='version', version='%(prog)s - Version 0.98')

    # Parse arguments
    args = parser.parse_args()

    # Raw print arguments
    # print("You are running the script with arguments: ")
    # for a in args.__dict__:
    #     print(str(a) + ": " + str(args.__dict__[a]))

    return args


if __name__ == '__main__':
    main(parse_arguments())
