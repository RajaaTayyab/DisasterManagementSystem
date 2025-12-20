"""
Models dynamic hazard areas such as fire zones or collapse zones.
"""

import logging
import math
from typing import Tuple


class HazardZone:
    """
    Represents a circular hazard region with dynamic intensity.
    """

    def __init__(
        self,
        center: Tuple[int, int],
        radius: float,
        intensity: float,
        hazard_type: str,
    ):
        self.center = center
        self.radius = radius
        self.intensity = intensity
        self.type = hazard_type

        self._logger = logging.getLogger(self.__class__.__name__)

    def contains(self, point: Tuple[int, int]) -> bool:
        return math.dist(self.center, point) <= self.radius

    def expand(self, amount: float) -> None:
        self.radius += amount
        self._logger.debug("Hazard %s expanded to radius %s", self.type, self.radius)

    def decay(self, amount: float) -> None:
        self.intensity = max(0, self.intensity - amount)

    def update(self, timestep: float) -> None:
        """
        Hazard dynamics.
        """
        if self.intensity > 0:
            self.expand(0.05 * timestep)
            self.decay(0.02 * timestep)
