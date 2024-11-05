import numpy as np

# Differential drive model 
class DifferentialDrive:
    def __init__(
        self,
        r, # Wheel radius
        s, # Space between wheels
        h = 0.0, # Robot height

        dt = 1e-4, # Differential time step

        # Initial pose parameters (aligned with the inertial frame and unmoving)
        x = 0.0,
        y = 0.0,
        theta = 0.0
    ):
        # Time parameters
        self.dt = dt

        # Robot geometry
        self.r = r
        self.s = s
        self.h = h
 
        # Robot pose
        self.x = x
        self.y = y
        self.theta = theta

        # Commands
        self.command = {
            "D" : self.drive_signal,
            "T"  : self.turn_signal
        }

    def kinematic_model(self, phi_dot_L, phi_dot_R):
        # Calculate and update state variables
        x_dot = self.r * np.cos(self.theta) * (phi_dot_L + phi_dot_R) / 2 
        y_dot = self.r * np.sin(self.theta) * (phi_dot_L + phi_dot_R) / 2 
        theta_dot = self.r * (phi_dot_R - phi_dot_L) / self.s

        # Integrate using Euler's Method
        self.x += x_dot * self.dt
        self.y += y_dot * self.dt
        self.theta += theta_dot * self.dt

    def get_output(self):
        return np.array(
            [
                [self.x], 
                [self.y], 
                [self.theta]
            ]
        )
    
    def get_position(self):
        return np.array(
            [
                [self.x], 
                [self.y], 
                [self.h]
            ]
        )
    
    def get_orientation(self):
        return np.array(
            [
                [np.cos(self.theta), -np.sin(self.theta), 0],
                [np.sin(self.theta),  np.cos(self.theta), 0],
                [                 0,                   0, 1]
            ]
        )
    
    def get_pose(self):
        # Get position and orientation
        t = self.get_position()
        R = self.get_orientation()
        
        return np.vstack((np.hstack((R, t)), [0, 0, 0, 1]))
    
    def turn_signal(self, theta, t):
        theta = np.radians(theta)
        theta_dot = theta / t 
        phi_dot = theta_dot * self.s / (2 * self.r)
        phi_dot_signal = phi_dot * np.ones(int(t / self.dt))

        phi_dot_L_signal = -phi_dot_signal
        phi_dot_R_signal =  phi_dot_signal

        return phi_dot_L_signal, phi_dot_R_signal

    def drive_signal(self, d, t):
        v_B = d / t
        phi_dot = v_B / self.r
        phi_dot_signal = phi_dot * np.ones(int(t / self.dt))

        phi_dot_L_signal = phi_dot_signal
        phi_dot_R_signal = phi_dot_signal

        return phi_dot_L_signal, phi_dot_R_signal
    
    def concatenate_signals(self, signals):
        complete_signal = np.hstack(signals)
        time_vector = np.linspace(0, complete_signal.shape[1] * self.dt, complete_signal.shape[1])

        return complete_signal, time_vector