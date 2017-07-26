#!/bin/sh
set -ex         #Fail if any line fails, print everything

SCRIPTDIR="$(dirname "$0")"

# Copy the service
\cp -rf "$SCRIPTDIR/verne.service" /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Add it to startup
systemctl enable verne.service
