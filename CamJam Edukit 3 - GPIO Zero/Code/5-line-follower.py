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
def SeekLine():
    print("Seeking the line")
    # The direction the robot will turn - True = Left
    Direction = True
    SeekSize = 0.2 # Turn time
    SeekCount = 1 # A count of times the robot has looked for the line
    MaxSeekCount = 5 # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or it has been searched for long enough
    while SeekCount <= MaxSeekCount:
        # Set the seek time
        SeekTime = SeekSize * SeekCount

        # Start the motors turning in a direction
        if Direction:
            print("Looking left")
            robot.left(0.4)
        else:
            print("Looking Right")
            robot.right(0.4)

        # Save the time it is now
        StartTime = time.time()

        # While the robot is turning for SeekTime seconds
        # check to see whether the line detector is over black
        while time.time() - StartTime <= SeekTime:
            if IsOverBlack():
                robot.stop()
                return True

        # The robot has not not found the black line yet, so stop
        robot.stop()

        time.sleep(0.1)

        # Increase the seek count
        SeekCount += 1

        # Change direction
        Direction = not Direction

    # The line wasn't found
    return False

try:
    print("Following the line")
    while True:
        if IsOverBlack():
            robot.forward(0.4)
        else:
            robot.stop()
            if SeekLine() == False:
                robot.stop()
                print("The robot has lost the line")
                exit()
            else:
                print("Following the line")

except KeyboardInterrupt:
    robot.stop()
    exit()
