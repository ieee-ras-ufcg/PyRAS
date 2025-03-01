import numpy as np

# Direct current motor model
class DCMotor:
    def __init__(
        self,
        # Electrical parameters
        R_a, # Armature resistance
        L_a, # Armature inductance
        K_t, # Torque constant

        # Mechanical Parameters
        J, # Rotor's moment of inertia
        b, # Viscous damping coefficient

        dt=1e-4, # Differential time step

        # Initial motor status parameters (not spinning and no current flowing)
        w=0.0,  # Angular velocity
        i_a=0.0 # Armature current
    ):
        # Time parameters
        self.dt = dt

        # Electrical characteristics of the motor
        self.R_a = R_a
        self.L_a = L_a
        self.K_e = K_t
        self.K_t = K_t
 
        # Mechanical properties
        self.J = J
        self.b = b

        # Motor status
        self.i_a = i_a
        self.w = w
        
    def electromechanical_model(self, v, T):
        # Calculate and update state variables
        i_a_dot = (v - self.i_a * self.R_a - self.w * self.K_e) / self.L_a

        # Integrate using Euler's Method
        self.i_a += i_a_dot * self.dt

        # Calculate and update state variables
        w_dot = self.i_a * self.K_t / self.J - self.w * self.b / self.J - T / self.J
        
        # Integrate using Euler's Method
        self.w += w_dot * self.dt

    def get_output(self):
        return np.array(
            [
                [self.i_a], 
                [self.w]
            ]
        )