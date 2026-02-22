# Tested using a robot built from the box the kit came in.
# Wheels mounted to the front of the robot. Sensor mounted between the wheels so turning arc of the sensor is small.
from gpiozero import CamJamKitRobot
from gpiozero import Button
import time

pinLineFollower = 25
sensor = Button(pinLineFollower)

robot = CamJamKitRobot()

# Seeking configuration constants (tuned for 2cm line)
SeekSize = 0.08       # Initial sweep duration
SeekIncrement = 0.03  # Added each attempt (smaller for narrow line)
SeekMax = 0.3         # Maximum sweep cap
TurnSpeed = 0.2       # Seeking turn speed (slower to not overshoot narrow line)
ForwardSpeed = 0.3    # Normal forward speed (slower to stay on line)

# Return True if the line detector is over a black line
def IsOverBlack():
    if sensor.is_pressed:
        return True
    else:
        return False

# Search for the black line - never gives up
def SeekLine():
    print("Seeking the line")
    # The direction the robot will turn - True = Left
    Direction = True
    SeekCount = 1 # A count of times the robot has looked for the line

    # Turn the robot left and right until it finds the line
    while True:
        # Set the seek time with additive growth and cap
        SeekTime = min(SeekSize + (SeekIncrement * (SeekCount - 1)), SeekMax)

        # Start the motors turning in a direction
        if Direction:
            print("Looking left")
            robot.left(TurnSpeed)
        else:
            print("Looking Right")
            robot.right(TurnSpeed)

        # Save the time it is now
        StartTime = time.time()

        # While the robot is turning for SeekTime seconds
        # check to see whether the line detector is over black
        while time.time() - StartTime <= SeekTime:
            if IsOverBlack():
                robot.stop()
                return

        # The robot has not found the black line yet, so stop
        robot.stop()

        time.sleep(0.1)

        # Increase the seek count
        SeekCount += 1

        # Change direction
        Direction = not Direction

try:
    print("Following the line")
    while True:
        if IsOverBlack():
            robot.forward(ForwardSpeed)
        else:
            robot.stop()
            SeekLine()
            print("Following the line")

except KeyboardInterrupt:
    robot.stop()
    exit()
