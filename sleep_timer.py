#!/usr/bin/env python
from __future__ import print_function
import argparse
import datetime as dt
import subprocess
import sys
import textwrap
import time

from Xlib.display import Display
from Xlib import X


def sleep_screen():
    print('')
    display = Display(':0')
    root = display.screen().root
    root.grab_pointer(True,
            X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask,
            X.GrabModeAsync, X.GrabModeAsync, 0, 0, X.CurrentTime)
    root.grab_keyboard(True,
            X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

    subprocess.call('xset dpms force off'.split())
    p = subprocess.Popen('gnome-screensaver-command -i'.split())

    while True:
        # print display.next_event()
        p.terminate()
        break

    subprocess.call('amixer set Master mute'.split())
    print('\nHave a nice rest! Signing out until dawn ({}).'.format(
        dt.datetime.now()))
    subprocess.call(
        'gsettings set org.gnome.desktop.session idle-delay 60'.split())
    print('\\' * 36 + '|' * 8 + '/' * 36)
    print('\\' * 38 + '|' * 4 + '/' * 38)
    print('\\' * 40 + '/' * 40)


def print_greeting(now, minutes):
    print('/' * 40 + '\\' * 40)
    print('/' * 38 + '|' * 4 + '\\' * 38)
    print('/' * 36 + '|' * 8 + '\\' * 36)
    print(textwrap.fill(
        str('It\'s currently {now}. Watching TV already you lazy bum? ' +
            'Setting the screen to sleep in {minutes} minutes. ' +
            'Enjoy!!!').format(
            now=now, minutes=minutes), 80))
    print('')

def arg_parse():
    parser = argparse.ArgumentParser(
        description=(
            'Sleep timer that mutes the computer and shuts off ' +
            'the displays after a specified number of minutes or hours. ' +
            'The program defaults to 120 minutes (2 hours).'))
    parser.add_argument(
        'minutes', type=float, metavar='N', default=120, nargs='?',
        help='Number of minutes to sleep')
    parser.add_argument(
        '--hours', type=float, metavar='N', default=None,
        help='Number of minutes to sleep. Overrides seconds and default.')
    args = parser.parse_args()

    if args.hours:
        args.minutes = args.hours * 60.

    return args


if __name__ == '__main__':
    args = arg_parse()
    
    seconds = int(args.minutes * 60)
    progress_message = (
        '\r{percent:02%} of {minutes} mins passed. {remain:.2f} mins remain.')

    print_greeting(dt.datetime.now(), args.minutes)

    # Set the screen to NEVER sleep to override system settings
    subprocess.call(
        'gsettings set org.gnome.desktop.session idle-delay 0'.split())
    for i in xrange(seconds):
        time.sleep(1)
        sys.stdout.write(progress_message.format(
            percent=float(i) / seconds,
            minutes=int(args.minutes),
            remain=float(args.minutes) - i / 60.))
        sys.stdout.flush()

    sys.exit(sleep_screen())
