#!/bin/bash

# Polyphrase password generator

# ! Adapt to your local storage path the path below
SCRIPT_PATH="/home/$(whoami)/code/polyphrase/polyphrase.py"

# Generate password and copy to clipboard
python3 $SCRIPT_PATH $@
# | xclip -selection clipboard

# Optional: Show notification
notify-send "Password Generator" "New password copied to clipboard!" 