*Note:* This documentation is my initial thought process prior to any code development and very much subject to change over the course of this project. 

# Multi-agent Navigation and Weapons Scheduling Environment
This is is a multi-agent navigation and weapons scheduling Gymnasium environment with baseline command and control algorithms. The initial develop is starting very simple in order to support rapid prototyping of software architecture, data flow, and experimenting with a variety of command and control algorithms. The intention is to incrementally grow capability and transition to higher fidelity models and simulation for increasing domain knowledge at each stage of development. While the intention is to stretch this project to the highest fidelity possible in the open source world, it is still a hobby project focused on experimenting with and evaluating a variety of ideas that I have been curious to explore.

# Scenario Configuration
The environment scenario configuration file (scenario.json) defines the initial state of the environment and references configuration files for each platform (<platform_name>.json), which references configuration files for each subsystem (<radar_name>.json, <weapon_name>.json).

## Configuration Structure
* Scenario Configuration:
  * Geodetic/Airspace Operating Area
  * Geodetic/Airspace Restricted Area
  * Geodetic/Airspace Protected Area
  * Team (Teams in scenario, can have multiple)
    * Common Operating Picture (COP) State
    * Common Operating Picture (COP) Uncertainty
      * Within Team
      * Between Team
    * Agent (Agents on team, can be multiple)
      * Duplicates (number of duplications of this agent config on this team)
      * Individual Platform State
      * Platform Type
        * Maximum Fuel
        * Maximum Thrust
      * Sensor Systems
        * Sensor Type
          * Field Of View (FOV)
          * Range
          * Probability of Detect (Pd)
      * Weapons Inventory
        * Weapon Type
            * Weapon Engagement Zone (WEZ)
              * Field Of View (FOV)
              * Range
            * State
            * Fuel
            * Warmup Delay
            * Trust
            * Probability of Kill (Pk)
    
# Environment
The environment carries a "God's Eye View", or "Ground Truth" global state. The initial state is built from the conditions defined by the scenario configuration.  

# Teams
There are four team options: 
* Blue - Friendly Forces
* Red - Adversary Forces
* Grey - Civilian Platforms
* Green - Ally Forces 

# Common Operating Picture (COP)
The COP is the shared state among all cooperating agents. This allows agents to have situational awareness beyond their sensor information.

## Uncertainty Within Team
Uncertainty applied to that teams COP estimated state of agents on the same team.
  - 0% if assuming perfect communications
  - likely a low uncertainty within the same team

## Uncertainty Between Team
Uncertainty applied to that teams COP estimated state of agents on another team
    - likely 100% between opposing teams (Blue/Red) that would not be communicating their state with one another
      - Could be < 100% as a surrogate representation of cyber capabilities
    - likely a low uncertainty (but more than within team) between allied teams (Blue/Green) since they would be communicating their state with on another
    - likely a low uncertainty between any team and the Grey Team, since they are likely broadcasting their state over AIS/ADS-B


# Platform

## Platform Types
This simulation supports surface and air platforms.

## Platform Features

# Weapons

## Weapon Types

### Guns

### Short Range Hardkill (SHK) - Within Visual Range (WVR) Air-to-Air Missile 

### Medium Range Hardkill (MHK)  - Within Visual Range (WVR) Air-to-Air Missile 

### Softkill (EWSK) - Electronic Counter Measures (ECM)

## Weapon Features

# Controllers

## Predicted Intercept Point
### Intercept
### Lead 
### Lag

## Command to Line-Of-Sight (CLOS)

## Pure Pursuit

## Proportional Navigation (ProNav)

## Non-linear Model Predictive Control (NMPC)

## Reinforcement Learning (RL)


# Future Features/Capability

## Environment Upgrades
* Upgrade from a simple Python Turtle Graphics 2D simulator and 2-DOF dynamics model to a 3D simulator and 6-DOF dynamics model
* Incorporate open source terrain data, like Digital Terrain Elevation Data (DTED), and Building data, like OpenStreetMap (OSM) Buildings 
* Incorporate higher fidelity dynamics models, like JSBSim and Unreal Engine

## Decision Making Features
The purpose of this is to give the agents the same information pilot's use from their Pilot's Operating Handbook (POH) to understand the operating limits of the platform and how to optimize their control input to that specific system.

### Static Features
* V<sub>X</sub> - airspeed for best angle of climb
* V<sub>Y</sub> - airspeed forbest rate of climb
* V<sub>NE</sub> - airspeed to never exceed
* V<sub>MAX</sub> - airspeed for maximum cruise structural limit
* V<sub>A</sub> - airspeed for maximum maneuver structural limit or in turbulent/windy conditions
* LL - Load Limit ("G Limit")
* Critical AOA - Angle Of Attack at which the aircraft will stall
* OEW - Operating Empty Weight

### Dynamic Features
* P<sub>S</sub> - aircraft-specific energy
* n - load factor
* TCA - track crossing angle
* AOT - angle off tail
* Usable Fuel

## Analysis of Results
* Controller stability/sensitivity analysis
* Game theoretic tactics analysis
  * cooperative/non-cooperative components analysis
  * zero sum/non-zero sum components analysis
  * Proper equilibrium
