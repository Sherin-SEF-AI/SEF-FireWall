# SEF-FireWall
Python GUI application for Linux FireWall

# SEF FireWall

## Project Overview

SEF FireWall is a Python application built using PyQt5 for managing firewall rules on Linux systems. It provides a user-friendly graphical interface to perform common firewall operations such as displaying, adding, and removing rules, as well as enabling or disabling the firewall.

## Features

- **View Firewall Rules**: Display all current firewall rules.
- **Manage Rules**: Add or remove firewall rules with customizable parameters.
- **Enable/Disable Firewall**: Toggle the firewall status.
- **Save/Load Configuration**: Save the current firewall configuration or load a previously saved configuration.
- **Custom Command Execution**: Execute any `iptables` command directly.
- **Clear Output**: Clear the output display area.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Sherin-SEF-AI/SEF-FireWall.git
   cd SEF-FireWall

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


Building an Executable
To convert the Python script to a standalone Linux executable:

Install PyInstaller

bash
Copy code
pip install pyinstaller
Build the Executable

bash
Copy code
pyinstaller --onefile --windowed firewall_app.py
