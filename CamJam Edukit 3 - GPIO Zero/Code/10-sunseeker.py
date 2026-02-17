from sunsensor import SunSensor
import time

sun = SunSensor()

try:
    while True:
        print(f"Light: {sun.light}  |  Distance: {sun.distance:.1f} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    sun.close()
