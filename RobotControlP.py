# Import libraries
import numpy as np

class RobotControlP: 
    def __init__(self,):
        self.draw = None

    # Draw the path based on the selected figure (lemniscata or circle)
    def draw_path(self, ax, figure="lemniscata", period=40):
        self.ax = ax
        self.figure = figure
        T = period

        self.center_x = 10
        self.center_y = 10
        self.r = 8.0
        self.w = 2*np.pi /T
        t = np.linspace(0, T, int(T*100)) # star, finish, steps

        # Remove the previous path if it exists
        if self.draw is not None:
            self.draw.remove()

        # Plot path
        if (self.figure=="lemniscata"):
            x = self.r * np.sin(self.w*t) + self.center_x
            y = 0.8*self.r*np.sin(2*self.w*t) + self.center_y
            self.draw, = self.ax.plot(x, y, label='Lemniscata path', color='green')
            self.ax.legend()
            self.ax.set_aspect('equal', 'box')

        elif (self.figure=="circle"):
            x = self.r*np.cos(self.w*t) + self.center_x
            y = self.r*np.sin(self.w * t) + self.center_y
            self.draw, = self.ax.plot(x, y, label='Circle path', color='orange')  
            self.ax.legend()
            self.ax.set_aspect('equal', 'box')   

    # Calculate desired state (position and velocity) based on the selected figure
    def calculate_desired_state(self, t):
        if (self.figure=="lemniscata"):
            # Calculate desired position
            xd = self.r*np.sin(self.w*t) + self.center_x
            yd = 0.8*self.r*np.sin(2*self.w*t) + self.center_y
            wd = 0
            desired_state = [xd, yd, wd]

            # Calculate desired velocity
            dxdt = self.r*self.w*np.cos(self.w*t)
            dydt = 1.6*self.r*self.w*np.cos(2*self.w*t)
            wdt = 0
            desired_state_d = [dxdt, dydt, wdt]

            return desired_state, desired_state_d 

        elif (self.figure=="circle"):
            # Calculate Position
            xd = self.r*np.cos(self.w*t) + self.center_x
            yd = self.r*np.sin(self.w*t) + self.center_y
            wd = 0
            desired_state = [xd, yd, wd]

            # Derivatives with respect to t
            dxdt = -self.r*self.w*np.sin(self.w*t)
            dydt = self.r*self.w*np.cos(self.w * t)
            wdt = 0
            desired_state_d = [dxdt, dydt, wdt]

            return desired_state, desired_state_d

    def calculate_velocity(self,current_state, desired_state,desired_state_d,kp=0.4):
        # Convert current_state, desired_state, desired_state_d to NumPy arrays
        current_state = np.asarray(current_state, dtype='float')
        desired_state = np.asarray(desired_state, dtype='float')
        desired_state_d = np.asarray(desired_state_d, dtype='float')

        # Jacobian matrix
        J = np.array([[np.cos(current_state[2]), -np.sin(current_state[2]), 0],
                      [np.sin(current_state[2]),  np.cos(current_state[2]), 0],
                      [ 0                      ,  0                       , 1]])

        # Control gain matrix 
        K = kp*np.array([[1, 0, 0],
                           [0,  1, 0],
                           [0,  0, 1]])
        
        # Calculate error between desired_state and current_state
        error = desired_state - current_state
        
        # Control Law
        qd = np.linalg.pinv(J)@(desired_state_d+K@error) 

        # Extract velocity components
        vx = qd[0]
        vy = qd[1]
        w  = qd[2]

        return vx, vy, w