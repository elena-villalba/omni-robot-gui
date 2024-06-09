# Import libraries
import numpy as np

class PlotErrors:
    def __init__(self, ax):
        # Initialize axis
        self.ax = ax
        self.ax.set_xlim(0, 12)
        self.ax.set_ylim(-2, 5)

        self.errors = {"xerror": [], "yerror": [], "terror": []}
        self.time_steps = []
        self.recent_errors = []  

        # Initialize dictionaries to store errors to plot them
        self.line_xeror, = self.ax.plot([], [], label="x error (m)")
        self.line_yerror, = self.ax.plot([], [], label="y error (m)")
        self.line_thetaerror, = self.ax.plot([], [], label="theta error (m)")
        
        # Set up plot
        self.ax.legend()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("errors")
        self.ax.grid()

    def add_data(self,x,y,theta,desired_state, t):
        # Calculate errors
        x_error = desired_state[0] - x
        y_error = desired_state[1] - y
        theta_error = desired_state[2] - theta
       
        # Add current data to the list of recent errors
        self.recent_errors.append((x_error, y_error, theta_error, t))
        
        # Filter recent errors to contain only data from the last second
        self.recent_errors = [data for data in self.recent_errors if t - data[3] <= 0.5]

        # Update errors if recent errors are not close to zero
        if all(np.isclose([data[0], data[1], data[2]], 0, atol=1e-2).all() for data in self.recent_errors):
            pass
        else:
            self.errors["xerror"].append(x_error)
            self.errors["yerror"].append(y_error)
            self.errors["terror"].append(theta_error)
            self.time_steps.append(t)

            # Update plot lines with new data
            self.line_xeror.set_data(self.time_steps, self.errors["xerror"])
            self.line_yerror.set_data(self.time_steps, self.errors["yerror"])
            self.line_thetaerror.set_data(self.time_steps, self.errors["terror"])
            
            # Adjust plot limits based on time and error values
            if t > 12:
                self.ax.set_xlim(0, t)

            max_value = max(max(self.errors["xerror"]), max(self.errors["yerror"]), max(self.errors["terror"]))
            min_value = min(min(self.errors["xerror"]), min(self.errors["yerror"]), min(self.errors["terror"]))

            if ((max_value > 0) and (max_value > 5)):
                self.ax.set_ylim(-2, (max_value+0.2))
            elif ((min_value < 0) and (min_value < -2)):
                self.ax.set_ylim((min_value-0.2), +5)
            elif (((max_value > 0) and (max_value > 5)) and ((min_value < 0) and (min_value < -2))):
                self.ax.set_ylim((min_value-0.2), (max_value+0.2))
    
    # Function to reset the plot
    def reset_graph(self):
        self.ax.set_xlim(0, 12)
        self.ax.set_ylim(-2, 5)
        self.errors = {"xerror": [], "yerror": [], "terror": []}
        self.time_steps = []
        self.line_xeror.set_data(self.time_steps, self.errors["xerror"])
        self.line_yerror.set_data(self.time_steps, self.errors["yerror"])
        self.line_thetaerror.set_data(self.time_steps, self.errors["terror"])
        self.recent_errors = []
