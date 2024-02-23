## About the Project
In this project, we simulated the food search behavior of ants using Python and the Pygame library. The simulation involves a group of ants navigating through an environment, searching for food sources, and depositing pheromones to communicate with each other. The ants are equipped with various behaviors, including the ability to follow pheromone trails, find and carry food, and navigate back to the nest.

## Dependencies

 - **Python**
 - **Pygame**
 - **Numpy**

## Installation
First Clone the Github repository:
```
git clone https://github.com/lucasthierry17/Ant_Project.git
```
Go into the repository:
```
cd Ant_Project
```
then install all Dependencies:
```
pip install -r requirements.txt
```

## How to run the simulation
1. navigate to the **`source`** folder:
   ```console
   cd source
   ```
2. run the **`main.py`** file
   ```console
   python main.py
   ```
### First you see the start menu
![start_menu](https://github.com/lucasthierry17/Ant_Project/assets/96741488/d2f7ec1c-a1a1-4cbb-847e-0d474dcc7cfe)
- here you can select the parameters you want
- type in a value for the number of ants
- then type in a speed value
- press the **START** button to start the simulation

### Then the simulation screen opens
![Screenshot](simulation_screen.png)

### Food Placement
You can place and remove food sources by simple mouse clicks

https://github.com/lucasthierry17/Ant_Project/assets/96741488/c9d30cf5-9261-4a96-8739-0196ba421fdf
- press **left mouse button** to place a new food source where you want
- press **right mouse button** on the food source you want to remove

### Restart with new parameters
To restart the simulation with new parameters simpy press **`ESCAPE`**

- Then the simulation stops and the start menu reopens
- there you can put in new variables and restart the simulation

## Developer Documentation
Welcome to the developer documentation for the Ant Search Behavior Simulation project. This guide is designed to assist developers in understanding the project structure, code architecture, customization options, and how to extend the functionality of the simulation.

## 1. Project Structure
The project is structured as follows:
- **`main.py`**: The main entry point for the simulation
- **`start_screen.py`**: Contains the StartMenu class for user configuration
- **`tests/`**: Directory containing test cases

## 2. Code Architecture
### 2.1 Ant Class ('Ants')
- each ant is represented as an instance of the **'Ants'** class
- ants have an initial starting position at the nest, and they move in the environment following a desired direction
- the ants exhibit dynamic behavior, such as turning around when reaching the nest or a food source, moving towards the nest when carrying food, and responding to pheromones
- the speed of the ants can be adjusted, allowing for different movement rates

### 2.2 Pheromone Class ('Pheromones')
- the **'Pheromones'** class represents the pheromone grid that ants use to communicate
- Pheromones are updated over time with an evaporation rate, creating a dynamic environment where pheromone trails fade over time
- pheromone levels are adjusted based on ant behavior, such as depositing pheromones when carrying food

### Simulation Environment:
- the simulation is displayed using Pygame, a popular game development library
- the environment consists of a nest, food sources, and a grid representing the pheromone levels
- users can interact with the simulation by adding or removing food sources using mouse clicks

### User Interface ('StartMenu'):
- the simulation includes a start menu allowing users to configure parameters before starting the simulation
- users can specify the number of ants and the speed of their movement.

## Code Diagramm
![Code_Diagramm](https://github.com/lucasthierry17/Ant_Project/assets/96741488/a4b8e4c2-c7da-4e99-bea9-e0ab46e194bf)


## 3. Customization
### 3.1 Adjustable Parameters
- Number of Ants: Modify the **`num_ants`** variable in **`main.py`**
- Ant Speed: Adjust the **`speed`** parameter when creating Ants instances in **`main.py`**
- Evaporation Rate: Change the rate in the **'Pheromones'** class constructor

## 4. API Documentation
### 4.1 Ants Class
4.1.1 **`__init__(self, nest, pheromones, speed)`**
- **Parameters:**
  - **`nest`**: Tuple, starting position of the ant.
  - **`pheromones`**: Pheromones instance for communication.
  - **`speed`**: Float, speed of ant movement.

4.1.2 **`update(self)`**
- Update the ant's position and behavior in the simulation

4.1.3 **`calculate_distance(self, start, target)`**
- Calculate the Euclidean distance between two points

4.1.4 **`turn_around(self)`**
- Change the ant's direction to simulate turning around

### 4.2 Pheromones Class
4.2.1 **`__init__(self, big_screen_size)`**
- **Parameters:**
  - **`big_screen_size`**: Tuple, size of the pheromone grid

4.2.2 **`update(self)`**
- Update the pheromone levels, simulating evaporation

4.2.3 **`reset(self)`**
- Reset the pheromone grid to its initial state

## 5. Extending Functionality
- Developers can extend functionality by subclassing existing classes or adding new features within the provided structure
- Follow the principles of object-oriented programming for modularity and maintainability

## 6. Testing
- Test cases are available in the **'tests/'** directory
- Run tests using a test runner such as pytest:
  ```console
  pytest tests/
  ```

## 7. Contributing
- Contributions are welcome! Fork the repository, make changes, and submit a pull request
- Follow the contribution guidelines in the repository


## Authors

- [Lucas Müller](https://github.com/LucasThierry17)
- [Fouad Mokhtari](https://github.com/Fouad1806)
- [Sven Ochmann](https://github.com/svenatgithub)
- [Nick Grabowski](https://github.com/nickno7)


**Thank you for your interest in the Ant Search Simulation project!**  


