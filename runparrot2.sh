#!/bin/bash
cd /home/pi/parrotai

echo running the parrot as service
echo about to determine whether pulseaudio is up and running
arecord -l
pulseaudio --check
pulseaudio -D
echo user: $USER

#/home/pi/parrotai/parrotMain.py
/home/pi/parrotai/parrotMain.py; exec bash;
#xterm -hold -e /home/pi/parrotai/parrotMain.py
#sudo DISPLAY=:0 xterm -hold -e /home/pi/parrotai/parrotMain.py


