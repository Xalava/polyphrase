#!/bin/bash

# Polyphrase password generator

# ! Adapt to your local storage path the path below
SCRIPT_FOLDER="/home/$(whoami)/code/polyphrase/"

# Generate password and copy to clipboard
(cd $SCRIPT_FOLDER && python3 polyphrase.py $@ )
# | xclip -selection clipboard

# Optional: Show notification
notify-send "Password Generator" "New password copied to clipboard!" 