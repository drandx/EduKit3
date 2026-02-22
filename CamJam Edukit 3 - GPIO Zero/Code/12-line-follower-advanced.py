# CamJam EduKit 3 - Robotics
# Advanced Line Following Robot with Ambient Light Tracking
#
# Uses the TCRT5000 IR line detector sensor to follow a black line
# and the SunSensor (VCNL4200) to track average ambient light levels.
# The robot adjusts its speed based on lighting conditions:
#   - Bright light  → full speed
#   - Dim light     → reduced speed for caution

import os
import time
from gpiozero import CamJamKitRobot, LineSensor
from sunsensor import SunSensor

# Set variables for the line detector GPIO pin
pinLineFollower = 25

linesensor = LineSensor(pinLineFollower)
robot = CamJamKitRobot()
sensor = SunSensor()

# Base motor speeds (0.0 to 1.0)
leftmotorspeed = 0.5
rightmotorspeed = 0.5

# Light-based speed scaling
# Below this light level the robot will slow down
DimLightThreshold = 500
# Minimum speed multiplier when it's dark (30% of base speed)
MinSpeedMultiplier = 0.3

# Rolling average window size for light readings
LightWindowSize = 20

# State flags
direction = True    # The direction the robot will turn - True = Left
isoverblack = True  # A flag to say the robot can see a black line
linelost = False    # A flag that is set if the line has been lost

# Rolling window of recent light readings
light_readings = []

# Log file – overwritten every run, placed next to this script
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "light_readings.log")
logfile = open(log_path, "w")
logfile.write("timestamp,raw_light,avg_light,speed_multiplier\n")


def update_light():
    """Read the current ambient light and update the rolling average."""
    reading = sensor.light
    light_readings.append(reading)
    if len(light_readings) > LightWindowSize:
        light_readings.pop(0)
    avg = average_light()
    mult = speed_multiplier()
    logfile.write(f"{time.time():.3f},{reading},{avg:.1f},{mult:.3f}\n")
    logfile.flush()


def average_light():
    """Return the average ambient light over the rolling window."""
    if not light_readings:
        return 0
    return sum(light_readings) / len(light_readings)


def speed_multiplier():
    """Calculate a speed multiplier (0.3–1.0) based on average light.

    In bright conditions (above DimLightThreshold) the robot runs at
    full speed.  As light drops toward zero the multiplier scales
    linearly down to MinSpeedMultiplier.
    """
    avg = average_light()
    if avg >= DimLightThreshold:
        return 1.0
    ratio = avg / DimLightThreshold
    return MinSpeedMultiplier + ratio * (1.0 - MinSpeedMultiplier)


def scaled_speeds():
    """Return (left, right) motor speeds scaled by ambient light."""
    m = speed_multiplier()
    return leftmotorspeed * m, rightmotorspeed * m


def motorforward():
    left, right = scaled_speeds()
    return (left, right)


def motorbackward():
    left, right = scaled_speeds()
    return (-left, -right)


def motorleft():
    left, right = scaled_speeds()
    return (left, -right)


def motorright():
    left, right = scaled_speeds()
    return (-left, right)


def lineseen():
    """Called by LineSensor when the line is detected."""
    global isoverblack, linelost
    print("The line has been found.")
    isoverblack = True
    linelost = False
    robot.value = motorforward()


def linenotseen():
    """Called by LineSensor when the line is lost."""
    global isoverblack
    print("The line has been lost.")
    isoverblack = False


def seekline():
    """Search left and right to relocate the black line."""
    global direction, linelost
    robot.stop()

    print("Seeking the line")

    seeksize = 0.25
    seekcount = 1
    maxseekcount = 5

    while seekcount <= maxseekcount:
        seektime = seeksize * seekcount

        if direction:
            print("Looking left")
            robot.value = motorleft()
        else:
            print("Looking right")
            robot.value = motorright()

        starttime = time.time()

        while (time.time() - starttime) <= seektime:
            update_light()
            if isoverblack:
                robot.value = motorforward()
                return True

        robot.stop()
        seekcount += 1
        direction = not direction

    robot.stop()
    print("The line has been lost - relocate your robot")
    linelost = True
    return False


# Tell the program what to do when a line is seen or not seen
linesensor.when_line = lineseen
linesensor.when_no_line = linenotseen

try:
    print("Advanced Line Follower with Light Tracking")
    print(f"Dim light threshold: {DimLightThreshold}")
    print("Press CTRL+C to stop\n")

    robot.value = motorforward()

    report_interval = 2.0  # seconds between light reports
    last_report = time.time()

    while True:
        # Sample ambient light each loop iteration
        update_light()

        # Periodically print light stats
        now = time.time()
        if now - last_report >= report_interval:
            avg = average_light()
            mult = speed_multiplier()
            print(f"Avg light: {avg:.0f}  |  Speed: {mult:.0%}"
                  f"  |  Sensor: {sensor.light}")
            last_report = now

        # Seek the line if lost
        if not isoverblack and not linelost:
            seekline()

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    robot.stop()
    sensor.close()
    logfile.close()
    avg = average_light()
    print(f"\nSession average light: {avg:.0f} (from {len(light_readings)} samples)")
    print(f"Light log saved to: {log_path}")
