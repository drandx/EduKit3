# CamJam EduKit 3 - Robotics
# Obstacle Avoidance using SunSensor (VCNL4200 proximity)

import time
from gpiozero import CamJamKitRobot
from sunsensor import SunSensor

robot = CamJamKitRobot()
sensor = SunSensor()

# Distance threshold in cm — objects closer than this trigger avoidance
hownear = 15.0
reversetime = 0.5
turntime = 0.75

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.5
rightmotorspeed = 0.5

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorleft = (leftmotorspeed, 0)
motorright = (0, rightmotorspeed)


def isnearobstacle(localhownear):
    distance = sensor.distance

    print("IsNearObstacle: " + str(distance))
    if distance < localhownear:
        print("Too close!")
        return True
    else:
        return False


def avoidobstacle():
    # Back off a little
    print("Backwards")
    robot.value = motorbackward
    time.sleep(reversetime)
    robot.stop()

    # Turn right
    print("Right")
    robot.value = motorright
    time.sleep(turntime)
    robot.stop()


try:
    while True:
        robot.value = motorforward
        time.sleep(0.1)
        if isnearobstacle(hownear):
            robot.stop()
            avoidobstacle()

except KeyboardInterrupt:
    robot.stop()
    sensor.close()
