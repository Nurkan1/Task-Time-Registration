# Activity Monitor

## Description
This Python script is designed to monitor user activity on a computer, logging active and inactive time based on mouse and keyboard interaction. It's perfect for those looking to track the time spent on various tasks throughout the day.

## Installation
To use this script, you will need Python 3 installed on your system. Ensure all dependencies listed in the `requirements.md` file are installed. You can install them using pip: pip install -r requirements.md

## Usage
Run the script from the command line: python Time_Task.py

## Compiling to an Executable (Windows)
For Windows users, you can compile this script into a standalone executable file using PyInstaller. This allows you to distribute and run it without needing Python installed on the target machine. Use the following command:
pyinstaller --onefile --hidden-import pynput --icon=dpi.ico Task_Time.py



Make sure you have `pyinstaller` installed and replace `dpi.ico` with the path to your own icon file if you wish to customize the executable's icon.

## Features
- Monitors active and inactive time based on keyboard and mouse interaction.
- Task creation for organizing monitoring time.
- Automatic logging of times in task-specific files.

## Author
Nurcan - A technology enthusiast and software developer.



