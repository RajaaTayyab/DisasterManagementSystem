#  Disaster  & Emergency Response System

A simulation-based **Disaster Management System** that models emergency scenarios using an **agent-based architecture** and **event-driven communication**.


##  Features
-  Agent-based simulation with intelligent agents  
-  Event-driven architecture with central event queue  
-  Environment modeling (city/map simulation)  
- Dynamic behaviors (movement, routing, panic, triage)  
-  YAML-based configuration system  
- Logging and simulation metrics  



##  Project Structure

```bash
DisasterManagementSystem/
│
├── agents/                # Agent implementations
├── behaviors/             # Behavior logic (movement, routing, etc.)
├── config/                # YAML configuration files
│   ├── agent_config.yaml
│   ├── environment_config.yaml
│   └── simulation_config.yaml
│
├── core/                  # Core system components
│   ├── agent_base.py
│   ├── event.py
│   ├── event_queue.py
│   ├── message_bus.py
│   └── registry.py
│
├── environment/           # Environment models
├── utils/                 # Utilities (logging, visualization)
├── main.py                # Entry point
└── README.md
```

---

##  Getting Started



###  Install Dependencies

```bash
pip install -r requirements.txt
```

If no requirements file exists:

```bash
pip install pyyaml
```

---

###  Run the Simulation

```bash
python main.py
```

---

##  Configuration

All configurations are located in the `config/` directory:

- `agent_config.yaml` → Agent definitions  
- `environment_config.yaml` → Environment settings  
- `simulation_config.yaml` → Simulation control  

Modify these files to customize system behavior.

---

##  Core Concepts

### Agents
Entities that perform actions and interact with the environment.

### Event Queue
Handles all system events in a time-driven manner.

### Message Bus
Facilitates communication between agents.

### Behaviors
Defines how agents act:
- Movement  
- Panic response  
- Routing  
- Triage  

---

##  Output

- Simulation logs  
- Event tracking  
- Metrics output  



## Technologies Used

- Python  
- YAML  
- Agent-based modeling  
- Event-driven systems  

