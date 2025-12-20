"""

Entry point for the Disaster Management & Emergency Response System.



GAIA Alignment:
- Agents enact their roles
- Event-driven inter-agent communication
- Liveness properties maintained via time-stepped updates
"""

import os
import yaml
import time
import logging
from typing import Dict, Any

from utils.logger import configure_logging
from utils.visualization import print_simulation_header, print_step, print_metrics

from core.registry import AgentRegistry
from core.event_queue import EventQueue

from environment.city_map import CityMap
from agents.sensor_agent import SensorAgent

#File paths for routing 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")


def load_yaml_config(filename: str) -> Dict[str, Any]:
    
    #Load a YAML configuration file from the absolute config directory.
    
    path = os.path.join(CONFIG_DIR, filename)
    with open(path, "r") as f:
        return yaml.safe_load(f)


def initialize_environment(env_config: Dict[str, Any]) -> CityMap:
    city_cfg = env_config.get("environment", {}).get("city", {})
    width = city_cfg.get("width", 500)
    height = city_cfg.get("height", 500)
    city = CityMap(width=width, height=height)
    logging.getLogger("main").info(
        "Environment initialized: width=%s height=%s", width, height
    )
    return city


def initialize_agents(agent_config: Dict[str, Any], registry: AgentRegistry):
    sensors_cfg = agent_config.get("agents", {}).get("sensor_agent", {})
    num_sensors = 3  # Can be parameterized

    for i in range(num_sensors):
        loc = (100 + i * 50, 100 + i * 50)
        sensor = SensorAgent(
            name=f"Sensor-{i+1}",
            location=loc,
            detection_radius=sensors_cfg.get("detection_radius", 100.0),
            failure_rate=sensors_cfg.get("failure", {}).get(
                "failure_probability_per_step", 0.01
            ),
            noise_level=sensors_cfg.get("noise", {}).get("gaussian_stddev", 0.1),
        )
        registry.register(sensor.id, sensor)


def run_simulation(sim_config, env_config, agent_config):
    logger = logging.getLogger("main")
    registry = AgentRegistry()
    event_queue = EventQueue()
    city = initialize_environment(env_config)
    initialize_agents(agent_config, registry)

    timestep = sim_config.get("simulation", {}).get("time", {}).get(
        "timestep_seconds", 1.0
    )
    max_duration = sim_config.get("simulation", {}).get("time", {}).get(
        "max_duration_seconds", 60
    )

    print_simulation_header()
    logger.info("Simulation started")

    current_time = 0.0
    step = 0

    while current_time < max_duration:
        print_step(step, current_time)

        #  Agent Perception Cycle 
        for agent in list(registry._agents.values()):
            agent.perceive()

        #  Event Queue Processing 
        while not event_queue.is_empty():
            event = event_queue.pop_next()
            logger.warning("Processing event: %s", event)

    


            # Apply environmental impact if event generates hazard
            if hasattr(event, "generate_hazard"):
                hazard = event.generate_hazard()
                city.add_hazard_zone(hazard)

        # Environment Update 
        city.update(timestep)

        time.sleep(0.05)  # pacing for readability
        current_time += timestep
        step += 1

    logger.info("Simulation ended")


if __name__ == "__main__":
    configure_logging(logging.INFO)

    # Load configs from absolute path
    simulation_config = load_yaml_config("simulation_config.yaml")
    agent_config = load_yaml_config("agent_config.yaml")
    environment_config = load_yaml_config("environment_config.yaml")

    # Run simulation
    run_simulation(simulation_config, environment_config, agent_config)
