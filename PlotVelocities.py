# Import libraries
import numpy as np

class PlotVelocities:
    def __init__(self, ax):
        # Initialize axis
        self.ax = ax
        self.ax.set_xlim(0, 12)
        self.ax.set_ylim(-5, 5)

        self.velocities = {"vx": [], "vy": [], "w": []}
        self.time_steps = []
        self.recent_velocities = []  
        
        # Initialize dictionaries to store velocities to plot them
        self.line_vx, = self.ax.plot([], [], label="vx (m/s)")
        self.line_vy, = self.ax.plot([], [], label="vy (m/s)")
        self.line_w, = self.ax.plot([], [], label="w  (m/s)")
        
        # Set up plot
        self.ax.legend()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Velocities")
        self.ax.grid()

    def add_data(self, vx, vy, w, t):
        # Add current data to the list of recent velocities
        self.recent_velocities.append((vx, vy, w, t))
        
        # Filter recent velocities to contain only data from the last second
        self.recent_velocities = [data for data in self.recent_velocities if t - data[3] <= 0.5]

        # Update velocities if recent errors are not close to zero
        if all(np.isclose([data[0], data[1], data[2]], 0, atol=1e-2).all() for data in self.recent_velocities):
            pass
        else:
            self.velocities["vx"].append(vx)
            self.velocities["vy"].append(vy)
            self.velocities["w"].append(w)
            self.time_steps.append(t)

            # Update plot lines with new data
            self.line_vx.set_data(self.time_steps, self.velocities["vx"])
            self.line_vy.set_data(self.time_steps, self.velocities["vy"])
            self.line_w.set_data(self.time_steps, self.velocities["w"])
            
            # Adjust plot limits based on time and error values
            if t > 12:
                self.ax.set_xlim(0, t)

            max_value = max(max(self.velocities["vx"]), max(self.velocities["vy"]), max(self.velocities["w"]))
            min_value = min(min(self.velocities["vx"]), min(self.velocities["vy"]), min(self.velocities["w"]))

            if ((max_value > 0) and (max_value > 5)):
                self.ax.set_ylim(-5, (max_value+0.2))
            elif ((min_value < 0) and (min_value < -5)):
                self.ax.set_ylim((min_value-0.2), +5)
            elif (((max_value > 0) and (max_value > 5)) and ((min_value < 0) and (min_value < -5))):
                self.ax.set_ylim((min_value-0.2), (max_value+0.2))
    
    # Function to reset the plot
    def reset_graph(self):
        self.ax.set_xlim(0, 12)
        self.ax.set_ylim(-5, 5)
        self.velocities = {"vx": [], "vy": [], "w": []}
        self.time_steps = []
        self.line_vx.set_data(self.time_steps, self.velocities["vx"])
        self.line_vy.set_data(self.time_steps, self.velocities["vy"])
        self.line_w.set_data(self.time_steps, self.velocities["w"])
        self.recent_velocities = []
