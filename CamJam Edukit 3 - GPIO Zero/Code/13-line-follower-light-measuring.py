# CamJam EduKit 3 - Robotics
# Simple Line Follower with Light Measuring
#
# The robot follows a black line on the floor.
# While driving, it reads ambient light from the SunSensor (VCNL4200)
# and prints the average light level every 2 seconds.
# All light readings are saved to a log file (overwritten each run).

import os
import time
from gpiozero import CamJamKitRobot, LineSensor
from sunsensor import SunSensor

# The line sensor is on GPIO pin 25
linesensor = LineSensor(25)
robot = CamJamKitRobot()
sun = SunSensor()

# How fast the robot moves (0.0 = stopped, 1.0 = full speed)
speed = 0.6
# Gentle speed for searching turns when the line is lost
turn_speed = 0.3
# How long each search sweep lasts (seconds) — short so we don't overshoot
sweep_duration = 0.15

# Keep all light readings so we can calculate an average
light_readings = []

# Open a log file next to this script (overwritten each run)
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "light_readings.log")
logfile = open(log_path, "w")
logfile.write("timestamp,light,avg_light\n")

try:
    print("Line Follower with Light Measuring")
    print("Press CTRL+C to stop\n")
    robot.forward(speed)

    last_report = time.time()
    sweep_direction = 1  # 1 = right, -1 = left

    # Keep running until we press CTRL+C
    while True:
        # --- Line following (polled every loop) ---
        if linesensor.line_detected:
            print("Line detected! Moving forward.")
            robot.forward(speed)
        else:
            print("Line lost! Sweeping search.")
            # Short gentle turn, then alternate direction for next time
            if sweep_direction == 1:
                robot.right(turn_speed)
            else:
                robot.left(turn_speed)
            time.sleep(sweep_duration)
            robot.stop()
            sweep_direction *= -1

        # --- Light measuring ---
        reading = sun.light
        light_readings.append(reading)
        avg = sum(light_readings) / len(light_readings)
        logfile.write(f"{time.time():.3f},{reading},{avg:.1f}\n")
        logfile.flush()

        # Every 2 seconds, print the average light so far
        now = time.time()
        if now - last_report >= 2.0:
            print(f"Light now: {reading}  |  Average: {avg:.0f}  |  Samples: {len(light_readings)}")
            last_report = now

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    robot.stop()
    sun.close()
    logfile.close()
    if light_readings:
        avg = sum(light_readings) / len(light_readings)
        print(f"\nFinal average light: {avg:.0f} (from {len(light_readings)} readings)")
    print(f"Log saved to: {log_path}")
