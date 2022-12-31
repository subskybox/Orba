#!/usr/bin/env python

import os
import re
import glob
import time
import pathlib
import platform
import tempfile
import subprocess
from string import ascii_uppercase
from shutil import rmtree, copytree, copyfile, unpack_archive, ignore_patterns


def disconnect_orba():
    # Wait for file I/O to complete
    time.sleep(3)

    # Re-Query for the Serial Port as it can change
    serial_port = find_serial_port()

    # Disconnect from Orba
    if serial_port:
        send_msc(serial_port)

    print('>> Resetting Orba.')


def find_orba_drive():
    timeout_start = time.time()
    orba_drive = ''
    if platform.uname().system == 'Windows':
        # Windows
        print('>> Attempting to connect to Orba', end='', flush=True)
        while not len(glob.glob(orba_drive + ':/Presets')) and (time.time() < timeout_start + 5):
            print('.', end='', flush=True)
            time.sleep(1)
            for orba_drive in ascii_uppercase:
                if len(glob.glob(orba_drive + ':/Presets')):
                    print()
                    return orba_drive + ':/', None
    else:
        # MacOS
        print('>> Attempting to connect to Orba', end='', flush=True)
        while not len(glob.glob('/Volumes/NO NAME/')) and (time.time() < timeout_start + 5):
            print('.', end='', flush=True)
            time.sleep(1)
        print()

        if len(glob.glob('/Volumes/NO NAME/')):
            orba_root = glob.glob('/Volumes/NO NAME/')[0]
            print('>> Connected to Orba.')
            return orba_root, None

    print()
    return None, '>> Orba NOT accessible. Try turning it off and then back on.'


def find_serial_port():
    if platform.uname().system == 'Windows':
        # Find Windows Serial port
        proc = subprocess.run(
            args=[
                'powershell',
                '-noprofile',
                '-command',
                'Get-CimInstance -Class Win32_SerialPort | Where ProviderType -eq "Modem Device" |'
                'Select DeviceID | Select-Object -ExpandProperty DeviceID'
            ],
            text=True,
            stdout=subprocess.PIPE
        )

        if proc.returncode != 0 or not proc.stdout.strip():
            # Failed to find Serial Port
            return None
        else:
            return proc.stdout
    else:
        # Find Mac Serial Port
        serial_ports = glob.glob('/dev/cu.usbmodem*')

        if len(serial_ports):
            return serial_ports[0]
        else:
            # Failed to find Serial Port
            return None


def send_msc(serial_port):
    if platform.uname().system == 'Windows':
        cmd = 'set /p x="M" <nul >\\\\.\\' + serial_port
    else:
        cmd = 'echo M > ' + serial_port
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def connect_to_orba():
    serial_port = find_serial_port()
    if serial_port:
        # Attempt to connect to Orba
        send_msc(serial_port)
        orba_home, err = find_orba_drive()

        if err:
            return None, '>> Orba NOT accessible. Try turning it off and then back on.'
        else:
            return orba_home, err
    return None, '>> Orba NOT accessible. Try turning it off and then back on.'


def deploy_preset(path_to_payload):
    os.system("")
    tmp_path = None

    if os.path.isfile(path_to_payload) and path_to_payload.endswith('.zip'):
        tmp_path = tempfile.mkdtemp()
        tmp_dir = pathlib.Path(tmp_path)
        unpack_archive(path_to_payload, tmp_path, 'zip')
        path_to_payload = tmp_dir / 'Common'
        print('{}Unzipping{}: Adding files to'.format('\033[94m', '\033[0m'), tmp_dir)
    elif not os.path.exists(path_to_payload) or os.path.basename(os.path.abspath(path_to_payload)) != 'Common':
        print('The specified folder does not seem to contain the preset payload.')
        return None  # What to return?

    # print(path_to_payload)
    src = path_to_payload
    dst = str(pathlib.Path.home()) + '/Documents/Artiphon/Common/'
    print('{}Deploy{}: Adding files to'.format('\033[94m', '\033[0m'), dst)
    copytree(src, dst, ignore=ignore_patterns('.DS_Store'), copy_function=copyfile, dirs_exist_ok=True)

    print('{}Deploy{}: Adding files to Orba'.format('\033[94m', '\033[0m'))
    orba_home, err = connect_to_orba()
    if err:
        print(err)

    # Deploy onto the Orba if found
    if orba_home:
        time.sleep(2)  # Appears to be a waiting period until file system is fully accessible.
        src = os.path.abspath(path_to_payload) + '/Presets/'
        dst = orba_home + 'Presets/'
        copytree(src, dst, ignore=ignore_patterns('.DS_Store'), copy_function=copyfile, dirs_exist_ok=True)
        src = os.path.abspath(path_to_payload) + '/SamplePools/'
        dst = orba_home + 'SamplePools/'
        copytree(src, dst, ignore=ignore_patterns('.DS_Store'), copy_function=copyfile, dirs_exist_ok=True)
        print('>> Copying files to Orba.')

        # Need to investigate a better way of monitoring end of file I/O
        disconnect_orba()
        print('{}Deploy{}: Complete'.format('\033[94m', '\033[0m'))

    if tmp_path is not None and os.path.exists(tmp_path):
        rmtree(tmp_path)


def remove_preset_structure(path_to_payload):
    os.system("")
    tmp_path = None
    if os.path.isfile(path_to_payload) and path_to_payload.endswith('.zip'):
        tmp_path = tempfile.mkdtemp()
        tmp_dir = pathlib.Path(tmp_path)
        unpack_archive(path_to_payload, tmp_path, 'zip')
        path_to_payload = tmp_dir / 'Common'
        print('{}Unzipping{}: Adding files to'.format('\033[94m', '\033[0m'), tmp_dir)
    elif not os.path.exists(path_to_payload) or os.path.basename(os.path.abspath(path_to_payload)) != 'Common':
        print('The specified folder does not seem to contain the preset payload.')
        return None  # What to return?

    # Remove the Preset from the Artiphon User Preset location
    dst = str(pathlib.Path.home() / 'Documents' / 'Artiphon')
    print('{}Remove{}: Removing files from'.format('\033[94m', '\033[0m'), dst)

    img_files = [re.search(r'(/|\\)Common.*.png$', x) for x in
                 glob.glob(os.path.abspath(path_to_payload) + '/**/*.png', recursive=True)]

    for idx, img in enumerate(img_files):
        if os.path.isfile(dst + img[0]):
            # print(idx, dst + img[0])
            os.remove(dst + img[0])

    arti_files = [re.search(r'(/|\\)Common.*.artipreset$', x) for x in
                  glob.glob(os.path.abspath(path_to_payload) + '/**/*.artipreset', recursive=True)]

    # Remove the Preset from the Artiphon User Preset location
    for idx, arti_file in enumerate(arti_files):
        if os.path.isfile(dst + arti_file[0]):
            # print(idx, dst + arti_file[0])
            os.remove(dst + arti_file[0])

    # print(tmp_dir)
    # print(os.path.abspath(tmp_dir / 'SamplePools' / 'User'))

    wav_folders = [os.path.basename(x) for x in
                   glob.glob(os.path.abspath(tmp_dir / 'Common/SamplePools/User') + '*/*', recursive=True)]

    # Remove the wav folders from the Artiphon User Preset location
    for idx, wav_folder in enumerate(wav_folders):
        target = dst + '/Common/SamplePools/User/' + wav_folder
        if os.path.exists(target):
            # print(idx, target)
            rmtree(target, ignore_errors=True)

    # Remove the Preset from the Orba
    print('{}Remove{}: Removing files from Orba'.format('\033[94m', '\033[0m'))
    orba_home, err = connect_to_orba()
    if err:
        print(err)

    if orba_home:
        for idx, arti_file in enumerate(arti_files):
            if os.path.isfile(orba_home + arti_file[0][8:]):
                # print(orba_home + arti_file[0][8:])
                os.remove(orba_home + arti_file[0][8:])
            if os.path.isfile(orba_home + arti_file[0][8:-11] + '.crc'):
                # print(orba_home + arti_file[0][8:-11] + '.crc')
                os.remove(orba_home + arti_file[0][8:-11] + '.crc')

        # Remove the wav folders from the Orba
        for idx, wav_folder in enumerate(wav_folders):
            target = orba_home + 'SamplePools/User/' + wav_folder
            if os.path.exists(target):
                # print(idx, target)
                rmtree(target, ignore_errors=True)

        print('>> Removing files and folders from Orba.')

        # Need to investigate a better way of monitoring end of file I/O
        disconnect_orba()
        print('{}Remove{}: Complete'.format('\033[94m', '\033[0m'))


def remove_preset(img_file, arti_file, wav_folder):
    os.system("")
    # Remove the Preset from the Artiphon User Preset location
    dst = str(pathlib.Path.home()) + '/Documents/Artiphon'
    print('{}Remove{}: Removing files from'.format('\033[94m', '\033[0m'), dst)
    if os.path.isfile(dst + img_file):
        os.remove(dst + img_file)
    if os.path.isfile(dst + arti_file):
        os.remove(dst + arti_file)
    if os.path.exists(dst + wav_folder):
        rmtree(dst + wav_folder, ignore_errors=True)

    # Remove the Preset from the Orba
    print('{}Remove{}: Removing files from Orba'.format('\033[94m', '\033[0m'))
    orba_home, err = connect_to_orba()
    if err:
        print(err)

    if orba_home:
        if os.path.isfile(orba_home + arti_file[8:]):
            os.remove(orba_home + arti_file[8:])
        if os.path.isfile(orba_home + arti_file[8:-11] + '.crc'):
            os.remove(orba_home + arti_file[8:-11] + '.crc')
        if os.path.exists(orba_home + wav_folder[8:]):
            rmtree(orba_home + wav_folder[8:], ignore_errors=True)

        # Need to investigate a better way of monitoring end of file I/O
        disconnect_orba()
        print('{}Remove{}: Complete'.format('\033[94m', '\033[0m'))
