import smbus2 as smbus
import math
import time
from threading import Thread

class SunSensor:
    def __init__(self, address=0x51):
        self._i2c = smbus.SMBus(1)
        self._address = address

        # User-adjustable thresholds
        self.sunny_threshold = 1000
        self.near_threshold = 2000

        # Proximity-to-distance calibration.
        # Tune these two values with a known object at a known distance:
        #   1. Place an object at a measured distance (e.g. 10 cm)
        #   2. Read the raw proximity value at that distance
        #   3. Set calibration_distance to the measured distance (in cm)
        #   4. Set calibration_raw to the raw value you read
        self.calibration_distance = 10.0   # cm
        self.calibration_raw = 4000        # raw count at that distance
        self.max_distance = 150.0          # cm — sensor max range

        # Event Callbacks
        self.when_sunny = None
        self.when_dark = None
        self.when_near = None
        self.when_far = None

        self._last_sunny = None
        self._last_near = None

        # INITIALIZATION
        # 0x00: ALS_CONF (0x0000 = power on ALS)
        self._i2c.write_word_data(self._address, 0x00, 0x0000)
        # 0x03: PS_CONF1_2 (0x0000 = power on Proximity)
        self._i2c.write_word_data(self._address, 0x03, 0x0000)
        time.sleep(0.1)

        self._running = True
        self._watcher = Thread(target=self._watch_sensor, daemon=True)
        self._watcher.start()

    @property
    def light(self):
        """Returns raw ambient light value from register 0x0B."""
        return self._i2c.read_word_data(self._address, 0x0B)

    @property
    def distance_raw(self):
        """Returns raw proximity value from register 0x08."""
        return self._i2c.read_word_data(self._address, 0x08)

    @property
    def distance(self):
        """Estimated distance in cm using inverse-square calibration.

        The VCNL4200 proximity count follows roughly:
            raw ∝ 1 / d²
        So:
            d ≈ calibration_distance * sqrt(calibration_raw / raw)

        Returns max_distance when nothing is detected (raw ≈ 0).
        """
        raw = self.distance_raw
        if raw <= 0:
            return self.max_distance
        k = self.calibration_distance * self.calibration_distance * self.calibration_raw
        d = math.sqrt(k / raw)
        return min(d, self.max_distance)

    @property
    def is_sunny(self):
        return self.light > self.sunny_threshold

    @property
    def is_dark(self):
        return self.light <= self.sunny_threshold

    @property
    def is_near(self):
        return self.distance_raw > self.near_threshold

    @property
    def is_far(self):
        return self.distance_raw <= self.near_threshold

    def _watch_sensor(self):
        while self._running:
            # Check Light Changes
            current_sunny = self.is_sunny
            if self._last_sunny is not None:
                if current_sunny and not self._last_sunny:
                    if self.when_sunny: self.when_sunny()
                elif not current_sunny and self._last_sunny:
                    if self.when_dark: self.when_dark()
            self._last_sunny = current_sunny

            # Check Proximity Changes
            current_near = self.is_near
            if self._last_near is not None:
                if current_near and not self._last_near:
                    if self.when_near: self.when_near()
                elif not current_near and self._last_near:
                    if self.when_far: self.when_far()
            self._last_near = current_near

            time.sleep(0.1)

    def close(self):
        self._running = False

# Example of how to use it in your robot script:
if __name__ == "__main__":
    sensor = SunSensor()

    # Optional: calibrate by placing an object at a known distance
    # sensor.calibration_distance = 10.0  # cm
    # sensor.calibration_raw = 4000       # raw count you read at that distance

    sensor.when_sunny = lambda: print("It's bright!")
    sensor.when_dark = lambda: print("It's dark!")
    sensor.when_near = lambda: print("Obstacle detected!")
    sensor.when_far = lambda: print("Path clear!")

    try:
        while True:
            print(f"Light: {sensor.light}  |  Distance: {sensor.distance:.1f} cm (raw: {sensor.distance_raw})")
            time.sleep(1)
    except KeyboardInterrupt:
        sensor.close()
