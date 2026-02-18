from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Initialize the pigpio pin factory
factory = PiGPIOFactory()

# Assign the factory to your sensor
# (Using EduKit 3 default pins: Echo=18, Trigger=17)
sensor = DistanceSensor(echo=18, trigger=17, pin_factory=factory, max_distance=4)

while True:
    print('Distance: ', sensor.distance * 100, 'cm')
    sleep(1)
