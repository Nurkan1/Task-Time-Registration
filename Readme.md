
# 🚀 Task Time Registration: Elevate Your Productivity Game! 🕒

## Description
**Task Time Registration** is a Python application crafted to revolutionize the way we monitor computer usage, offering a deeper insight into your productivity patterns. This tool is designed not just to track time but to master it, by seamlessly monitoring mouse and keyboard activity and distinguishing between active and inactive periods with precision.

## Key Features

### Intelligent Activity Tracking
Tracks your mouse and keyboard activity, distinguishing between active and inactive periods with a 5-minute threshold. This ensures every second of usage is accounted for, providing you with a detailed view of your productivity.

### Effortless Record Keeping
Automatically creates a dedicated folder titled "Task Time Registration" on your system for storing all task logs neatly in their own txt files, making it easy for you to review and analyze your productivity patterns anytime.

### Live Updates
The application updates your activity logs every minute, giving you real-time insights into your active and inactive times and helping you identify productivity trends to adjust your work habits accordingly.

## Installation
Ensure you have Python 3 installed on your system. Install all dependencies listed in the `requirements.md` file using pip:

```
pip install -r requirements.md
```

## Usage
Execute the script from the command line to start tracking:

```
python Task_Time.py
```

## Compiling to an Executable (Windows)
To compile the script into a standalone executable for Windows, use PyInstaller. This allows for distribution and execution without needing Python installed on the target machine.

```
pyinstaller --onefile --hidden-import pynput --icon=dpi.ico Task_Time.py
```

*Note: Ensure you have `pyinstaller` installed. Replace `dpi.ico` with the path to your own icon file to customize the executable's icon.*

## Author
**Nurcan** - A passionate inventor, technology enthusiast, and software developer. Always exploring the boundaries of creativity and technology to enhance everyday productivity and