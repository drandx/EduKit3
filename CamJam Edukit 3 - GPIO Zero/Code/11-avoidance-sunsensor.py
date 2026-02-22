# Room Explorer Robot
# Drives around a room. When it sees a wall, it turns
# little by little until the way is clear, then keeps going.
# Runs forever until the battery runs out!
# Uses the SunSensor (VCNL4200 proximity sensor).

import time
import random
from gpiozero import CamJamKitRobot
from sunsensor import SunSensor

# Set up the robot and the proximity sensor
robot = CamJamKitRobot()
sensor = SunSensor()

# === Settings you can change ===
TooClose = 15.0    # How close to a wall before turning (centimeters)
Speed = 0.5        # How fast the robot drives (0.0 to 1.0)
TurnSpeed = 0.3    # How fast the robot turns (0.0 to 1.0)
TurnStep = 0.05    # How long each little turn lasts (seconds)


# Check how far the wall is (in centimeters)
def wall_distance():
    return sensor.distance


# Turn a little bit at a time until the way is clear
def find_clear_path():
    print("Wall ahead! Scanning...")

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


# === Main program - runs forever! ===
try:
    print("Room Explorer starting!")

    while True:
        # Drive forward
        robot.forward(Speed)
        time.sleep(0.05)

        # If a wall is close, stop and find a new way
        if wall_distance() < TooClose:
            robot.stop()
            find_clear_path()

except KeyboardInterrupt:
    robot.stop()
    sensor.close()
    print("Stopped!")
