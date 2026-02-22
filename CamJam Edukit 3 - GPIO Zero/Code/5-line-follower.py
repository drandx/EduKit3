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
TurnSpeed = 0.3      # Seeking turn speed (min 0.2 for motor movement)
ForwardSpeed = 0.3   # Normal forward speed
ForwardTime = 0.1    # Forward pulse duration (shorter = slower overall)

# Return True if the line detector is over a black line
def IsOverBlack():
    if sensor.is_pressed:
        return True
    else:
        return False

# Search for the black line - optimized for left-turn track
def SeekLine():
    print("Seeking the line")

    # First, do a longer left sweep since turns are always left
    print("Looking left (priority)")
    robot.left(TurnSpeed)
    StartTime = time.time()
    while time.time() - StartTime <= SeekMax:
        if IsOverBlack():
            robot.stop()
            return
    robot.stop()
    time.sleep(0.1)

    # If not found, fall back to alternating sweeps
    Direction = False  # Start right to return to center
    SeekCount = 1

    while True:
        SeekTime = min(SeekSize + (SeekIncrement * (SeekCount - 1)), SeekMax)

        if Direction:
            print("Looking left")
            robot.left(TurnSpeed)
        else:
            print("Looking right")
            robot.right(TurnSpeed)

        StartTime = time.time()
        while time.time() - StartTime <= SeekTime:
            if IsOverBlack():
                robot.stop()
                return

        robot.stop()
        time.sleep(0.1)
        SeekCount += 1
        Direction = not Direction

try:
    print("Following the line")
    while True:
        if IsOverBlack():
            robot.forward(ForwardSpeed)
            time.sleep(ForwardTime)
            robot.stop()
        else:
            SeekLine()
            print("Following the line")

except KeyboardInterrupt:
    robot.stop()
    exit()
