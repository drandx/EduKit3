from gpiozero import CamJamKitRobot, LineSensor, DistanceSensor
from sunsensor import SunSensor
import time

# 1. Setup our Robot and Sensors
robot = CamJamKitRobot()
line_sensor = LineSensor(25)     # From Worksheet 5 [cite: 195, 228]
distance_sensor = DistanceSensor(echo=18, trigger=17) # From Worksheet 6 [cite: 107, 108]
sun = SunSensor()

# 2. This is the "Brain" function for making a decision
def choose_the_sun():
    print("I found a split! Checking the sun...")
    robot.stop()
    
    # Peek Left
    robot.left(0.3)
    time.sleep(0.5)
    left_brightness = sun.light
    
    # Peek Right (Turn past middle to the right)
    robot.right(0.3)
    time.sleep(1.0) 
    right_brightness = sun.light
    
    if left_brightness > right_brightness:
        print("Left looks sunnier! Going left.")
        robot.left(0.3) # Turn back to the left path
        time.sleep(0.5)
    else:
        print("Right looks sunnier! Going right.")
        # We are already facing right, so we just continue!

# 3. The Main Loop (Runs until the battery dies!)
print("Robot starting! I am looking for the sunniest path.")

try:
    while True:
        # Check for obstacles first so we don't crash! [cite: 119]
        if distance_sensor.distance < 0.1: # If something is 10cm away [cite: 119]
            robot.stop()
            print("Obstacle! Waiting for it to move.")
        
        # Follow the line! [cite: 241]
        elif line_sensor.line_detected:
            robot.forward(0.3)
            
        # If we lose the line, it might be a split!
        else:
            choose_the_sun()
            
except KeyboardInterrupt:
    print("Robot stopped by user.")
    robot.stop()