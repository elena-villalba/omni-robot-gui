# Import libraries
from RobotMotion import RobotMotion
from RobotSimulation import RobotSimulation
from RobotControlP import RobotControlP
from PlotVelocities import PlotVelocities
from PlotErrors import PlotErrors
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import signal
import csv
import sys
import os

class PathFollowing:
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
        
        self.root = tk.Tk()
        self.root.title("Path Following Simulation")
        self.root.attributes('-zoomed', True) # Maximize the window

        # Create the Path Following window
        self.figure = "lemniscata"
        self.figure_interface = tk.StringVar(value="lemniscata")

        self.saturate_velocities = tk.BooleanVar(value=False)

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
        self.robot_control = RobotControlP()
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
    def main(self,
             init_pos=[2.0, 2.0, 0.0],
             kp_value=0.4,
             sample_time=40.0,
             steps=0.1,
             saturate=False,
             vx_max=None,
             vy_max=None,
             w_max=None):
        
        self.kp_value = kp_value
        self.sample_time = sample_time
        self.steps = steps
        self.saturate = saturate
        self.vx_max = vx_max
        self.vy_max = vy_max
        self.w_max = w_max

        self.robot_control.draw_path(self.ax,self.figure,self.sample_time)
        self.robot_motion.get_init_state(init_pos, self.steps)  

        # Plot the initial point
        self.initial_point.set_data(init_pos[0], init_pos[1])

        # Start animation     
        self.ani = animation.FuncAnimation(self.fig, self.update, init_func=self.init, interval=10, repeat=False)
        self.canvas.draw()

    # Update animation
    def update(self, frame):
        x,y,theta = self.robot_motion.position()
        current_state = [x,y,theta]
        desired_state, desired_state_d = self.robot_control.calculate_desired_state(self.robot_motion.time_elapsed)
        vx, vy, w = self.robot_control.calculate_velocity(current_state,desired_state,desired_state_d,self.kp_value)
        
        # Saturate velocities if required
        if self.saturate:
            vx = np.clip(vx, -self.vx_max, self.vx_max)
            vy = np.clip(vy, -self.vy_max, self.vy_max)
            w = np.clip(w, -self.w_max, self.w_max)
        
        self.robot_motion.step(vx, vy, w)
        x, y, theta = self.robot_motion.position()
        self.robot_simulation.draw_robot([x, y, theta])
       
        self.text_box.set_text(f'Robot Coordinates: ({x:.2f}, {y:.2f})')

        self.velocity_graph.add_data(vx, vy, w, self.robot_motion.time_elapsed)
        self.error_graph.add_data(x,y,theta,desired_state,self.robot_motion.time_elapsed)

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

            kp_value = float(self.kp_entry.get())
            if kp_value > 1.0:
                kp_value = 1.0

            sample_time = float(self.sample_time_entry.get())
            time_steps = float(self.time_steps_entry.get())
            self.figure = str(self.figure_interface.get())

            saturate = self.saturate_velocities.get()
            vx_max = float(self.vx_max_entry.get()) if saturate else None
            vy_max = float(self.vy_max_entry.get()) if saturate else None
            w_max = float(self.w_max_entry.get()) if saturate else None

            self.main(init_pos,kp_value,sample_time,time_steps,saturate,vx_max, vy_max, w_max)
        except ValueError:
            messagebox.showerror("Error", "Enter the value of all parameters.")

    # Export data to CSV
    def export_data(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Time', 'Vx', 'Vy', 'W', 'X Error', 'Y Error', 'Theta Error'])
                    for t, vx, vy, w, x_err, y_err, t_err in zip(self.velocity_graph.time_steps, 
                                                                 self.velocity_graph.velocities['vx'], 
                                                                 self.velocity_graph.velocities['vy'], 
                                                                 self.velocity_graph.velocities['w'], 
                                                                 self.error_graph.errors['xerror'], 
                                                                 self.error_graph.errors['yerror'], 
                                                                 self.error_graph.errors['terror']):
                        writer.writerow([t, vx, vy, w, x_err, y_err, t_err])
                messagebox.showinfo("Export Successful", "Data exported successfully.")
            else:
                messagebox.showwarning("Export Cancelled", "No file selected for export.")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting data: {str(e)}")

    # Simulation Interface
    def create_interface(self):
        # Path Following frame to hold everything
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

        tk.Label(self.interface_frame, text="Sampling Time (s):").grid(row=3, column=0)
        self.sample_time_entry = tk.Entry(self.interface_frame)
        self.sample_time_entry.grid(row=3, column=1)

        tk.Label(self.interface_frame, text="Time Steps (s):").grid(row=4, column=0)
        self.time_steps_entry = tk.Entry(self.interface_frame)
        self.time_steps_entry.grid(row=4, column=1)

        tk.Label(self.interface_frame, text="kp Value (from 0 to 1):").grid(row=5, column=0)
        self.kp_entry = tk.Entry(self.interface_frame)
        self.kp_entry.grid(row=5, column=1)

        # Select buttons to choose between "lemniscata" and "circle"
        tk.Label(self.interface_frame, text="Path Type:").grid(row=6, column=0)
        lemniscata_radio = tk.Radiobutton(self.interface_frame, text="Lemniscata", variable=self.figure_interface, value="lemniscata")
        lemniscata_radio.grid(row=6, column=1, sticky="w")
        circle_radio = tk.Radiobutton(self.interface_frame, text="Circle", variable=self.figure_interface, value="circle")
        circle_radio.grid(row=6, column=1, sticky="e")

        # Saturation selection
        tk.Label(self.interface_frame, text="Saturate Velocities:").grid(row=7, column=0)
        saturate_yes = tk.Radiobutton(self.interface_frame, text="Yes", variable=self.saturate_velocities, value=True, command=self.toggle_saturation_fields)
        saturate_yes.grid(row=7, column=1, sticky="w")
        saturate_no = tk.Radiobutton(self.interface_frame, text="No", variable=self.saturate_velocities, value=False, command=self.toggle_saturation_fields)
        saturate_no.grid(row=7, column=1, sticky="e")

        # Saturation fields
        tk.Label(self.interface_frame, text="Max Velocity X (m/s):").grid(row=8, column=0)
        self.vx_max_entry = tk.Entry(self.interface_frame)
        self.vx_max_entry.grid(row=8, column=1)
        
        tk.Label(self.interface_frame, text="Max Velocity Y (m/s):").grid(row=9, column=0)
        self.vy_max_entry = tk.Entry(self.interface_frame)
        self.vy_max_entry.grid(row=9, column=1)
        
        tk.Label(self.interface_frame, text="Max Angular Velocity (rad/s):").grid(row=10, column=0)
        self.w_max_entry = tk.Entry(self.interface_frame)
        self.w_max_entry.grid(row=10, column=1)

        # Hide saturation fields initially
        self.toggle_saturation_fields()

        # Buttons to run, export data, and exit the simulation, and back to the previous interface
        run_button = tk.Button(self.interface_frame, text="Run", command=self.run_simulation)
        run_button.grid(row=11, column=1)

        export_button = tk.Button(self.interface_frame, text="Export Data", command=self.export_data)
        export_button.grid(row=11, column=2)

        exit_button = tk.Button(self.interface_frame, text="Exit", command=self.exit_program)
        exit_button.grid(row=11, column=3)

        # Back botton
        back_button = tk.Button(self.interface_frame, text="Back", command=self.back)
        back_button.grid(row=12, column=0)

        # Set up handling of window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def toggle_saturation_fields(self):
        if self.saturate_velocities.get():
            self.vx_max_entry.grid()
            self.vy_max_entry.grid()
            self.w_max_entry.grid()
        else:
            self.vx_max_entry.grid_remove()
            self.vy_max_entry.grid_remove()
            self.w_max_entry.grid_remove()
    
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
    robot_animation = PathFollowing()
    robot_animation.init_simulation()
    robot_animation.root.mainloop()
