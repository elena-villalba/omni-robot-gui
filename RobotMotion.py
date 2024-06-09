import numpy as np
import scipy.integrate as integrate

class RobotMotion:
    def __init__(self):
        self.params = ()
        self.time_elapsed = 0

    def get_init_state(self, init_state=[0.0, 0.0, 0.0], dt=0.1): # init_stat 0:x, 1:y, 2:w in rad/s; dt in seconds
        self.init_state = np.asarray(init_state, dtype='float')
        self.state = self.init_state.copy()
        self.dt = dt

    # Reset the state and time elapsed
    def reset(self):
        self.time_elapsed = 0

    # Return current position (x, y, theta in rad)
    def position(self):
        x, y, theta = self.state
        return x, y, theta

    # Define the differential equations for the motion model
    def dstate_dt(self, state, t):
        (vx, vy, w) = self.params
        dxdt = vx * np.cos(state[2]) - vy * np.sin(state[2])
        dydt = vx * np.sin(state[2]) + vy * np.cos(state[2])
        dthetadt = w
        return [dxdt, dydt, dthetadt]

    # Perform one integration step based on the provided velocities
    def step(self, vx, vy, w): # w in rad/s
        self.params = (vx, vy, w)
        self.state = integrate.odeint(self.dstate_dt, self.state, [0, self.dt])[1]
        self.time_elapsed += self.dt