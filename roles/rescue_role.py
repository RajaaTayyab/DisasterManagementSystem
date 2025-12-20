"""

GAIA Role: Rescue
---------------------------------
Defines responsibilities for search-and-rescue operations.

GAIA Mapping:
- Responsibilities: Locate and extract affected entities
- Liveness: All assigned rescue tasks must be attempted
- Safety: Rescuers must not enter unauthorized hazardous zones
"""

from core.role_base import Role
from typing import Dict, Any
import logging


class RescueRole(Role):
    """
    RescueRole encapsulates GAIA rescue behavior.
    """

    def __init__(self):
        super().__init__(name="Rescue")
        self._logger = logging.getLogger(self.__class__.__name__()

        )

        self.permissions.update(
            {
                "access_hazard_maps",
                "extract_entities",
                "transport_entities",
            }
        )

    def responsibilities(self) -> str:
        return (
            "Perform search and rescue operations to locate and extract "
            "affected entities from hazardous environments."
        )

    def liveness(self) -> str:
        return "Every assigned rescue task will eventually be attempted."

    def safety(self) -> str:
        return (
            "The role must not enter zones marked as critically unsafe "
            "without explicit authorization."
        )

    def prioritize_rescue(self, target: Dict[str, Any]) -> int:
        """
        Role-level decision logic.

        Computes a priority score for rescue targets.

        :param target: Information about the affected entity
        :return: Priority score (higher = more urgent)
        """
        injury = target.get("injury_level", 0)
        trapped = target.get("trapped", False)

        priority = injury * 2 + (5 if trapped else 0)

        self._logger.debug(
            "RescueRole priority calculation: injury=%s trapped=%s score=%s",
            injury,
            trapped,
            priority,
        )
        return priority
