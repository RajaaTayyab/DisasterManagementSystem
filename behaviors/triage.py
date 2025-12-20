"""
Implements medical triage logic.

Used by MedicalAgent and RescueAgent to prioritize casualties.
"""

import logging
from enum import Enum


class TriageCategory(Enum):
    IMMEDIATE = 3
    DELAYED = 2
    MINOR = 1
    EXPECTANT = 0


class TriageBehavior:
    """
    Encapsulates triage decision rules.

    GAIA Concept:
    - Supports prioritize(casualties) organizational rule
    """

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------

    def assess(self, injury_severity: float) -> TriageCategory:
        """
        Determine triage category.

        :param injury_severity: Severity in range [0,1]
        :return: TriageCategory
        """
        if injury_severity >= 0.8:
            category = TriageCategory.IMMEDIATE
        elif injury_severity >= 0.5:
            category = TriageCategory.DELAYED
        elif injury_severity >= 0.2:
            category = TriageCategory.MINOR
        else:
            category = TriageCategory.EXPECTANT

        self._logger.debug(
            "Injury severity %.2f -> %s",
            injury_severity,
            category.name,
        )

        return category

    # ------------------------------------------------------------------

    def priority_score(self, category: TriageCategory) -> int:
        """
        Convert category to numeric priority.

        :param category: TriageCategory
        :return: Priority score
        """
        return category.value
