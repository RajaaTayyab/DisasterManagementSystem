"""
behaviors/panic.py

Models panic escalation and de-escalation behavior.

Primarily used by civilians but applicable to any agent
with stress-sensitive decision-making.
"""

import logging
import random


class PanicBehavior:
    """
    Represents panic as a bounded internal state.

    GAIA Concept:
    - Internal state affecting role permissions and actions
    """

    def __init__(self):
        self.level = 0.0  # range [0.0, 1.0]
        self._logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------

    def increase(self, intensity: float) -> None:
        """
        Increase panic level.

        :param intensity: Panic increment
        """
        self.level = min(1.0, self.level + intensity)
        self._logger.debug("Panic increased to %.2f", self.level)

    def decrease(self, calm_factor: float) -> None:
        """
        Reduce panic level.

        :param calm_factor: Reduction factor
        """
        self.level = max(0.0, self.level - calm_factor)
        self._logger.debug("Panic decreased to %.2f", self.level)

    # ------------------------------------------------------------------

    def is_panicking(self) -> bool:
        """
        Determine if agent is panicking.

        :return: Boolean panic state
        """
        return self.level > 0.6

    def decision_noise(self) -> float:
        """
        Generate randomness proportional to panic.

        Used to perturb rational decisions.

        :return: Noise factor
        """
        noise = random.uniform(-self.level, self.level)
        self._logger.debug("Decision noise %.2f", noise)
        return noise
