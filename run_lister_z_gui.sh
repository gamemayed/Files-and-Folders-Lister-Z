#!/bin/bash
# Launcher for Files and Folders Lister Z GUI (Linux/macOS)

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3."
    exit 1
fi

# Launch the GUI script
python3 "$(dirname "$0")/lister_z_gui.py" "$@"
