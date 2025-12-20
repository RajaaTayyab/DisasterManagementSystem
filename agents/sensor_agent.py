"""
This module defines the SensorAgent, a core perception agent within the
Disaster Management & Emergency Response System.

GAIA Alignment
--------------
Role Enacted:
- ObserverRole

GAIA Responsibilities:
- Observe the environment for disaster-related signals
- Detect earthquakes and fires with probabilistic uncertainty
- Filter noise and handle sensor degradation/failure
- Escalate validated observations as simulation events

Design Notes
------------
- This agent does NOT directly modify the environment.
- It publishes disaster events to the EventQueue.
- It is intentionally conservative to avoid false positives.
- Multiple SensorAgents may coexist and overlap spatially.

This file intentionally contains rich internal logic and documentation,
as it represents the perception backbone of the entire system.
"""

import logging
import random
import math
from typing import Optional, Tuple, Dict

from core.agent_base import Agent
from core.event_queue import EventQueue
from core.event import Event

from roles.observer_role import ObserverRole
from disasters.earthquake import Earthquake
from disasters.fire import Fire


class SensorAgent(Agent):
    """
    SensorAgent is responsible for perceiving low-level environmental signals
    and converting them into high-level disaster events.

    The agent simulates:
    - Sensor noise
    - Missed detections
    - False negatives
    - Complete sensor failure

    This agent is *reactive* and *stateless with respect to command authority*.
    It never issues commands—only observations.
    """

    def __init__(
        self,
        name: str,
        location: Tuple[int, int],
        detection_radius: float = 100.0,
        failure_rate: float = 0.02,
        noise_level: float = 0.15,
    ):
        """
        Initialize the SensorAgent.

        :param name: Human-readable identifier
        :param location: (x, y) coordinates of the sensor
        :param detection_radius: Maximum sensing radius
        :param failure_rate: Probability of total sensor failure per cycle
        :param noise_level: Degree of signal distortion (0–1)
        """
        super().__init__(name=name)

        # Spatial properties
        self.location: Tuple[int, int] = location
        self.detection_radius: float = detection_radius

        # Reliability modeling
        self.failure_rate: float = failure_rate
        self.noise_level: float = noise_level

        # Internal operational state
        self.operational: bool = True
        self.last_detection_time: Optional[float] = None

        # Detection thresholds
        self.earthquake_threshold: float = 4.5
        self.fire_threshold: float = 0.6

        # Role assignment (GAIA-compliant)
        self.observer_role = ObserverRole()
        self.add_role(self.observer_role)

        # Core infrastructure
        self._event_queue = EventQueue()
        self._logger = logging.getLogger(self.__class__.__name__)

        self._logger.info(
            "SensorAgent initialized at %s with radius %s",
            self.location,
            self.detection_radius,
        )


    def perceive(self) -> None:
        """
        Perceive the environment.

        In a full simulation, this method would ingest raw sensor feeds.
        Here, it probabilistically simulates environmental signals.
        """
        if not self.operational:
            self._logger.debug("Sensor offline; skipping perception cycle")
            return

        # Random chance of catastrophic sensor failure
        if random.random() < self.failure_rate:
            self.operational = False
            self._logger.error("SensorAgent has failed and is now offline")
            return

        # Simulated raw signal generation
        raw_signals = self._simulate_raw_signals()
        self._process_signals(raw_signals)

    def decide(self) -> None:
        """
        Decision phase.

        For SensorAgent, decision-making is embedded in signal processing.
        This method exists to preserve the perceive–decide–act contract.
        """
        # No deferred decisions; logic handled immediately in perceive()
        pass

    def act(self) -> None:
        """
        Action phase.

        SensorAgent actions consist solely of publishing validated events.
        """
        # Actions are executed immediately during perception
        pass

    # SENSOR LOGIC

    def _simulate_raw_signals(self) -> Dict[str, float]:
        """
        Simulate raw environmental signals.

        This models imperfect sensing:
        - Signals may be noisy
        - Signals may be absent even if disaster exists

        :return: Dictionary of signal intensities
        """
        earthquake_signal = random.gauss(mu=0.0, sigma=1.0)
        fire_signal = random.random()

        # Apply noise distortion
        earthquake_signal *= (1 + random.uniform(-self.noise_level, self.noise_level))
        fire_signal *= (1 + random.uniform(-self.noise_level, self.noise_level))

        self._logger.debug(
            "Raw signals detected: earthquake=%s fire=%s",
            earthquake_signal,
            fire_signal,
        )

        return {
            "earthquake": abs(earthquake_signal),
            "fire": max(0.0, fire_signal),
        }

    def _process_signals(self, signals: Dict[str, float]) -> None:
        """
        Process raw signals and determine whether escalation is required.

        This method applies GAIA ObserverRole logic to decide whether
        observations are significant enough to generate events.
        """
        # Earthquake detection
        if signals["earthquake"] >= self.earthquake_threshold:
            magnitude = self._estimate_magnitude(signals["earthquake"])
            observation = {
                "type": "earthquake",
                "severity": magnitude,
                "validated": True,
            }

            if self.observer_role.evaluate_observation(observation):
                self._publish_earthquake(magnitude)

        # Fire detection
        if signals["fire"] >= self.fire_threshold:
            intensity = self._estimate_fire_intensity(signals["fire"])
            observation = {
                "type": "fire",
                "severity": intensity,
                "validated": True,
            }

            if self.observer_role.evaluate_observation(observation):
                self._publish_fire(intensity)

    # EVENT GENERATION

    def _publish_earthquake(self, magnitude: float) -> None:
        """
        Publish an Earthquake event to the EventQueue.

        :param magnitude: Estimated Richter magnitude
        """
        event = Earthquake(epicenter=self.location, magnitude=magnitude)
        self._event_queue.schedule(event)

        self._logger.warning(
            "Earthquake detected! Magnitude=%s at %s",
            magnitude,
            self.location,
        )

    def _publish_fire(self, intensity: float) -> None:
        """
        Publish a Fire event to the EventQueue.

        :param intensity: Fire intensity estimate
        """
        event = Fire(origin=self.location, intensity=intensity)
        self._event_queue.schedule(event)

        self._logger.warning(
            "Fire detected! Intensity=%s at %s",
            intensity,
            self.location,
        )


    # UTILITY METHODS
    

    def _estimate_magnitude(self, signal: float) -> float:
        """
        Convert a raw seismic signal into a magnitude estimate.

        Uses a logarithmic compression to avoid unrealistically large values.
        """
        magnitude = max(3.0, min(9.5, math.log10(signal + 1) * 6))
        self._logger.debug("Estimated earthquake magnitude: %s", magnitude)
        return magnitude

    def _estimate_fire_intensity(self, signal: float) -> float:
        """
        Convert raw fire signal into a bounded intensity value.
        """
        intensity = max(0.1, min(10.0, signal * 10))
        self._logger.debug("Estimated fire intensity: %s", intensity)
        return intensity

    # DIAGNOSTICS & RECOVERY

    def reset_sensor(self) -> None:
        """
        Attempt to recover a failed sensor.

        This does not guarantee recovery and is intentionally conservative.
        """
        if not self.operational and random.random() < 0.3:
            self.operational = True
            self._logger.info("SensorAgent successfully reset and operational")
        else:
            self._logger.debug("Sensor reset attempt failed")
