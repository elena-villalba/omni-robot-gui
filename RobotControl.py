# Import libraries
import numpy as np

class RobotControl: 
    def __init__(self,):
        pass
     
    def calculate_velocity(self,current_state, desired_state,kp=0.4):
        # Convert current_state and desired_state to NumPy arrays
        current_state = np.asarray(current_state, dtype='float')
        desired_state = np.asarray(desired_state, dtype='float')

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
        qpRef = np.linalg.pinv(J)@K@error

        # Extract velocity components
        vx = qpRef[0]
        vy = qpRef[1]
        w = qpRef[2]

        return vx, vy, w