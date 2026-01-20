# SunSensor - A light sensor for robots!
# Works just like LineSensor but measures sunlight

import smbus2 as smbus
import time
from threading import Thread


class SunSensor:
    """
    A sensor that measures how bright the sunlight is.

    Example:
        sun = SunSensor()
        print(sun.light)  # Shows brightness number

        if sun.is_sunny:
            print("Nice and bright!")
    """

    def __init__(self, address=0x51):
        """Create a new sun sensor."""
        self._i2c = smbus.SMBus(1)
        self._address = address
        self._sunny_threshold = 1000  # Above this = sunny!

        # Callbacks (like LineSensor has when_line)
        self._when_sunny = None
        self._when_dark = None
        self._last_state = None

        # Turn on the sensor
        self._i2c.write_word_data(self._address, 0x00, 0x0000)
        time.sleep(0.1)

        # Start watching for changes
        self._running = True
        self._watcher = Thread(target=self._watch_light, daemon=True)
        self._watcher.start()

    @property
    def light(self):
        """How bright is it? Returns a number."""
        return self._i2c.read_word_data(self._address, 0x09)

    @property
    def is_sunny(self):
        """Is it bright enough? Returns True or False."""
        return self.light > self._sunny_threshold

    @property
    def is_dark(self):
        """Is it too dark? Returns True or False."""
        return self.light <= self._sunny_threshold

    @property
    def sunny_threshold(self):
        """The brightness level we call 'sunny'."""
        return self._sunny_threshold

    @sunny_threshold.setter
    def sunny_threshold(self, value):
        """Change what we call 'sunny'."""
        self._sunny_threshold = value

    @property
    def when_sunny(self):
        """Function to call when it gets sunny."""
        return self._when_sunny

    @when_sunny.setter
    def when_sunny(self, callback):
        """Set what happens when it gets sunny."""
        self._when_sunny = callback

    @property
    def when_dark(self):
        """Function to call when it gets dark."""
        return self._when_dark

    @when_dark.setter
    def when_dark(self, callback):
        """Set what happens when it gets dark."""
        self._when_dark = callback

    def _watch_light(self):
        """Keep checking if sunny/dark changed."""
        while self._running:
            current = self.is_sunny

            if self._last_state is not None:
                # Did it just get sunny?
                if current and not self._last_state:
                    if self._when_sunny:
                        self._when_sunny()
                # Did it just get dark?
                elif not current and self._last_state:
                    if self._when_dark:
                        self._when_dark()

            self._last_state = current
            time.sleep(0.1)

    def close(self):
        """Turn off the sensor."""
        self._running = False
