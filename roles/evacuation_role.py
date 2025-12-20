"""
GAIA Role: Evacuation
---------------------------------
Responsible for coordinated movement of entities to safety.

GAIA Mapping:
- Responsibilities: Plan and execute evacuations
- Liveness: Evacuation orders must be carried out
- Safety: Routes must avoid known hazards
"""

from core.role_base import Role
from typing import Dict, Any
import logging


class EvacuationRole(Role):
    """
    EvacuationRole models GAIA evacuation responsibilities.
    """

    def __init__(self):
        super().__init__(name="Evacuation")
        self._logger = logging.getLogger(self.__class__.__name__)

        self.permissions.update(
            {
                "access_route_maps",
                "control_transport",
                "issue_movement_orders",
            }
        )

    def responsibilities(self) -> str:
        return (
            "Coordinate the safe relocation of entities away from "
            "hazard zones using approved routes."
        )

    def liveness(self) -> str:
        return "All issued evacuation orders will eventually be executed."

    def safety(self) -> str:
        return "Evacuation routes must not pass through active hazard zones."

    def evaluate_route(self, route_data: Dict[str, Any]) -> bool:
        """
        Role-level decision logic.

        Determines whether a route is safe for evacuation.

        :param route_data: Route characteristics
        :return: True if route is acceptable
        """
        hazard_level = route_data.get("hazard_level", 0)
        congestion = route_data.get("congestion", 0)

        decision = hazard_level == 0 and congestion < 7

        self._logger.debug(
            "EvacuationRole route evaluation: hazard=%s congestion=%s valid=%s",
            hazard_level,
            congestion,
            decision,
        )
        return decision
