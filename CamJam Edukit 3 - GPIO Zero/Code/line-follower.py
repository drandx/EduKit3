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

# Track the last direction the robot swept to find the line
# True = left, False = right
LastFoundDirection = True

# Search for the black line
# Start seeking in the opposite direction to where we last found it,
# since the line likely curved the other way
def SeekLine():
    global LastFoundDirection
    print("Line lost - stopping")
    robot.stop()
    time.sleep(0.5)

    SweepTime = 0.5   # seconds per sweep
    TurnSpeed = 0.3   # Speed to turn at while seeking
    # Start in the opposite direction to where we last found the line
    Direction = not LastFoundDirection

    while True:
        if Direction:
            print("Sweeping left")
            robot.left(TurnSpeed)
        else:
            print("Sweeping right")
            robot.right(TurnSpeed)

        # Turn for SweepTime, checking the sensor continuously
        StartTime = time.time()
        while time.time() - StartTime < SweepTime:
            if IsOverBlack():
                robot.stop()
                # Remember which direction found the line this time
                LastFoundDirection = Direction
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
