"""
Implements the central message routing mechanism for the
multi-agent system. The message bus decouples agents and enables
asynchronous communication.
"""

import logging
import heapq
from typing import Dict, List
from core.message import Message


class MessageBus:
    """
    Central mediator responsible for routing messages between agents.

    Implements a priority queue to ensure time-critical messages
    are processed first.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageBus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._queue: List = []
        self._subscribers: Dict[str, List[str]] = {}

    def subscribe(self, agent_id: str, message_type: str) -> None:
        """
        Subscribe an agent to a specific message type.

        :param agent_id: ID of subscribing agent.
        :param message_type: Message category to subscribe to.
        """
        self._subscribers.setdefault(message_type, []).append(agent_id)
        self._logger.debug(
            "Agent %s subscribed to message type %s", agent_id, message_type
        )

    def publish(self, message: Message) -> None:
        """
        Publish a message to the bus.

        :param message: Message instance to enqueue.
        """
        heapq.heappush(self._queue, (message.priority, message.timestamp, message))
        self._logger.debug("Message enqueued: %s", message)

    def dispatch(self) -> List[Message]:
        """
        Dispatch all queued messages.

        This method retrieves messages in priority order
        and returns them for delivery by the simulation loop.

        :return: Ordered list of messages to be delivered.
        """
        dispatched = []
        while self._queue:
            _, _, message = heapq.heappop(self._queue)
            dispatched.append(message)
            self._logger.debug("Message dispatched: %s", message)
        return dispatched
