# Sun Seeker Robot
# The robot spins around, measures the light in each direction,
# then turns to face the brightest direction.
# The right motor is inverted, so we flip its speed.

import time
from gpiozero import CamJamKitRobot
from sunsensor import SunSensor

robot = CamJamKitRobot()
sensor = SunSensor()

# === Settings you can change ===
TurnSpeed = 0.3      # How fast to spin while scanning
TurnStep = 0.3       # How long each step lasts (seconds)
Steps = 20           # How many steps in a full scan

# Turn left one step (right motor is inverted, so we flip it)
def turn_left():
    robot.value = (-TurnSpeed, TurnSpeed)
    time.sleep(TurnStep)
    robot.stop()
    time.sleep(0.2)

# Turn right one step (right motor is inverted, so we flip it)
def turn_right():
    robot.value = (TurnSpeed, -TurnSpeed)
    time.sleep(TurnStep)
    robot.stop()
    time.sleep(0.2)

try:
    print("Sun Seeker starting! (Ctrl+C to stop)")

    while True:
        # Step 1: Spin left and measure light at each step
        print("Scanning...")
        BrightestLight = 0
        BrightestStep = 0

        for Step in range(Steps):
            Light = sensor.light
            print(f"  Step {Step}: Light = {Light}")

            if Light > BrightestLight:
                BrightestLight = Light
                BrightestStep = Step

            turn_left()

        print(f"Brightest at step {BrightestStep} with light {BrightestLight}")

        # Step 2: Turn right to go back to the brightest position
        StepsBack = Steps - BrightestStep
        print(f"Turning back {StepsBack} steps...")

        for Step in range(StepsBack):
            turn_right()

        print("Facing the light! Staying for 5 seconds...")

        # Step 3: Stay on the bright spot by wiggling back and forth
        WiggleDuration = 5.0   # Total time to stay (seconds)
        WiggleStep = 0.25      # Each half-wiggle lasts this long
        WiggleSpeed = 0.2      # Gentle speed for wiggling

        elapsed = 0.0
        forward = True
        while elapsed < WiggleDuration:
            if forward:
                robot.value = (WiggleSpeed, WiggleSpeed)
            else:
                robot.value = (-WiggleSpeed, -WiggleSpeed)
            time.sleep(WiggleStep)
            elapsed += WiggleStep
            forward = not forward

        robot.stop()
        print("Done staying. Scanning again...\n")

except KeyboardInterrupt:
    pass

robot.stop()
sensor.close()
print("Done!")
