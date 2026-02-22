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
# since the line likely curved the other way.
# After a full sweep round (left + right) with no result, reposition
# by driving right, then left, alternating between rounds.
def SeekLine():
    global LastFoundDirection
    print("Line lost - stopping")
    robot.stop()
    time.sleep(0.5)

    SweepTime = 0.2       # seconds per sweep turn
    TurnSpeed = 0.3       # speed while sweeping
    MoveSpeed = 0.3       # speed while repositioning
    SweepsPerRound = 2    # left + right = one round
    MoveDirection = False # first reposition goes right (False=right, True=left)

    # Start sweeping opposite to where we last found the line
    Direction = not LastFoundDirection
    SweepCount = 0        # how many sweeps done in this round
    SearchTime = 0.0      # total time spent sweeping in this round

    while True:
        # --- Sweep ---
        if Direction:
            print("Sweeping left")
            robot.left(TurnSpeed)
        else:
            print("Sweeping right")
            robot.right(TurnSpeed)

        StartTime = time.time()
        while time.time() - StartTime < SweepTime:
            if IsOverBlack():
                robot.stop()
                LastFoundDirection = Direction
                return

        robot.stop()
        SearchTime += SweepTime
        SweepCount += 1
        Direction = not Direction

        # --- After a full round, reposition and try again ---
        if SweepCount >= SweepsPerRound:
            if MoveDirection:
                print(f"Repositioning left for {SearchTime:.1f}s")
                robot.left(MoveSpeed)
            else:
                print(f"Repositioning right for {SearchTime:.1f}s")
                robot.right(MoveSpeed)

            # Drive for the tracked time, checking sensor while moving
            StartTime = time.time()
            while time.time() - StartTime < SearchTime:
                if IsOverBlack():
                    robot.stop()
                    LastFoundDirection = MoveDirection
                    return

            robot.stop()
            time.sleep(0.3)

            # Reset for next round, flip reposition direction
            MoveDirection = not MoveDirection
            SweepCount = 0
            SearchTime = 0.0

try:
    print("Following the line")
    while True:
        if IsOverBlack():
            robot.forward(0.3)
        else:
            SeekLine()
            print("Following the line")

except KeyboardInterrupt:
    robot.stop()
    exit()
