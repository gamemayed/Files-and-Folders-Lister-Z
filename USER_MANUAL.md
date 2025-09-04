# Files and Folders Lister Z - User Manual

## Overview
Files and Folders Lister Z is a utility for listing the contents of directories on your computer. It provides both a command-line and a graphical user interface (GUI) for easy use.

## How to Use

### 1. Using the GUI
**Windows:**
- Double-click `lister_z_gui.exe` to launch the graphical interface.

**Linux/MacOS:**
- Run the shell script:
  ```
  ./run_lister_z_gui.sh
  ```
- Or on MacOS, double-click `Lister Z GUI.command`.

Select the folder you want to list using the provided options.
Choose your desired output format (e.g., text, CSV).
Click the button to generate the list.
Save or copy the results as needed.

### 2. Using the Command Line
**Windows:**
- Open a command prompt or PowerShell window.
- Run the script with Python:
  ```
  python lister_z.py [options]
  ```
- Or use the provided batch file:
  ```
  run_lister_z.cmd
  ```

**Linux/MacOS:**
- Run the shell script:
  ```
  ./run_lister_z.sh
  ```
- Or on MacOS, double-click `Lister Z.command`.

Follow the on-screen prompts or use command-line arguments to specify the folder and output options.

## Features
- List all files and folders in a selected directory.
- Export results to various formats.
- Simple and intuitive interface.

## Notes
- Requires Python to run the `lister_z.py` and `lister_z_gui.py` scripts.
- For the GUI version on Windows, use the `lister_z_gui.exe` file for convenience (no Python required).
- For Linux/macOS, use the provided launch scripts: `run_lister_z.sh`, `run_lister_z_gui.sh`, `Lister Z.command`, or `Lister Z GUI.command`.
- See `README.md` for more details and advanced options.

For support or more information, refer to the project README or contact the developer.