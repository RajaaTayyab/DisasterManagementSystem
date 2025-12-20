"""

Defines the base Event abstraction for the simulation.
Events represent time-based or triggered occurrences such
as disasters or internal system signals.
"""

import time
import uuid
import logging
from typing import Dict, Any


class Event:
    """
    Base class for all simulation events.
    """

    def __init__(self, event_type: str, data: Dict[str, Any]):
        """
        Initialize an Event.

        :param event_type: Identifier of event category.
        :param data: Event-specific payload.
        """
        self.id: str = str(uuid.uuid4())
        self.type: str = event_type
        self.data: Dict[str, Any] = data
        self.timestamp: float = time.time()

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Event created: %s", self)

    def __repr__(self) -> str:
        """
        String representation.

        :return: Event representation.
        """
        return f"<Event id={self.id} type={self.type}>"
