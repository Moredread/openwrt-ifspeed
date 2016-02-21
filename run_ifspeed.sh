#!/bin/sh

DEV=/dev/ttyUSB0

stty -F $DEV cs8 9600 ignbrk -brkint -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
python ifspeed.py > $DEV