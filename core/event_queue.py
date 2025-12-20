"""

Provides a time-ordered event queue used to drive
the simulation forward.
"""

import heapq
import logging
from typing import List
from core.event import Event


class EventQueue:
    """
    Priority-based event scheduler.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventQueue, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._queue: List = []

    def schedule(self, event: Event, delay: float = 0.0) -> None:
        """
        Schedule an event for execution.

        :param event: Event to schedule.
        :param delay: Delay in seconds before event is processed.
        """
        execution_time = event.timestamp + delay
        heapq.heappush(self._queue, (execution_time, event))
        self._logger.debug("Event scheduled: %s at %f", event, execution_time)

    def pop_next(self) -> Event:
        """
        Retrieve the next scheduled event.

        :return: Next Event instance.
        """
        _, event = heapq.heappop(self._queue)
        self._logger.debug("Event popped: %s", event)
        return event

    def is_empty(self) -> bool:
        """
        Check whether the queue is empty.

        :return: True if empty.
        """
        return len(self._queue) == 0
