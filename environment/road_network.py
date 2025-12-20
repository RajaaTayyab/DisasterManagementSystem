"""

Defines a graph-based road network used for navigation and evacuation.
"""

import logging
from typing import Dict, List, Tuple


class RoadNetwork:
    """
    Represents roads and intersections as a graph.
    """

    def __init__(self):
        self.nodes: Dict[str, Tuple[int, int]] = {}
        self.edges: Dict[str, List[str]] = {}
        self.blocked_edges: set = set()

        self._logger = logging.getLogger(self.__class__.__name__)

    def add_node(self, node_id: str, position: Tuple[int, int]) -> None:
        self.nodes[node_id] = position
        self.edges.setdefault(node_id, [])

    def connect(self, node_a: str, node_b: str) -> None:
        self.edges[node_a].append(node_b)
        self.edges[node_b].append(node_a)

    def block_edge(self, node_a: str, node_b: str) -> None:
        self.blocked_edges.add((node_a, node_b))
        self.blocked_edges.add((node_b, node_a))
        self._logger.warning("Road blocked between %s and %s", node_a, node_b)

    def is_accessible(self, node_a: str, node_b: str) -> bool:
        return (node_a, node_b) not in self.blocked_edges
