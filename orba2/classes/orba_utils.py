#!/usr/bin/env python

import glob
import time
import subprocess


def disconnect_orba():
    modems = glob.glob('/dev/cu.usbmodem*')

    if len(modems):
        time.sleep(3)
        cmd = 'echo M > ' + modems[0]
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print('>> Orba Reset.')
    return


def connect_to_orba():
    modems = glob.glob('/dev/cu.usbmodem*')

    if len(modems):
        cmd = 'echo M > ' + modems[0]
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    else:
        return None, '>> Orba not connected.'

    timeout_start = time.time()
    print('>> Attempting to connect to Orba', end='')

    while not len(glob.glob('/Volumes/NO NAME/')) and (time.time() < timeout_start + 10):
        print('.', end='')
        time.sleep(1)

    print()

    if len(glob.glob('/Volumes/NO NAME/')):
        orba_root = glob.glob('/Volumes/NO NAME/')[0]
        print('>> Connected to Orba.')
        return orba_root, None
    else:
        return None, '>> Orba NOT accessible. Try turning it off and then back on.'

