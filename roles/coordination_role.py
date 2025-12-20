"""
GAIA Role: Coordination
---------------------------------
Defines centralized decision-making and task allocation.

GAIA Mapping:
- Responsibilities: Global awareness and coordination
- Liveness: All critical events must be addressed
- Safety: Conflicting commands must not be issued
"""

from core.role_base import Role
from typing import Dict, Any, List
import logging


class CoordinationRole(Role):
    """
    CoordinationRole encapsulates GAIA command and control behavior.
    """

    def __init__(self):
        super().__init__(name="Coordination")
        self._logger = logging.getLogger(self.__class__.__name__)

        self.permissions.update(
            {
                "assign_tasks",
                "prioritize_events",
                "access_global_state",
            }
        )

    def responsibilities(self) -> str:
        return (
            "Maintain global situational awareness and coordinate agents "
            "by assigning tasks and resolving conflicts."
        )

    def liveness(self) -> str:
        return "Every critical event will eventually receive a response."

    def safety(self) -> str:
        return "The role must not issue contradictory or redundant commands."

    def prioritize_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Role-level decision logic.

        Orders events by severity and urgency.

        :param events: List of event descriptors
        :return: Prioritized list
        """
        prioritized = sorted(
            events,
            key=lambda e: (e.get("severity", 0), e.get("timestamp", 0)),
            reverse=True,
        )

        self._logger.debug(
            "CoordinationRole prioritized %s events", len(prioritized)
        )
        return prioritized
