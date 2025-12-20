"""
Models buildings within the city, including structural integrity,
occupancy, and damage accumulation.
"""

import uuid
import logging
import math
from typing import Tuple


class Building:
    """
    Represents a physical structure subject to disaster damage.
    """

    def __init__(self, location: Tuple[int, int], floors: int):
        self.id = str(uuid.uuid4())
        self.location = location
        self.floors = floors

        self.integrity = 100.0
        self.occupancy = 0
        self.collapsed = False

        self._logger = logging.getLogger(self.__class__.__name__)

    def apply_damage(self, amount: float) -> None:
        """
        Apply structural damage to the building.
        """
        if self.collapsed:
            return

        self.integrity -= amount
        self._logger.debug(
            "Building %s damaged by %s (integrity=%s)",
            self.id,
            amount,
            self.integrity,
        )

        if self.integrity <= 0:
            self.collapsed = True
            self.integrity = 0
            self._logger.warning("Building %s collapsed", self.id)

    def distance_to(self, point: Tuple[int, int]) -> float:
        return math.dist(self.location, point)

    def update(self, timestep: float) -> None:
        """
        Gradual degradation logic.
        """
        if not self.collapsed and self.integrity < 30:
            self.apply_damage(0.1 * timestep)
