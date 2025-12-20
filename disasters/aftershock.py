"""
Models secondary seismic events following an earthquake.
"""

import logging
from core.event import Event


class Aftershock(Event):
    """
    Represents an aftershock event.
    """

    def __init__(self, epicenter, magnitude: float):
        super().__init__("aftershock", {"magnitude": magnitude})
        self.epicenter = epicenter
        self.magnitude = magnitude

        self._logger = logging.getLogger(self.__class__.__name__)

    def severity(self) -> float:
        return self.magnitude * 3
