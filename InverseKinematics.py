from RobotMotion import RobotMotion
from RobotSimulation import RobotSimulation
from RobotControl import RobotControl
from PlotVelocities import PlotVelocities
from PlotErrors import PlotErrors
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import signal
import sys

class InverseKinematics:
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

        # Create the Inverse Kinematics window
        self.root = tk.Tk()
        self.root.title("Inverse Kinematics Simulation")
        self.root.attributes('-zoomed', True)  # Maximize the window
        self.create_interface()

        # Initialize axis
        self.fig, (self.ax, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 5), gridspec_kw={'height_ratios': [2, 1, 1]})
        self.ax.set_xlabel("x (m)")
        self.ax.set_ylabel("y (m)")
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 20)
        self.ax.set_aspect('equal')
        self.ax.grid()

        # Create a text box to display robot coordinates
        self.text_position = (0.75, 0.75)
        self.text_box = self.ax.text(self.text_position[0], self.text_position[1], '', bbox=dict(facecolor='white', alpha=0.9))

        # Initialize several objects
        self.robot_simulation = RobotSimulation(self.ax, delta=30, escala=0.5)
        self.robot_motion = RobotMotion()
        self.robot_control = RobotControl()
        self.velocity_graph = PlotVelocities(self.ax2)
        self.error_graph = PlotErrors(self.ax3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a legend to the plot
        self.legend_labels = ['Initial Point', 'Path']
        self.initial_point, = self.ax.plot([], [], 'ro', label='Initial Point')
        self.line, = self.ax.plot([], [], 'b--', label='Path')
        self.ax.legend()

    def init(self):
        return self.robot_simulation.artists

    # Main function to run the simulation
    def main(self, steps, init_pos=[2.0, 2.0, 0.0], final_pose=[0.0, 0.0, 0.0], kp_value=0.4):
        self.final_pose = final_pose
        self.steps = steps
        self.kp_value = kp_value
        self.robot_motion.get_init_state(init_pos, self.steps)

        # Plot the initial point
        self.initial_point.set_data(init_pos[0], init_pos[1])

        # Start animation
        self.ani = animation.FuncAnimation(self.fig, self.update, init_func=self.init, interval=10, repeat=False)
        self.canvas.draw()

    # Update animation
    def update(self, frame):
        x, y, theta = self.robot_motion.position()
        current_state = [x, y, theta]
        vx, vy, w = self.robot_control.calculate_velocity(current_state, self.final_pose,self.kp_value)
        self.robot_motion.step(vx, vy, w)
        x, y, theta = self.robot_motion.position()
        self.robot_simulation.draw_robot([x, y, theta])

        self.text_box.set_text(f'Robot Coordinates: ({x:.2f}, {y:.2f})')

        self.velocity_graph.add_data(vx, vy, w, self.robot_motion.time_elapsed)
        self.error_graph.add_data(x, y, theta, self.final_pose, self.robot_motion.time_elapsed)

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

            self.robot_simulation.clear_robot()
            self.robot_motion.reset()
            self.velocity_graph.reset_graph()
            self.error_graph.reset_graph()

            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            angulo = float(self.angle_entry.get())
            angulo = angulo * (np.pi / 180)
            init_pos = [x, y, angulo]

            xf = float(self.xf_entry.get())
            yf = float(self.yf_entry.get())
            anglef = float(self.anglef_entry.get())
            anglef = anglef * (np.pi / 180)
            final_pose = [xf, yf, anglef]

            samples = float(self.samples_entry.get())
            kp_value = float(self.kp_entry.get())
            if kp_value > 1.0:
                kp_value = 1.0
            self.main(samples, init_pos, final_pose,kp_value)
        except ValueError:
            messagebox.showerror("Error", "Enter the value of all parameters.")

    # Simulation Interface
    def create_interface(self):
        # Inverse Kinematics frame to hold everything
        self.interface_frame = tk.Frame(self.root)
        self.interface_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Initialize the frame with buttons
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Entry fields and labels for simulation parameters
        tk.Label(self.interface_frame, text="Initial X (m):").grid(row=0, column=0)
        self.x_entry = tk.Entry(self.interface_frame)
        self.x_entry.grid(row=0, column=1)

        tk.Label(self.interface_frame, text="Initial Y (m):").grid(row=1, column=0)
        self.y_entry = tk.Entry(self.interface_frame)
        self.y_entry.grid(row=1, column=1)

        tk.Label(self.interface_frame, text="Initial Angle (degrees):").grid(row=2, column=0)
        self.angle_entry = tk.Entry(self.interface_frame)
        self.angle_entry.grid(row=2, column=1)

        tk.Label(self.interface_frame, text="Final X (m):").grid(row=3, column=0)
        self.xf_entry = tk.Entry(self.interface_frame)
        self.xf_entry.grid(row=3, column=1)

        tk.Label(self.interface_frame, text="Final Y (m):").grid(row=4, column=0)
        self.yf_entry = tk.Entry(self.interface_frame)
        self.yf_entry.grid(row=4, column=1)

        tk.Label(self.interface_frame, text="Final Angle (degrees):").grid(row=5, column=0)
        self.anglef_entry = tk.Entry(self.interface_frame)
        self.anglef_entry.grid(row=5, column=1)

        tk.Label(self.interface_frame, text="Time Steps (s):").grid(row=6, column=0)
        self.samples_entry = tk.Entry(self.interface_frame)
        self.samples_entry.grid(row=6, column=1)

        tk.Label(self.interface_frame, text="kp Value (from 0 to 1):").grid(row=7, column=0)
        self.kp_entry = tk.Entry(self.interface_frame)
        self.kp_entry.grid(row=7, column=1)

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
            self.root.destroy()  # Close the simulation windows
            self.on_back_callback()

if __name__ == "__main__":
    robot_animation = InverseKinematics()
    robot_animation.init_simulation()
    robot_animation.root.mainloop()