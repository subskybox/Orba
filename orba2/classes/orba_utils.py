#!/usr/bin/env python

import glob
import time
import platform
import subprocess
from string import ascii_uppercase


def disconnect_orba():
    # Wait for file I/O to complete
    time.sleep(3)

    # Re-Query for the Serial Port as it can change
    serial_port = find_serial_port()

    # Disconnect from Orba
    if serial_port:
        send_MSC(serial_port)


def find_orba_drive():
    timeout_start = time.time()
    orba_drive = ''
    if platform.uname().system == 'Windows':
        # Windows
        print('>> Attempting to connect to Orba', end='')
        while not len(glob.glob(orba_drive + ':/Presets')) and (time.time() < timeout_start + 5):
            print('.', end='')
            time.sleep(1)
            for orba_drive in ascii_uppercase:
                if len(glob.glob(orba_drive + ':/Presets')):
                    print()
                    return orba_drive + ':/', None
    else:
        # MacOS
        print('>> Attempting to connect to Orba', end='')
        while not len(glob.glob('/Volumes/NO NAME/')) and (time.time() < timeout_start + 5):
            print('.', end='')
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
            print('>> Failed to find Serial Port')
            return None
        else:
            return proc.stdout
    else:
        # Find Mac Serial Port
        serial_ports = glob.glob('/dev/cu.usbmodem*')

        if len(serial_ports):
            return serial_ports[0]
        else:
            print('>> Failed to find Serial Port')
            return None


def send_MSC(serial_port):
    if platform.uname().system == 'Windows':
        cmd = 'set /p x="M" <nul >\\\\.\\' + serial_port
    else:
        cmd = 'echo M > ' + serial_port
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def connect_to_orba():
    serial_port = find_serial_port()
    if serial_port:
        # Attempt to connect to Orba
        send_MSC(serial_port)
        orba_home, err = find_orba_drive()

        if err:
            return None, '>> Orba NOT accessible. Try turning it off and then back on.'
        else:
            return orba_home, err
    return None, '>> Orba NOT accessible. Try turning it off and then back on.'

