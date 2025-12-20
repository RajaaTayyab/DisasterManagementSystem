"""
GAIA Role: Affected
Represents entities impacted by disasters (e.g., civilians).
This role defines reactive behavior rather than proactive control.

GAIA Mapping is being perfomed here :
- Responsibilities: Seek safety and assistance
- Liveness: Affected entities must attempt survival actions
- Safety: Must avoid knowingly unsafe actions
"""

from core.role_base import Role
from typing import Dict, Any
import logging


class AffectedRole(Role):
    
    #AffectedRole models behavior of disaster-impacted entities.
    

    def __init__(self):
        super().__init__(name="Affected")
        self._logger = logging.getLogger(self.__class__.__name__)

        self.permissions.update(
            {
                "request_help",
                "receive_instructions",
                "move_within_environment",
            }
        )

    def responsibilities(self) -> str:
        return (
            "React to hazardous conditions by seeking safety, "
            "requesting assistance, and complying with evacuation directives."
        )

    def liveness(self) -> str:
        return (
            "If the entity is in danger, it will eventually attempt to "
            "escape, request help, or follow guidance."
        )

    def safety(self) -> str:
        return (
            "The role must not intentionally move toward known hazards "
            "or ignore direct evacuation orders."
        )

    def assess_threat(self, perceived_state: Dict[str, Any]) -> str:
        """
        Role-level decision logic.

        Determines high-level response strategy based on perceived risk.

        :param perceived_state: Information about hazards and health
        :return: Chosen response strategy
        """
        danger_level = perceived_state.get("danger_level", 0)
        injured = perceived_state.get("injured", False)

        if injured:
            decision = "request_medical_help"
        elif danger_level > 7:
            decision = "evacuate_immediately"
        elif danger_level > 3:
            decision = "seek_shelter"
        else:
            decision = "monitor"

        self._logger.debug(
            "AffectedRole decision: danger=%s injured=%s action=%s",
            danger_level,
            injured,
            decision,
        )
        return decision
