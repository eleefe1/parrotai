#!/bin/bash
cd /home/pi/parrotai

echo running the parrot as service
echo about to determine whether pulseaudio is up and running
arecord -l
pulseaudio --check
echo user: $USER

sudo DISPLAY=:0 xterm -hold -e /home/pi/parrotai/parrotMain.py
#xterm -hold -e /home/pi/parrotai/parrotMain.py


