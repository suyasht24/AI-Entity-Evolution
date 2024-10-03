# EvoSim

EvoSim is a dynamic 2D simulation where entities learn to avoid threats, collect food, and adapt their behavior using reinforcement learning. The entities evolve by learning from their past experiences to optimize their survival in a hostile environment.

## Features

- **Reinforcement Learning**: Entities adapt and improve their ability to avoid threats based on past encounters.
- **Collision Avoidance**: Entities avoid threats and intelligently navigate the environment.
- **Visual Representation**: Displays the simulation in real-time, showing entities, threats, and food scattered around the world.
- **Graphical Performance**: A graph at the end shows the number of collisions over time for each entity (Male and Female).

## How It Works

The simulation starts with two entities (one male and one female) that must collect food to survive and avoid randomly spawning threats. As they encounter threats, they learn to avoid them, improving over time. The program tracks each entity's collisions with threats and presents the data graphically at the end.

### Key Components

- **Entities**: Represented as blue (male) and pink (female) circles.
- **Threats**: Red circles that entities must avoid.
- **Food**: Green dots that entities consume to gain energy.
- **Learning Mechanism**: The entities learn from each encounter with a threat and adapt to avoid it in the future.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-entity-evolution.git

2. Navigate to the project directory:
   cd ai-entity-evolution
   
4. Install the required dependencies:
   pip install pygame matplotlib

## Running the Project
1. To start the simulation, run the following command:
    python main.py

2. The simulation will run for 60 seconds per cycle, tracking the number of collisions for both entities during that period.

3. At the end of the simulation, a graph showing the time vs. collision data for both male and female entities will be displayed.

## Usage
- **Control the Simulation**: Watch how the entities learn to avoid threats and collect food in real time.
- **Data Visualization**: Observe the collision data between entities and threats using graphical outputs at the end of the simulation.
  
## Example
After running the simulation, the final output graph will look like this:

- **Blue Line**: Represents the male entity's collisions over time.
- **Pink Line**: Represents the female entity's collisions over time.
The entities adapt their behavior based on these interactions, improving their chances of survival.

## Future Enhancements
- **Advanced Learning Algorithms**: Implement more complex reinforcement learning techniques to enhance threat avoidance.
- **Dynamic World Expansion**: Introduce more entities and obstacles, creating a richer environment.
- **Reproduction**: Add a reproduction feature where entities can reproduce and create new generations that inherit learned behaviors.

## Author
**Suyash Thamake**
