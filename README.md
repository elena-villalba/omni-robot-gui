# omni-robot-gui

The repository contains Python code for a GUI designed for the real-time simulation of a three-wheeled omnidirectional robot. The GUI enables the simulation and verification of both forward and inverse kinematics of the robot. Additionally, it tests the implemented control law by directing the robot to follow a predefined path.
During the inverse kinematics and path planning simulations, two real-time graphs display the robot's speed and error. The path planning simulation also includes an option to export data to a CSV file for further analysis.

This code was developed as part of my Master's thesis project.

## Prerequisites

- Python 3.10.12
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/omni-robot-gui.git
    cd omni-robot-gui
    ```

2. **Install Python 3 virtual environment library**
    ```sh
    sudo apt install python3.10-venv
    ```

3. **Create a virtual environment in the same folder that contains the downloaded code**
    ```sh
    python3 -m venv omni-gui-env
    ```

4. **Activate the virtual environment**
    ```sh
    source omni-gui-env/bin/activate
    ```

5. **Install the required libraries**
    ```sh
    pip install -r requirements.txt
    ```


## Usage

1. **Run the GUI**
    ```sh
    python main.py
    ```

2. **Simulate and verify kinematics**
    - Use the GUI to select either forward or inverse kinematics.
    - Observe the real-time graphs displaying the robot's speed and error.

3. **Path Planning and Data Export**
    - Select the path planning simulation to test the control law.
    - Optionally, export the simulation data to a CSV file for further analysis.

## Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the existing style and include appropriate tests.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.

---

Feel free to reach out if you have any questions or suggestions regarding the project. Happy coding!

**Maintainer:** Elena Villalba (evillalba001@gmail.com)


