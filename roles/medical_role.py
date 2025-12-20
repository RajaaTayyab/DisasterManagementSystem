"""

GAIA Role: Medical
---------------------------------
Encapsulates emergency medical treatment and triage logic.

GAIA Mapping:
- Responsibilities: Diagnose and treat patients
- Liveness: All admitted patients must be triaged
- Safety: Treatment must respect capacity constraints
"""

from core.role_base import Role
from typing import Dict, Any
import logging


class MedicalRole(Role):
    """
    MedicalRole defines GAIA-compliant medical behavior.
    """

    def __init__(self):
        super().__init__(name="Medical")
        self._logger = logging.getLogger(self.__class__.__name__)

        self.permissions.update(
            {
                "access_patient_data",
                "perform_triage",
                "administer_treatment",
            }
        )

    def responsibilities(self) -> str:
        return (
            "Provide medical assessment and treatment, prioritizing "
            "patients based on severity and available resources."
        )

    def liveness(self) -> str:
        return "All patients entering care will eventually be assessed."

    def safety(self) -> str:
        return (
            "The role must not exceed medical capacity or misclassify "
            "critical patients."
        )

    def triage(self, patient_data: Dict[str, Any]) -> str:
        """
        Role-level decision logic.

        Assigns a triage category based on patient condition.

        :param patient_data: Patient health information
        :return: Triage category
        """
        severity = patient_data.get("severity", 0)

        if severity >= 8:
            category = "critical"
        elif severity >= 4:
            category = "serious"
        else:
            category = "stable"

        self._logger.debug(
            "MedicalRole triage: severity=%s category=%s",
            severity,
            category,
        )
        return category
