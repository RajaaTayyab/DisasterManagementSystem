"""
Defines the Message abstraction used for inter-agent communication
within the disaster management multi-agent system.

This module is GAIA-aligned and supports asynchronous, event-driven
communication with extensibility for priorities, acknowledgements,
and broadcast messaging.
"""

import uuid
import time
import logging
from enum import Enum
from typing import Any, Dict, Optional


class MessageType(Enum):
    """
    Enumeration of supported message categories.
    """

    INFORM = "inform"
    REQUEST = "request"
    COMMAND = "command"
    RESPONSE = "response"
    ALERT = "alert"
    EVENT = "event"


class Message:
    """
    Represents a single immutable message exchanged between agents.

    Messages are treated as value objects and should not be modified
    once created. They may be routed through a message bus and queued
    for asynchronous processing.
    """

    def __init__(
        self,
        sender_id: str,
        receiver_id: Optional[str],
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: int = 5,
        correlation_id: Optional[str] = None,
    ):
        """
        Initialize a Message instance.

        :param sender_id: Unique ID of the sending agent.
        :param receiver_id: Unique ID of the receiving agent (None for broadcast).
        :param message_type: Category of the message.
        :param payload: Arbitrary message content.
        :param priority: Message priority (lower = higher priority).
        :param correlation_id: Optional ID to correlate request/response flows.
        """
        self.id: str = str(uuid.uuid4())
        self.sender_id: str = sender_id
        self.receiver_id: Optional[str] = receiver_id
        self.type: MessageType = message_type
        self.payload: Dict[str, Any] = payload
        self.priority: int = priority
        self.timestamp: float = time.time()
        self.correlation_id: str = correlation_id or self.id

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug(
            "Message created: id=%s sender=%s receiver=%s type=%s",
            self.id,
            self.sender_id,
            self.receiver_id,
            self.type.value,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the message to a dictionary.

        :return: Dictionary representation of the message.
        """
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "type": self.type.value,
            "payload": self.payload,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
        }

    def __repr__(self) -> str:
        """
        Developer-friendly string representation.

        :return: String representation.
        """
        return (
            f"<Message id={self.id} "
            f"type={self.type.value} "
            f"sender={self.sender_id} "
            f"receiver={self.receiver_id}>"
        )
