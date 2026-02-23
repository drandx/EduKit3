# Room Explorer Robot
# Drives around a room. When it sees a wall, it turns
# little by little until the way is clear, then keeps going.
# Runs forever until the battery runs out!
# Uses the SunSensor (VCNL4200 proximity sensor).

import time
import random
from datetime import datetime
from gpiozero import CamJamKitRobot
from sunsensor import SunSensor

# Set up the robot and the proximity sensor
robot = CamJamKitRobot()
sensor = SunSensor()

# === Settings you can change ===
TooClose = 90    # How close to a wall before turning (centimeters)
Speed = 0.5        # How fast the robot drives (0.0 to 1.0)
Drift = 0.15       # Make left motor a bit slower so robot goes straight
TurnSpeed = 0.5    # How fast the robot turns (0.0 to 1.0)
TurnStep = 0.5    # How long each little turn lasts (seconds)


# Check how far the wall is (in centimeters)
# If the sensor glitches, assume no wall (keep going)
def wall_distance():
    try:
        return sensor.distance
    except OSError:
        return 150.0


# Turn a little bit at a time until the way is clear
def find_clear_path():
    print(f"Wall ahead! Scanning... Distance: {wall_distance()}" )

    # Pick a direction: left most of the time (works best in a square loop)
    GoLeft = random.choice([True, True, True, False])

    # Keep turning in small steps until the path is clear
    while wall_distance() < TooClose:
        if GoLeft:
            print("  Turning left")
            robot.left(TurnSpeed)
        else:
            print("  Turning right")
            robot.right(TurnSpeed)
        time.sleep(TurnStep)
        robot.stop()
        time.sleep(0.1)  # Short pause so the sensor can measure

    print("  Clear! Going forward.")


# === Logging setup ===
HistoryFile = "explorer_history.txt"  # One line per run (never overwritten)
LightFile = "explorer_light.txt"     # Light reading every 10 seconds
LightInterval = 10  # Seconds between light readings


# === Main program - runs forever! ===
try:
    StartTime = datetime.now()

    # Append start time to history (never overwritten)
    try:
        StartLight = sensor.light
    except OSError:
        StartLight = 0
    history = open(HistoryFile, "a")
    history.write(str(StartTime) + " | Light: " + str(StartLight) + "\n")
    history.flush()
    history.close()

    # Open the light log (overwrites each run)
    lightlog = open(LightFile, "w")
    lightlog.write("Started: " + str(StartTime) + "\n")
    lightlog.flush()

    print("Room Explorer starting!")

    LastLightTime = time.time()

    while True:
        # Drive forward (left wheel, right wheel)
        robot.value = (Speed - Drift, Speed)
        time.sleep(0.05)

        # If a wall is close, stop and find a new way
        if wall_distance() < TooClose:
            robot.stop()
            find_clear_path()

        # Every 10 seconds, log the ambient light
        if time.time() - LastLightTime >= LightInterval:
            try:
                Light = sensor.light
                lightlog.write(str(datetime.now()) + " | Light: " + str(Light) + "\n")
                lightlog.flush()
                print(f"Light: {Light}")
            except OSError:
                print("Sensor glitch, skipping read")
            LastLightTime = time.time()

except KeyboardInterrupt:
    lightlog.write(str(datetime.now()) + " | Stopped by user\n")
    lightlog.flush()

except Exception as error:
    lightlog.write(str(datetime.now()) + " | CRASH: " + str(error) + "\n")
    lightlog.flush()

lightlog.close()
robot.stop()
sensor.close()
print("Stopped!")
