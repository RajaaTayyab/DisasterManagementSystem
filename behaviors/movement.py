"""
Defines movement-related behaviors shared by multiple agents.

This module abstracts spatial reasoning, path following, speed
variation, and obstruction handling. It does NOT own the map.
"""

import logging
import math
from typing import Tuple


class MovementBehavior:
    """
    Encapsulates generic movement logic.

    GAIA Concept:
    - Supports liveness properties such as reach(destination)
    - Reusable across civilian, rescue, and evacuation agents
    """

    def __init__(self, max_speed: float = 1.0):
        self.max_speed = max_speed
        self.current_speed = max_speed
        self._logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------

    def move_towards(
        self,
        current: Tuple[float, float],
        target: Tuple[float, float],
        timestep: float,
    ) -> Tuple[float, float]:
        """
        Compute next position toward a target.

        :param current: Current (x, y)
        :param target: Target (x, y)
        :param timestep: Simulation timestep
        :return: New position
        """
        dx = target[0] - current[0]
        dy = target[1] - current[1]
        distance = math.hypot(dx, dy)

        if distance == 0:
            return current

        step = min(self.current_speed * timestep, distance)
        nx = current[0] + (dx / distance) * step
        ny = current[1] + (dy / distance) * step

        self._logger.debug(
            "Moving from %s to %s (step=%.2f)", current, (nx, ny), step
        )

        return nx, ny

    # ------------------------------------------------------------------

    def slow_down(self, factor: float) -> None:
        """
        Reduce movement speed (e.g., debris, panic).

        :param factor: Multiplier in range (0,1]
        """
        self.current_speed = max(0.1, self.max_speed * factor)

    def reset_speed(self) -> None:
        """Restore original speed."""
        self.current_speed = self.max_speed
