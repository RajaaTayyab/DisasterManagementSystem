"""

GAIA Role: Observer
---------------------------------
This role represents environmental observation responsibilities.
It is intentionally agent-agnostic and can be enacted by any agent
capable of sensing or monitoring the environment.

GAIA Mapping:
- Responsibilities: Detect, classify, and report events
- Liveness: Hazards must eventually be observed and reported
- Safety: False or duplicate alerts must not be generated
"""

from core.role_base import Role
from typing import Dict, Any
import logging


class ObserverRole(Role):
    """
    ObserverRole encapsulates the GAIA Observer role.

    This role does NOT perform sensing itself. Instead, it defines
    how sensed information should be interpreted and escalated.
    """

    def __init__(self):
        super().__init__(name="Observer")
        self._logger = logging.getLogger(self.__class__.__name__)

        # GAIA Permissions: what the role is allowed to access or do
        self.permissions.update(
            {
                "read_environment_state",
                "generate_alerts",
                "notify_command_center",
            }
        )

    def responsibilities(self) -> str:
        """
        GAIA Responsibility Definition.
        """
        return (
            "Monitor the environment for significant changes or hazards "
            "and report validated observations to coordinating entities."
        )

    def liveness(self) -> str:
        """
        GAIA Liveness Property.
        """
        return (
            "If an environmental hazard exists, it will eventually be "
            "detected and reported."
        )

    def safety(self) -> str:
        """
        GAIA Safety Property.
        """
        return (
            "The role must not generate alerts without verified observations "
            "or flood the system with redundant notifications."
        )

    def evaluate_observation(self, observation: Dict[str, Any]) -> bool:
        """
        Role-level decision logic.

        Determines whether a raw observation is significant enough
        to escalate into an alert.

        :param observation: Structured observation data
        :return: True if escalation is required
        """
        severity = observation.get("severity", 0)
        validated = observation.get("validated", False)

        decision = validated and severity > 0
        self._logger.debug(
            "ObserverRole decision: severity=%s validated=%s escalate=%s",
            severity,
            validated,
            decision,
        )
        return decision
