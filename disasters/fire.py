"""
Models a spreading fire disaster.
"""

import logging
from core.event import Event
from environment.hazard_zone import HazardZone


class Fire(Event):
    """
    Fire disaster event with spread mechanics.
    """

    def __init__(self, origin, intensity: float):
        super().__init__("fire", {"intensity": intensity})
        self.origin = origin
        self.intensity = intensity

        self._logger = logging.getLogger(self.__class__.__name__)

    def generate_hazard(self) -> HazardZone:
        return HazardZone(self.origin, 5, self.intensity, "fire")
