#!/bin/sh
set -ex         #Fail if any line fails, print everything

apt-get update
apt-get install python-dev -y

cd /tmp
git clone https://github.com/VIP-LES/RTIMULib2.git

cd RTIMULib2/Linux/python
python setup.py build
python setup.py install
