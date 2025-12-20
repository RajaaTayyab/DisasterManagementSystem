"""
behaviors/routing.py

Provides route selection and rerouting logic.

This module is deliberately map-agnostic and operates on
abstract graph-like interfaces.
"""

import logging
from typing import List, Any


class RoutingBehavior:
    """
    Abstract routing behavior.

    GAIA Concept:
    - Supports safety(goal) and reach(goal) liveness
    """

    def __init__(self):
        self.current_route: List[Any] = []
        self._logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------

    def set_route(self, route: List[Any]) -> None:
        """
        Assign a route to follow.

        :param route: Sequence of waypoints or nodes
        """
        self.current_route = list(route)
        self._logger.debug("Route set: %s", self.current_route)

    def next_waypoint(self):
        """
        Get next waypoint on route.

        :return: Waypoint or None
        """
        if not self.current_route:
            return None
        return self.current_route[0]

    def advance(self) -> None:
        """
        Move to next waypoint.
        """
        if self.current_route:
            wp = self.current_route.pop(0)
            self._logger.debug("Reached waypoint %s", wp)

    # ------------------------------------------------------------------

    def requires_reroute(self, hazard_level: float) -> bool:
        """
        Determine if rerouting is needed.

        :param hazard_level: Environmental risk
        :return: Boolean
        """
        decision = hazard_level > 0.5
        if decision:
            self._logger.info("Reroute required due to hazard")
        return decision
