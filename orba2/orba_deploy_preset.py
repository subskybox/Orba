#!/usr/bin/env python

import argparse
from classes.orba_utils import deploy_preset, remove_preset_structure


# You should be able to deploy and remove Packages (a.k.a multiple Presets in the same zip)
def main(args):
    if args.r:
        remove_preset_structure(args.payloadPath)
    else:
        deploy_preset(args.payloadPath)


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument('payloadPath', help='path to the preset payload. The path should start at the Common '
                                            'folder or reference a .zip file containing the same structure', type=str)

    # Optional arguments
    parser.add_argument('-r', help='remove the content from the Artiphon folder and Orba.', action='store_true')

    # Print version
    parser.add_argument('--version', action='version', version='%(prog)s - Version 0.8')

    # Parse arguments
    args = parser.parse_args()

    # Raw print arguments
    # print("You are running the script with arguments: ")
    # for a in args.__dict__:
    #     print(str(a) + ": " + str(args.__dict__[a]))

    return args


if __name__ == '__main__':
    main(parse_arguments())
