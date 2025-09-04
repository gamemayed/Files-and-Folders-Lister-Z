#!/bin/bash
# macOS double-clickable launcher for Files and Folders Lister Z GUI
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/lister_z_gui.py" "$@"
