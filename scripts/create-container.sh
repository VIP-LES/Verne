#!/bin/sh
set -ex         #Fail if any line fails, print everything

docker create --name=verne --device /dev/ttyAMA0 --device /dev/i2c-1 -v /home/pi/vernedata:/data gtviples/verne