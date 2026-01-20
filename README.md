# CamJam Edukit 3 - Robotics

![CamJam EduKit 3 - Robotics](http://camjam.me/wp-content/uploads/2015/09/Edukit3_1500-Alex-Eames-sm.jpg)

The code contained within this repository is for use with the CamJam Edukit 3 - Robotics, created by the organisers of The Cambridge Raspberry Jam (http://camjam.me), an event for fans of the Raspberry Pi.

There are two versions of the instructions:

* GPIO Zero - using the easy-to-use GPIO Zero library to control the GPIO Pins
* RPi.GPIO - the original and more complex way of controlling GPIO Pins. These worksheets are no longer supported; we advise you to use the GPIO Zero versions.

The kit costs only £20 including UK VAT, and is available from [The Pi Hut](http://thepihut.com/collections/camjam-edukit)

## Required Libraries

### GPIO Zero Version
The GPIO Zero worksheets require:
- `gpiozero` - GPIO Zero library for Raspberry Pi
- `smbus2` - SMBus access for I2C devices (used by sun sensor scripts)

Install using a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install gpiozero smbus2
```

On Raspberry Pi OS, you can also install system packages:
```bash
sudo apt install python3-gpiozero python3-smbus
```

### VS Code Setup
If using VS Code, select the virtual environment interpreter:
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose `.venv/bin/python` from the list