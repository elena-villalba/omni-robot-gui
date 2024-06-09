# Import libraries
from RobotMotion import RobotMotion
from RobotSimulation import RobotSimulation
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import signal
import sys
import os

class ForwardKinematics:
    def __init__(self):
        pass
    
    def init_simulation(self, on_back_callback=None): 
        self.on_back_callback = on_back_callback
        self.vx = 0.0
        self.vy = 0.0
        self.w = 0.0
        self.path = []  # List to store the robot's path
        self.line = None  # To store the path line
        self.initial_point = None  # To store the initial point
        self.ani = None

        # Create the Forward Kinematics window
        self.root = tk.Tk()
        self.root.title("Forward Kinematics window")
        self.root.attributes('-zoomed', True) # Maximize the window
        self.create_interface()

        # Initialize axis
        self.fig, self.ax = plt.subplots() 
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)
        self.ax.set_aspect('equal')
        self.ax.grid()

        # Create a text box to display robot coordinates
        self.text_position = (0.75, 0.75)  
        self.text_box = self.ax.text(self.text_position[0], self.text_position[1], '', bbox=dict(facecolor='white', alpha=0.9))

        # Initialize RobotSimulation and RobotMotion objects
        self.robot_simulation = RobotSimulation(self.ax, delta=30, escala=0.5)
        self.robot_motion = RobotMotion()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a legend to the plot
        self.legend_labels = ['Initial Point', 'Path']
        self.initial_point, = self.ax.plot([], [], 'ro', label='Initial Point')
        self.line, = self.ax.plot([], [], 'b--', label='Path')
        self.ax.legend()

    # Initialize the animation
    def init(self):
        return self.robot_simulation.artists

    # Main function to run the simulation
    def main(self,
             init_pos=[2.0, 2.0, 0.0],
             velocities=[0.0, 0.0, 0.0],
             total_time=5.0,
             steps=0.1):
        
        self.steps = steps
        self.robot_motion.get_init_state(init_pos, self.steps)

        self.vx = velocities[0]
        self.vy = velocities[1]
        self.w = velocities[2]

        self.total_time = total_time       

        # Plot the initial point
        self.initial_point.set_data(init_pos[0], init_pos[1])
        
        # Start animation
        self.ani = animation.FuncAnimation(self.fig, self.update, init_func=self.init, interval=10, repeat=False)
        self.canvas.draw()

    # Update animation
    def update(self, frame):
        if self.robot_motion.time_elapsed < self.total_time:
            self.robot_motion.step(self.vx, self.vy, self.w)
            x, y, theta = self.robot_motion.position()
            self.robot_simulation.draw_robot([x, y, theta])
            self.text_box.set_text(f'Robot Coordinates: ({x:.2f}, {y:.2f})')

            # Append the current position to the path
            self.path.append((x, y))

            # Draw the path as a blue dashed line
            if self.path:
                self.path_x, self.path_y = zip(*self.path)  # Unzip the path into x and y coordinates
                self.line.set_data(self.path_x, self.path_y)  # Update the line data

        return self.robot_simulation.artists

    # Run the simulation
    def run_simulation(self):
        try:
            if self.ani is not None:
                self.ani.event_source.stop()
                self.ani._stop()
            
            # Clear the path
            self.path = []
            
            # Remove the old path line if it exists
            if self.line:
                self.line.set_data([], [])
            
            # Clear initial point
            if self.initial_point:
                self.initial_point.set_data([], [])
            
            # Clear robot and reset motion
            self.robot_simulation.clear_robot()
            self.robot_motion.reset()
            
            # Redraw the canvas
            self.canvas.draw()

            # Get initial position and velocities from user input
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            angulo = float(self.angle_entry.get())
            angulo = angulo * (np.pi / 180)
            init_pos = [x, y, angulo]

            vx = float(self.vx_entry.get())
            vy = float(self.vy_entry.get())
            w = float(self.w_entry.get())
            velocities = [vx, vy, w]

            simulation_time = float(self.simulation_time_entry.get())
            samples = float(self.samples_entry.get())
            self.main(init_pos, velocities, simulation_time, samples)
        
        except ValueError:
            messagebox.showerror("Error", "Enter the value of all parameters.")

    # Simulation Interface
    def create_interface(self):
        # Forward Kinematics frame to hold everything
        self.interface_frame = tk.Frame(self.root)
        self.interface_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Initialize the frame with buttons
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Entry fields and labels for simulation parameters
        tk.Label(self.interface_frame, text="Initial X:").grid(row=0, column=0)
        self.x_entry = tk.Entry(self.interface_frame)
        self.x_entry.grid(row=0, column=1)

        tk.Label(self.interface_frame, text="Initial Y:").grid(row=1, column=0)
        self.y_entry = tk.Entry(self.interface_frame)
        self.y_entry.grid(row=1, column=1)

        tk.Label(self.interface_frame, text="Initial Angle (degrees):").grid(row=2, column=0)
        self.angle_entry = tk.Entry(self.interface_frame)
        self.angle_entry.grid(row=2, column=1)

        tk.Label(self.interface_frame, text="vx (m/s):").grid(row=3, column=0)
        self.vx_entry = tk.Entry(self.interface_frame)
        self.vx_entry.grid(row=3, column=1)

        tk.Label(self.interface_frame, text="vy (m/s):").grid(row=4, column=0)
        self.vy_entry = tk.Entry(self.interface_frame)
        self.vy_entry.grid(row=4, column=1)

        tk.Label(self.interface_frame, text="w (rad/s):").grid(row=5, column=0)
        self.w_entry = tk.Entry(self.interface_frame)
        self.w_entry.grid(row=5, column=1)

        tk.Label(self.interface_frame, text="Time (s):").grid(row=6, column=0)
        self.simulation_time_entry = tk.Entry(self.interface_frame)
        self.simulation_time_entry.grid(row=6, column=1)

        tk.Label(self.interface_frame, text="Time Steps (s):").grid(row=7, column=0)
        self.samples_entry = tk.Entry(self.interface_frame)
        self.samples_entry.grid(row=7, column=1)

        # Buttons to run and exit the simulation, and back to the previous interface
        run_button = tk.Button(self.interface_frame, text="Run", command=self.run_simulation)
        run_button.grid(row=8, column=1)

        exit_button = tk.Button(self.interface_frame, text="Exit", command=self.exit_program)
        exit_button.grid(row=8, column=2)

        back_button = tk.Button(self.interface_frame, text="Back", command=self.back)
        back_button.grid(row=9, column=0)

        # Set up handling of window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    # Function to handle Ctrl+C signal
    def signal_handler(self, sig, frame):
        print("Ctrl+C pressed. Exiting...")
        self.exit_handler()
    
    # Function to handle program exit
    def exit_handler(self):
        print("Exiting...")
        self.root.quit()
        sys.exit()

    def exit_program(self):
        self.root.destroy()
        os._exit(0)

    def back(self):
        if self.on_back_callback != None:
            self.root.destroy() # Close the simulation windows
            self.on_back_callback()

if __name__ == "__main__":
    robot_animation = ForwardKinematics()
    robot_animation.init_simulation()
    robot_animation.root.mainloop()

