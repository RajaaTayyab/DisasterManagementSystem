"""

Defines the abstract Agent base class.
Agents enact roles and interact via messages and events.
"""

import logging
import uuid
from abc import ABC, abstractmethod
from typing import List

from core.message import Message
from core.message_bus import MessageBus
from core.registry import AgentRegistry
from core.role_base import Role


class Agent(ABC): #This is the main agent class 
    """
    Abstract base class for all agents in the system.
    """

    def __init__(self, name: str):
        """
        Initialize the agent.

        :param name: Human-readable name.
        """
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.roles: List[Role] = []

        self._logger = logging.getLogger(self.__class__.__name__)
        self._bus = MessageBus()
        self._registry = AgentRegistry()

        self._registry.register(self.id, self)
        self._logger.info("Agent initialized: %s (%s)", self.name, self.id)

    def add_role(self, role: Role) -> None:
        """
        We are  Assigning a role to this agent.

        :param role: Role instance.
        """
        self.roles.append(role)
        self._logger.debug("Role %s assigned to agent %s", role.name, self.id)

    def send_message(self, message: Message) -> None:
        """
        Send a message via the message bus.

        :param message: Message to send.
        """
        self._bus.publish(message)
        self._logger.debug("Agent %s sent message %s", self.id, message.id)

    @abstractmethod
    def perceive(self) -> None:
        """
        Perceive the environment or incoming events.
        """
        pass

    @abstractmethod
    def decide(self) -> None:
        """
        Decide next actions based on perceptions.
        """
        pass

    @abstractmethod
    def act(self) -> None:
        """
        Execute decided actions.
        """
        pass

    def shutdown(self) -> None:
        """
        Gracefully remove the agent from the system.
        """
        self._registry.unregister(self.id)
        self._logger.info("Agent shutdown: %s", self.id)
