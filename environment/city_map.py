"""

Defines the CityMap model that represents the global simulation
environment. The city map acts as a spatial container for buildings,
roads, hospitals, and hazard zones.

This module is environment-only and does not contain agent logic.
"""

import logging
from typing import Dict, List, Tuple, Optional
from environment.building import Building
from environment.road_network import RoadNetwork
from environment.hazard_zone import HazardZone
from environment.hospital import Hospital


class CityMap:
    """
    Represents the complete simulated city.

    Acts as the authoritative spatial and structural model
    against which disasters and agents interact.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.buildings: Dict[str, Building] = {}
        self.hospitals: Dict[str, Hospital] = {}
        self.hazard_zones: List[HazardZone] = []
        self.road_network = RoadNetwork()

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("CityMap initialized (%sx%s)", width, height)

    def add_building(self, building: Building) -> None:
        self.buildings[building.id] = building
        self._logger.debug("Building added: %s", building.id)

    def add_hospital(self, hospital: Hospital) -> None:
        self.hospitals[hospital.id] = hospital
        self._logger.debug("Hospital added: %s", hospital.id)

    def add_hazard_zone(self, hazard: HazardZone) -> None:
        self.hazard_zones.append(hazard)
        self._logger.debug("Hazard zone added: %s", hazard)

    def get_buildings_in_radius(
        self, center: Tuple[int, int], radius: float
    ) -> List[Building]:
        """
        Retrieve all buildings within a given radius.

        :param center: (x, y) coordinate
        :param radius: radius value
        """
        affected = []
        for building in self.buildings.values():
            if building.distance_to(center) <= radius:
                affected.append(building)
        return affected

    def update(self, timestep: float) -> None:
        """
        Advance environment state.

        Updates hazard zones and structural degradation.
        """
        for hazard in self.hazard_zones:
            hazard.update(timestep)

        for building in self.buildings.values():
            building.update(timestep)

    def get_safe_zones(self) -> List[Tuple[int, int]]:
        """
        Compute locations not affected by any hazard zone.
        """
        safe_locations = []
        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                if all(not hz.contains((x, y)) for hz in self.hazard_zones):
                    safe_locations.append((x, y))
        return safe_locations
