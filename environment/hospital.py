"""

Models hospitals with capacity, triage, and patient handling.
"""

import uuid
import logging


class Hospital:
    """
    Represents a medical facility.
    """

    def __init__(self, location, capacity: int):
        self.id = str(uuid.uuid4())
        self.location = location
        self.capacity = capacity
        self.current_patients = 0

        self._logger = logging.getLogger(self.__class__.__name__)

    def admit(self) -> bool:
        if self.current_patients < self.capacity:
            self.current_patients += 1
            return True
        return False

    def discharge(self) -> None:
        if self.current_patients > 0:
            self.current_patients -= 1
