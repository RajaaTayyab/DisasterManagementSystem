"""

Defines the GAIA Role abstraction. 
Roles encapsulate responsibilities, permissions,
and interaction protocols independently of agents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Set


class Role(ABC):
    """
    Abstract base class for GAIA roles.
    """

    def __init__(self, name: str):
        self.name: str = name
        self.permissions: Set[str] = set()
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def responsibilities(self) -> str:
        """
        Describe the role's responsibilities.

        :return: Responsibility description.
        """
        pass

    @abstractmethod
    def liveness(self) -> str:
        """
        Define liveness properties.

        :return: Liveness condition.
        """
        pass

    @abstractmethod
    def safety(self) -> str:
        """
        Define safety properties.

        :return: Safety condition.
        """
        pass

    def add_permission(self, permission: str) -> None:
        """
        Grant a permission to this role.

        :param permission: Permission identifier.
        """
        self.permissions.add(permission)
        self._logger.debug("Permission added to role %s: %s", self.name, permission)
