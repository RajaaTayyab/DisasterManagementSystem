"""
Maintains a registry of active agents in the system.
Provides lookup and lifecycle management functionality.
"""

import logging
from typing import Dict, Optional


class AgentRegistry:
    """
    Centralized registry for all agents.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._agents: Dict[str, object] = {}

    def register(self, agent_id: str, agent: object) -> None:
        """
        Register an agent with the system.

        :param agent_id: Unique identifier.
        :param agent: Agent instance.
        """
        self._agents[agent_id] = agent
        self._logger.info("Agent registered: %s", agent_id)

    def unregister(self, agent_id: str) -> None:
        """
        Remove an agent from the registry.

        :param agent_id: Agent ID.
        """
        self._agents.pop(agent_id, None)
        self._logger.info("Agent unregistered: %s", agent_id)

    def get(self, agent_id: str) -> Optional[object]:
        """
        Retrieve an agent by ID.

        :param agent_id: Agent identifier.
        :return: Agent instance or None.
        """
        return self._agents.get(agent_id)
