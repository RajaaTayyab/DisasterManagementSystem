"""
Models an earthquake event with intensity-based damage propagation.
"""

import logging
from core.event import Event
from environment.hazard_zone import HazardZone


class Earthquake(Event):
    """
    Earthquake disaster event.
    """

    def __init__(self, epicenter, magnitude: float):
        super().__init__("earthquake", {"magnitude": magnitude})
        self.epicenter = epicenter
        self.magnitude = magnitude

        self._logger = logging.getLogger(self.__class__.__name__)

    def generate_hazard(self) -> HazardZone:
        radius = self.magnitude * 10
        intensity = self.magnitude * 5
        return HazardZone(self.epicenter, radius, intensity, "seismic")
