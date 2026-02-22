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
TooClose = 80    # How close to a wall before turning (centimeters)
Speed = 0.5        # How fast the robot drives (0.0 to 1.0)
TurnSpeed = 0.5    # How fast the robot turns (0.0 to 1.0)
TurnStep = 0.5    # How long each little turn lasts (seconds)


# Check how far the wall is (in centimeters)
def wall_distance():
    return sensor.distance


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
LogFile = "explorer_log.txt"
LogInterval = 5  # Write to log every 5 seconds

# Track light readings for the average
LightTotal = 0
LightCount = 0


# === Main program - runs forever! ===
try:
    StartTime = datetime.now()

    # Start a fresh log file (overwrites the old one)
    log = open(LogFile, "w")
    log.write("Room Explorer Log\n")
    log.write("Started: " + str(StartTime) + "\n\n")
    log.flush()

    print("Room Explorer starting!")
    print("Logging to " + LogFile)

    LastLogTime = time.time()

    while True:
        # Drive forward
        robot.forward(Speed)
        time.sleep(0.05)

        # If a wall is close, stop and find a new way
        if wall_distance() < TooClose:
            robot.stop()
            find_clear_path()

        # Read the ambient light and add it to our total
        LightTotal += sensor.light
        LightCount += 1

        print(f"Light: {sensor.light}  |  Distance: {sensor.distance:.1f} cm")

        # Every few seconds, save the average light to the log file
        if time.time() - LastLogTime >= LogInterval:
            AvgLight = LightTotal / LightCount
            log.write(str(datetime.now()) + " | Avg light: " + str(round(AvgLight, 1)) + "\n")
            log.flush()
            LastLogTime = time.time()

except KeyboardInterrupt:
    pass

# Write the final summary (works for Ctrl+C, may not survive battery death)
EndTime = datetime.now()
Duration = EndTime - StartTime
if LightCount > 0:
    AvgLight = LightTotal / LightCount
    log.write("\nFinished: " + str(EndTime) + "\n")
    log.write("Duration: " + str(Duration) + "\n")
    log.write("Final avg light: " + str(round(AvgLight, 1)) + "\n")
    log.flush()
log.close()

robot.stop()
sensor.close()
print("Stopped! Log saved to " + LogFile)
