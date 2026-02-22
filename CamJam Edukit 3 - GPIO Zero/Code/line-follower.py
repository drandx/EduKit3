# Tested using a robot built from the box the kit came in.
# Wheels mounted to the front of the robot. Sensor mounted between the wheels so turning arc of the sensor is small.
from gpiozero import CamJamKitRobot
from gpiozero import Button
import time

pinLineFollower = 25
sensor = Button(pinLineFollower)

robot = CamJamKitRobot()

# Return True if the line detector is over a black line
def IsOverBlack():
    if sensor.is_pressed:
        return True
    else:
        return False

# Search for the black line
# Stop, wait, then sweep left/right at minimum speed until found
def SeekLine():
    print("Line lost - stopping")
    robot.stop()
    time.sleep(0.5)

    SweepTime = 1.5   # seconds per sweep
    Direction = True   # True = left first

    while True:
        if Direction:
            print("Sweeping left")
            robot.left(0.1)
        else:
            print("Sweeping right")
            robot.right(0.1)

        # Turn for SweepTime, checking the sensor continuously
        StartTime = time.time()
        while time.time() - StartTime < SweepTime:
            if IsOverBlack():
                robot.stop()
                return

        robot.stop()

        # Flip direction for next sweep
        Direction = not Direction

try:
    print("Following the line")
    while True:
        if IsOverBlack():
            robot.forward(0.4)
        else:
            SeekLine()
            print("Following the line")

except KeyboardInterrupt:
    robot.stop()
    exit()
